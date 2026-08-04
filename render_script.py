import os
import sys
import requests
import asyncio
import numpy as np

# Force unbuffered stdout so logs stream directly into GitHub Actions UI
sys.stdout.reconfigure(line_buffering=True)

# Patch Pillow compatibility before MoviePy imports
from PIL import Image, ImageDraw, ImageFont
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

import edge_tts
from moviepy.editor import VideoClip, AudioFileClip, AudioArrayClip, CompositeAudioClip

# Ensure target directory exists
os.makedirs("assets/ig-media", exist_ok=True)

IMAGE_URL = "https://raw.githubusercontent.com/safetyfirstsolarLLC/Europe-Northamerica-network/main/assets/ig-media/spongebob1%20.jpg"
TEMP_RAW_IMG = "raw_input_product.jpg"
LOCAL_AUDIO_TTS = "voiceover_raw.mp3"
OUTPUT_VIDEO = "assets/ig-media/spongebob_reel1.mp4"

# ==========================================
# 1. DOWNLOAD PRODUCT & FAST ALPHA REMOVAL
# ==========================================
print("--- 1. Downloading product image... ---", flush=True)
try:
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(IMAGE_URL, headers=headers, timeout=15)
    r.raise_for_status()
    with open(TEMP_RAW_IMG, 'wb') as f:
        f.write(r.content)
    print("✅ Image downloaded successfully.", flush=True)
except Exception as e:
    print(f"❌ Download error: {e}", flush=True)
    sys.exit(1)

product_raw = Image.open(TEMP_RAW_IMG).convert("RGBA")

# Fast numpy chroma keying to drop white/near-white studio backgrounds
data = np.array(product_raw)
r_ch, g_ch, b_ch, a_ch = data.T
white_areas = (r_ch > 235) & (g_ch > 235) & (b_ch > 235)
data[..., 3][white_areas.T] = 0

product_img = Image.fromarray(data)

# Square cutout container
p_w, p_h = product_img.size
max_d = max(p_w, p_h)
square_bg = Image.new("RGBA", (max_d, max_d), (0, 0, 0, 0))
square_bg.paste(product_img, ((max_d - p_w) // 2, (max_d - p_h) // 2), product_img)
product_core = square_bg

# ==========================================
# 2. VOICE & MUSIC SYNTHESIS
# ==========================================
print("--- 2. Generating Voiceover & Techno Track... ---", flush=True)

voice_text = "Stop buying plain socks! Grab your limited edition SpongeBob 3D streetwear socks today. Link in bio!"
VOICE = "en-US-ChristopherNeural"

async def generate_voiceover():
    communicate = edge_tts.Communicate(voice_text, VOICE, rate="+15%")
    await communicate.save(LOCAL_AUDIO_TTS)

try:
    asyncio.run(generate_voiceover())
    print("✅ Voiceover synthesized.", flush=True)
except Exception as e:
    print(f"❌ Voiceover synthesis failed: {e}", flush=True)
    sys.exit(1)

raw_voice_clip = AudioFileClip(LOCAL_AUDIO_TTS)
total_duration = round(raw_voice_clip.duration + 1.2, 2)

sample_rate = 44100
t_audio = np.linspace(0, total_duration, int(sample_rate * total_duration), False)

bpm = 128
beat_freq = bpm / 60.0

kick_env = np.exp(-14 * ((t_audio * beat_freq) % 1.0))
kick_wave = np.sin(2 * np.pi * (55 + 100 * kick_env) * t_audio) * kick_env

synth_freqs = [261.63, 311.13, 392.00, 466.16]
note_index = (t_audio * beat_freq * 4).astype(int) % len(synth_freqs)
current_freqs = np.array([synth_freqs[i] for i in note_index])
synth_env = np.exp(-10 * ((t_audio * beat_freq * 4) % 1.0))
synth_wave = np.sin(2 * np.pi * current_freqs * t_audio) * synth_env * 0.2

techno_mono = (kick_wave * 0.45 + synth_wave * 0.25)
techno_stereo = np.vstack([techno_mono, techno_mono]).T
techno_music_clip = AudioArrayClip(techno_stereo, fps=sample_rate).set_duration(total_duration)

final_audio = CompositeAudioClip([
    raw_voice_clip.volumex(1.5), 
    techno_music_clip.volumex(0.35)
]).set_duration(total_duration)

# ==========================================
# 3. FRAME GENERATOR
# ==========================================
print("--- 3. Rendering video frames... ---", flush=True)

def make_frame(t):
    bg_canvas = Image.new("RGBA", (1080, 1920), (18, 18, 18, 255))
    
    angle = (t * 140) % 360
    scale = 1.0 + 0.08 * np.sin(2 * np.pi * t * 1.5)
    target_size = (int(620 * scale), int(620 * scale))
    
    scaled_sock = product_core.resize(target_size, Image.Resampling.LANCZOS)
    rotated_sock = scaled_sock.rotate(-angle, expand=True, resample=Image.Resampling.BICUBIC)
    
    sw, sh = rotated_sock.size
    offset = ((1080 - sw) // 2, (1920 - sh) // 2 - 80)
    bg_canvas.paste(rotated_sock, offset, rotated_sock)
    
    draw = ImageDraw.Draw(bg_canvas)
    try:
        font_main = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 68)
        font_pop = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
    except Exception:
        font_main = ImageFont.load_default()
        font_pop = font_main

    text_bottom = "SPONGEBOB DRIP 🧽🔥\nGET YOURS NOW!"
    draw.multiline_text((540, 1600), text_bottom, fill="yellow", font=font_main, anchor="mm", align="center", stroke_width=6, stroke_fill="black")

    popup_text = None
    angle_pop = 45
    pos_pop = (300, 480)

    if 0.3 <= t < 1.5:
        popup_text = "OMG!"
        angle_pop = 45
        pos_pop = (280, 480)
    elif 1.7 <= t < 2.9:
        popup_text = "WOW!"
        angle_pop = -45
        pos_pop = (800, 480)
    elif 3.1 <= t < 4.5:
        popup_text = "LINK IN BIO!"
        angle_pop = 35
        pos_pop = (540, 320)

    if popup_text:
        txt_img = Image.new("RGBA", (850, 320), (0, 0, 0, 0))
        txt_draw = ImageDraw.Draw(txt_img)
        txt_draw.text((425, 160), popup_text, fill="cyan", font=font_pop, anchor="mm", stroke_width=8, stroke_fill="black")
        
        p_scale = 1.0 + 0.12 * np.sin(2 * np.pi * t * 3.0)
        txt_img = txt_img.resize((int(850 * p_scale), int(320 * p_scale)), Image.Resampling.LANCZOS)
        
        txt_rotated = txt_img.rotate(angle_pop, expand=True, resample=Image.Resampling.BICUBIC)
        rw, rh = txt_rotated.size
        bg_canvas.paste(txt_rotated, (pos_pop[0] - rw//2, pos_pop[1] - rh//2), txt_rotated)

    return np.array(bg_canvas.convert("RGB"))

# ==========================================
# 4. EXPORT MP4 VIDEO
# ==========================================
print("--- 4. Exporting MP4 video... ---", flush=True)
video_clip = VideoClip(make_frame, duration=total_duration)
final_video = video_clip.set_audio(final_audio)

try:
    final_video.write_videofile(
        OUTPUT_VIDEO,
        fps=24,
        codec='libx264',
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True,
        verbose=True,
        logger='bar'
    )
    print(f"✅ Reel Rendered Successfully: {OUTPUT_VIDEO}", flush=True)
except Exception as e:
    print(f"❌ MoviePy Export Failed: {e}", flush=True)
    sys.exit(1)
