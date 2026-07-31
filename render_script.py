import os
import io
import requests
import numpy as np
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoClip, AudioFileClip, AudioArrayClip, CompositeAudioClip

try:
    from rembg import remove
except ImportError:
    remove = None

os.makedirs("assets/ig-media", exist_ok=True)

# Sources & Output
IMAGE_URL = "https://raw.githubusercontent.com/safetyfirstsolarLLC/Europe-Northamerica-network/main/assets/ig-media/spongebob1%20.jpg"
TEMP_RAW_IMG = "raw_input_product.jpg"
LOCAL_AUDIO_TTS = "voiceover_raw.mp3"
OUTPUT_VIDEO = "assets/ig-media/spongebob_reel1.mp4"

# ==========================================
# 1. DOWNLOAD PRODUCT & AUTO-REMOVE BACKGROUND
# ==========================================
print("--- 1. Downloading product image & stripping background... ---")
r = requests.get(IMAGE_URL)
with open(TEMP_RAW_IMG, 'wb') as f:
    f.write(r.content)

if remove:
    try:
        with open(TEMP_RAW_IMG, 'rb') as i:
            output_data = remove(i.read())
            product_img = Image.open(io.BytesIO(output_data)).convert("RGBA")
    except Exception as e:
        print(f"rembg warning: {e}, using raw image")
        product_img = Image.open(TEMP_RAW_IMG).convert("RGBA")
else:
    product_img = Image.open(TEMP_RAW_IMG).convert("RGBA")

# Square cutout container
p_w, p_h = product_img.size
max_d = max(p_w, p_h)
square_bg = Image.new("RGBA", (max_d, max_d), (0, 0, 0, 0))
square_bg.paste(product_img, ((max_d - p_w) // 2, (max_d - p_h) // 2), product_img)
product_core = square_bg

# ==========================================
# 2. SPUNKY VOICE & TECHNO MUSIC GENERATOR
# ==========================================
print("--- 2. Creating voiceover & procedural techno track... ---")

# A. Generate Voiceover
voice_text = "Stop buying plain socks! Grab your limited edition SpongeBob 3D streetwear socks today. Link in bio!"
tts = gTTS(text=voice_text, lang='en', tld='co.uk', slow=False)
tts.save(LOCAL_AUDIO_TTS)

# Spunky Voiceover speed adjustment (Slightly faster playback rate)
raw_voice_clip = AudioFileClip(LOCAL_AUDIO_TTS)
# Play faster by altering duration property cleanly
spunky_voice = raw_voice_clip.fl_time(lambda t: 1.25 * t, apply_to=['audio']).set_duration(raw_voice_clip.duration / 1.25)
total_duration = spunky_voice.duration + 1.2

# B. Generate 100% Royalty-Free Techno Beat in Numpy (128 BPM)
sample_rate = 44100
t_audio = np.linspace(0, total_duration, int(sample_rate * total_duration), False)

bpm = 128
beat_freq = bpm / 60.0

# Punchy Kick drum wave
kick_env = np.exp(-14 * ((t_audio * beat_freq) % 1.0))
kick_wave = np.sin(2 * np.pi * (55 + 100 * kick_env) * t_audio) * kick_env

# Upbeat Synth Pattern (C minor chord synth)
synth_freqs = [261.63, 311.13, 392.00, 466.16]
note_index = (t_audio * beat_freq * 4).astype(int) % len(synth_freqs)
current_freqs = np.array([synth_freqs[i] for i in note_index])
synth_env = np.exp(-10 * ((t_audio * beat_freq * 4) % 1.0))
synth_wave = np.sin(2 * np.pi * current_freqs * t_audio) * synth_env * 0.2

# Stereo Techno Track
techno_mono = (kick_wave * 0.45 + synth_wave * 0.25)
techno_stereo = np.vstack([techno_mono, techno_mono]).T
techno_music_clip = AudioArrayClip(techno_stereo, fps=sample_rate).set_duration(total_duration)

# Composite Voice + Techno
final_audio = CompositeAudioClip([spunky_voice.volumex(1.5), techno_music_clip.volumex(0.4)])

# ==========================================
# 3. HYPNOTIC RAINBOW & POPUP TEXT GENERATOR
# ==========================================
print("--- 3. Rendering video frames... ---")

# Matrix for Hypnotic Rainbow calculations
h_res, w_res = 320, 180
y_idx, x_idx = np.ogrid[-h_res//2:h_res//2, -w_res//2:w_res//2]
r_grid = np.sqrt(x_idx**2 + y_idx**2)
theta_grid = np.arctan2(y_idx, x_idx)

def make_frame(t):
    # A. Hypnotic Rainbow Spiral Background
    hue = (theta_grid / (2 * np.pi) + r_grid * 0.025 - t * 0.9) % 1.0
    sat = np.ones_like(hue) * 0.95
    val = np.ones_like(hue) * 0.90
    
    hsv = np.stack([hue, sat, val], axis=-1)
    rgb_img = Image.fromarray((hsv * 255).astype('uint8'), mode='HSV').convert('RGB')
    bg_canvas = rgb_img.resize((1080, 1920), Image.Resampling.BILINEAR).convert("RGBA")
    
    # B. Spinning Product Sock
    angle = (t * 140) % 360
    scale = 1.0 + 0.08 * np.sin(2 * np.pi * t * 1.5)
    target_size = (int(620 * scale), int(620 * scale))
    
    scaled_sock = product_core.resize(target_size, Image.Resampling.LANCZOS)
    rotated_sock = scaled_sock.rotate(-angle, expand=True, resample=Image.Resampling.BICUBIC)
    
    sw, sh = rotated_sock.size
    offset = ((1080 - sw) // 2, (1920 - sh) // 2 - 80)
    bg_canvas.paste(rotated_sock, offset, rotated_sock)
    
    # C. Main Text & 45-degree Popups
    draw = ImageDraw.Draw(bg_canvas)
    try:
        font_main = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 68)
        font_pop = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
    except Exception:
        font_main = ImageFont.load_default()
        font_pop = font_main

    # Bottom Call To Action Banner
    text_bottom = "SPONGEBOB DRIP 🧽🔥\nGET YOURS NOW!"
    draw.multiline_text((540, 1600), text_bottom, fill="yellow", font=font_main, anchor="mm", align="center", stroke_width=6, stroke_fill="black")

    # D. Rotating Pop-Up Texts ("OMG!", "WOW!", "LINK IN BIO!")
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
        
        # Scale pulsation
        p_scale = 1.0 + 0.12 * np.sin(2 * np.pi * t * 3.0)
        txt_img = txt_img.resize((int(850 * p_scale), int(320 * p_scale)), Image.Resampling.LANCZOS)
        
        # 45 degree rotation
        txt_rotated = txt_img.rotate(angle_pop, expand=True, resample=Image.Resampling.BICUBIC)
        rw, rh = txt_rotated.size
        bg_canvas.paste(txt_rotated, (pos_pop[0] - rw//2, pos_pop[1] - rh//2), txt_rotated)

    return np.array(bg_canvas.convert("RGB"))

# ==========================================
# 4. EXPORT FINAL VIDEO
# ==========================================
print("--- 4. Exporting MP4 video... ---")
video_clip = VideoClip(make_frame, duration=total_duration)
final_video = video_clip.set_audio(final_audio)

final_video.write_videofile(
    OUTPUT_VIDEO,
    fps=24,
    codec='libx264',
    audio_codec='aac',
    threads=2,
    preset='fast'
)

print(f"✅ Hypnotic Techno Reel Rendered Successfully: {OUTPUT_VIDEO}")
