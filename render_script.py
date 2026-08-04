import os
import sys
import gc
import requests
import asyncio
import traceback
import numpy as np

# Stream stdout immediately
sys.stdout.reconfigure(line_buffering=True)

# Patch Pillow compatibility before MoviePy imports
from PIL import Image, ImageDraw, ImageFont
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

import edge_tts
from moviepy.editor import VideoClip, AudioFileClip

os.makedirs("assets/ig-media", exist_ok=True)

IMAGE_URL = "https://raw.githubusercontent.com/safetyfirstsolarLLC/Europe-Northamerica-network/main/assets/ig-media/spongebob1%20.jpg"
TEMP_RAW_IMG = "raw_input_product.jpg"

# List of female voices to render
VOICE_VARIANTS = [
    {"name": "ana",   "voice": "en-US-AnaNeural",   "rate": "+28%", "pitch": "+12Hz"},
    {"name": "ava",   "voice": "en-US-AvaNeural",   "rate": "+25%", "pitch": "+10Hz"},
    {"name": "emma",  "voice": "en-US-EmmaNeural",  "rate": "+25%", "pitch": "+8Hz"},
    {"name": "aria",  "voice": "en-US-AriaNeural",  "rate": "+25%", "pitch": "+5Hz"},
    {"name": "sonia", "voice": "en-GB-SoniaNeural", "rate": "+20%", "pitch": "+8Hz"},
]

def prepare_product_image():
    print("--- 1. Downloading product image... ---", flush=True)
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(IMAGE_URL, headers=headers, timeout=15)
    r.raise_for_status()
    with open(TEMP_RAW_IMG, 'wb') as f:
        f.write(r.content)
    print("✅ Image downloaded successfully.", flush=True)

    product_raw = Image.open(TEMP_RAW_IMG).convert("RGBA")

    # Fast numpy background keying
    data = np.array(product_raw)
    r_ch, g_ch, b_ch, a_ch = data.T
    white_areas = (r_ch > 235) & (g_ch > 235) & (b_ch > 235)
    data[..., 3][white_areas.T] = 0

    product_img = Image.fromarray(data)

    p_w, p_h = product_img.size
    max_d = max(p_w, p_h)
    square_bg = Image.new("RGBA", (max_d, max_d), (0, 0, 0, 0))
    square_bg.paste(product_img, ((max_d - p_w) // 2, (max_d - p_h) // 2), product_img)
    
    del data
    gc.collect()
    return square_bg

def render_video_for_voice(variant, product_core):
    variant_name = variant["name"]
    voice_id = variant["voice"]
    rate = variant["rate"]
    pitch = variant["pitch"]
    
    local_tts = f"voiceover_{variant_name}.mp3"
    output_video = f"assets/ig-media/spongebob_reel_{variant_name}.mp4"
    
    print(f"\n==========================================", flush=True)
    print(f"🎬 Processing Voice: {variant_name.upper()} ({voice_id})", flush=True)
    print(f"==========================================", flush=True)

    voice_text = "Boring socks? NO WAY! 😱 Level up your fit with these crazy SpongeBob 3D drip socks! They are going FAST, hit that link in bio right now!"

    async def generate_voiceover():
        communicate = edge_tts.Communicate(
            voice_text, 
            voice_id, 
            rate=rate, 
            pitch=pitch
        )
        await communicate.save(local_tts)

    asyncio.run(generate_voiceover())
    print(f"✅ Voiceover synthesized ({local_tts})", flush=True)

    final_audio = AudioFileClip(local_tts)
    total_duration = round(final_audio.duration + 0.6, 2)

    try:
        font_main = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 68)
        font_pop = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
    except Exception:
        font_main = ImageFont.load_default()
        font_pop = font_main

    def make_frame(t):
        bg_canvas = Image.new("RGBA", (1080, 1920), (18, 18, 18, 255))
        
        angle = (t * 220) % 360
        scale = 1.0 + 0.12 * np.sin(2 * np.pi * t * 2.5)
        target_size = (int(640 * scale), int(640 * scale))
        
        scaled_sock = product_core.resize(target_size, Image.Resampling.BILINEAR)
        rotated_sock = scaled_sock.rotate(-angle, expand=True, resample=Image.Resampling.BILINEAR)
        
        sw, sh = rotated_sock.size
        offset = ((1080 - sw) // 2, (1920 - sh) // 2 - 80)
        bg_canvas.paste(rotated_sock, offset, rotated_sock)
        
        draw = ImageDraw.Draw(bg_canvas)
        text_bottom = "SPONGEBOB DRIP 🧽🔥\nGRAB YOURS NOW!"
        draw.multiline_text((540, 1600), text_bottom, fill="yellow", font=font_main, anchor="mm", align="center", stroke_width=6, stroke_fill="black")

        popup_text = None
        angle_pop = 45
        pos_pop = (300, 480)

        if 0.2 <= t < 1.2:
            popup_text = "TOO FIRE! 🔥"
            angle_pop = 35
            pos_pop = (300, 480)
        elif 1.4 <= t < 2.5:
            popup_text = "MUST HAVE! 😱"
            angle_pop = -35
            pos_pop = (780, 480)
        elif 2.7 <= t < 4.2:
            popup_text = "LINK IN BIO! 🛍️"
            angle_pop = 25
            pos_pop = (540, 320)

        if popup_text:
            txt_img = Image.new("RGBA", (880, 320), (0, 0, 0, 0))
            txt_draw = ImageDraw.Draw(txt_img)
            txt_draw.text((440, 160), popup_text, fill="cyan", font=font_pop, anchor="mm", stroke_width=8, stroke_fill="black")
            
            p_scale = 1.0 + 0.15 * np.sin(2 * np.pi * t * 4.0)
            txt_img = txt_img.resize((int(880 * p_scale), int(320 * p_scale)), Image.Resampling.BILINEAR)
            
            txt_rotated = txt_img.rotate(angle_pop, expand=True, resample=Image.Resampling.BILINEAR)
            rw, rh = txt_rotated.size
            bg_canvas.paste(txt_rotated, (pos_pop[0] - rw//2, pos_pop[1] - rh//2), txt_rotated)

        return np.array(bg_canvas.convert("RGB"))

    print(f"--- Exporting MP4 video: {output_video} ---", flush=True)
    video_clip = VideoClip(make_frame, duration=total_duration)
    final_video = video_clip.set_audio(final_audio)

    final_video.write_videofile(
        output_video,
        fps=24,
        codec='libx264',
        audio_codec='aac',
        preset='ultrafast',
        threads=2,
        logger=None
    )
    print(f"✅ Rendered: {output_video}", flush=True)
    
    # Clean up audio resource
    final_audio.close()
    video_clip.close()
    gc.collect()

def main():
    product_core = prepare_product_image()
    
    for variant in VOICE_VARIANTS:
        render_video_for_voice(variant, product_core)
        
    print("\n🎉 ALL 5 VOICE REELS RENDERED SUCCESSFULLY!", flush=True)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\n❌ CRITICAL PYTHON ERROR TRACEBACK:", flush=True)
        traceback.print_exc()
        sys.exit(1)
