import os
import io
import requests
import numpy as np
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoClip, AudioFileClip, AudioArrayClip, CompositeAudioClip
from moviepy.audio.fx.all import speedx

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
    with open(TEMP_RAW_IMG, 'rb') as i:
        output_data = remove(i.read())
        product_img = Image.open(io.BytesIO(output_data)).convert("RGBA")
else:
    product_img = Image.open(TEMP_RAW_IMG).convert("RGBA")

# Make square box around cutout
p_w, p_h = product_img.size
max_d = max(p_w, p_h)
square_bg = Image.new("RGBA", (max_d, max_d), (0, 0, 0, 0))
square_bg.paste(product_img, ((max_d - p_w) // 2, (max_d - p_h) // 2), product_img)
product_core = square_bg

# ==========================================
# 2. SPUNKY CHILDLIKE VOICE & TECHNO MUSIC GENERATOR
# ==========================================
print("--- 2. Creating voiceover & procedural techno track... ---")

# A. Generate Voiceover
voice_text = "Stop buying plain socks! Grab your limited edition SpongeBob 3D streetwear socks today. Link in bio!"
tts = gTTS(text=voice_text, lang='en', tld='co.uk', slow=False)
tts.save(LOCAL_AUDIO_TTS)

# Pitch-shift / Speed-up voice (1.28x) to make it spunky and childlike
raw_voice_clip = AudioFileClip(LOCAL_AUDIO_TTS)
spunky_voice = raw_voice_clip.fx(speedx, 1.28)
total_duration = spunky_voice.duration + 1.2

# B. Generate 100% Royalty-Free Techno Beat in Numpy (128 BPM)
sample_rate = 44100
t_audio = np.linspace(0, total_duration, int(sample_rate * total_duration), False)

# 128 BPM Kick drum synth pulse
bpm = 128
beat_freq = bpm / 60.0
kick_env = np.exp(-12 * ((t_audio * beat_freq) % 1.0))
kick_wave = np.sin(2 * np.pi * (60 + 120 * kick_env) * t_audio) * kick_env

# Upbeat Techno Synth Arpeggio
synth_freqs = [261.63, 311.13, 392.00, 466.16] # C minor chord
note_index = (t_audio * beat_freq * 4).astype(int) % len(synth_freqs)
current_freqs = np.array([synth_freqs[i] for i in note_index])
synth_env = np.exp(-8 * ((t_audio * beat_freq * 4) % 1.0))
synth_wave = np.sin(2 * np.pi * current_freqs * t_audio) * synth_env * 0.25

# Combine kick + synth beat
techno_audio = (kick_wave * 0.4 + synth_wave * 0.3)
techno_stereo = np.vstack([techno_audio, techno_audio]).T

techno_music_clip = AudioArrayClip(techno_stereo, fps=sample_rate).set_duration(total_duration)

# Mix Voice (loud) + Techno (background)
final_audio = CompositeAudioClip([spunky_voice.volumex(1.4), techno_music_clip.volumex(0.35)])

# ==========================================
# 3. HYPNOTIC RAINBOW & POPUP TEXT GENERATOR
# ==========================================
print("--- 3. Rendering video frames... ---")

# Precompute grid for fast Hypnotic Rainbow calculations
h_res, w_res = 480, 270 # Low-res math buffer scaled to 1080x1920
y_idx, x_idx = np.ogrid[-h_res//2:h_res//2, -w_res//2:w_res//2]
r_grid = np.sqrt(x_idx**2 + y_idx**2)
theta_grid = np.arctan2(y_idx, x_idx)

def make_frame(t):
    # A. Generate Hypnotic Rainbow Spiral Background
    hue = (theta_grid / (2 * np.pi) + r_grid * 0.02 - t * 0.8) % 1.0
    sat = np.ones_like(hue) * 0.95
    val = np.ones_like(hue) * 0.90
    
    # Convert HSV to RGB
    hsv = np.stack([hue, sat, val], axis=-1)
    rgb = (Image.fromarray((hsv * 255).astype('uint8'), mode='HSV').convert('RGB'))
    bg_canvas = rgb.resize((1080, 1920), Image.Resampling.BILINEAR).convert("RGBA")
    
    # B. Rotating / Spinning Sock
    angle = (t * 140) % 360
    scale = 1.0 + 0.08 * np.sin(2 * np.pi * t * 1.5)
    target_size = (int(620 * scale), int(620 * scale))
    
    scaled_sock = product_core.resize(target_size, Image.Resampling.LANCZOS)
    rotated_sock = scaled_sock.rotate(-angle, expand=True, resample=Image.Resampling.BICUBIC)
    
    # Paste Spinning Sock in Center
    sw, sh = rotated_sock.size
    offset = ((1080 - sw) // 2, (1920 - sh) // 2 - 80)
    bg_canvas.paste(rotated_sock, offset, rotated_sock)
    
    # C. Draw Dynamic Text & 45-Degree Side Popups
    draw = ImageDraw.Draw(bg_canvas)
    try:
        font_main = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 68)
        font_pop = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 75)
    except Exception:
        font_main = ImageFont.load_default()
        font_pop = font_main

    # Constant Bottom Banner
    text_bottom = "SPONGEBOB DRIP 🧽🔥\nGET YOURS NOW!"
    draw.multiline_text((540, 1600), text_bottom, fill="yellow", font=font_main, anchor="mm", align="center", stroke_width=6, stroke_fill="black")

    # D. 45-Degree Rotating Pop-Up Texts ("OMG!", "WOW!", "LINK IN BIO!")
    popup_text = None
    angle_pop = 45
    pos_pop = (220, 450) # Left side

    if 0.4 <= t < 1.6:
        popup_text = "OMG!"
        angle_pop = 45
        pos_pop = (260, 500)
    elif 1.8 <= t < 3.0:
        popup_text = "WOW!"
        angle_pop = -45
        pos_pop = (820, 500)
    elif 3.2 <= t < 4.8:
        popup_text = "LINK IN BIO! 🔥"
        angle_pop = 35
        pos_pop = (540, 320)

    if popup_text:
        # Create separate transparent layer for angled text burst
        txt_img = Image.new("RGBA", (800, 300), (0, 0, 0, 0))
        txt_draw = ImageDraw.Draw(txt_img)
        txt_draw.text((400, 150), popup_text, fill="cyan", font=font_pop, anchor="mm", stroke_width=7, stroke_fill="black")
        
        # Pulse size
        p_scale = 1.0 + 0.15 * np.sin(2 * np.pi * t * 3.0)
        txt_img = txt_img.resize((int(800 * p_scale), int(300 * p_scale)), Image.Resampling.LANCZOS)
        
        # Rotate 45 degrees
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
