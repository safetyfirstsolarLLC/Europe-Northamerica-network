import os
import io
import requests
import numpy as np
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoClip, AudioFileClip

# Only import rembg here to prevent startup delay if needed elsewhere
try:
    from rembg import remove
except ImportError:
    print("⚠️ 'rembg' library not found. Background removal will be skipped.")
    remove = None

os.makedirs("assets/ig-media", exist_ok=True)

# Sources and Output
IMAGE_URL = "https://raw.githubusercontent.com/safetyfirstsolarLLC/Europe-Northamerica-network/main/assets/ig-media/spongebob1%20.jpg"
TEMP_RAW_IMG = "raw_input_product.jpg"
LOCAL_AUDIO = "voiceover.mp3"
OUTPUT_VIDEO = "assets/ig-media/spongebob_reel1.mp4"

# ==========================================
# 1. Prepare Product Asset (Download & Transparent Cutout)
# ==========================================
print("--- Preparing product asset... ---")

# A. Download raw image
r = requests.get(IMAGE_URL)
with open(TEMP_RAW_IMG, 'wb') as f:
    f.write(r.content)

# B. Automatic Background Removal using rembg
if remove:
    print("--- Automatically removing background... ---")
    with open(TEMP_RAW_IMG, 'rb') as i:
        input_data = i.read()
        # Create a transparent PNG output directly in memory
        output_data = remove(input_data)
        product_img = Image.open(io.BytesIO(output_data)).convert("RGBA")
else:
    # Fallback if library missing (wont happen in configured workflow)
    print("--- Using raw image (no background removal)... ---")
    product_img = Image.open(TEMP_RAW_IMG).convert("RGBA")

# Ensure product img is roughly square for clean rotation before animation starts
prod_w, prod_h = product_img.size
max_dim = max(prod_w, prod_h)
background = Image.new("RGBA", (max_dim, max_dim), (0, 0, 0, 0))
offset = ((max_dim - prod_w) // 2, (max_dim - prod_h) // 2)
background.paste(product_img, offset, product_img)
product_core = background

# ==========================================
# 2. Generate Voiceover Audio
# ==========================================
print("--- Generating AI voiceover... ---")
voice_text = "Stop buying plain socks! Grab your limited edition SpongeBob 3D streetwear socks today. Link in bio!"
tts = gTTS(text=voice_text, lang='en', slow=False)
tts.save(LOCAL_AUDIO)
audio_clip = AudioFileClip(LOCAL_AUDIO)
duration = audio_clip.duration + 1.5 # Extra time for visual effect

# ==========================================
# 3. Procedural Animated Frame Generator (9:16)
# ==========================================
print("--- Starting render of animated frames... ---")

def make_frame(t):
    # Canvas setup (9:16 vertical Reel 1080x1920) with a dark gradient/color background
    canvas = Image.new("RGBA", (1080, 1920), (18, 18, 24, 255))
    
    # --- ANIMATION CALCULATIONS ---
    # Angle: Continuous 360 rotation every 3 seconds
    angle = (t * 120) % 360
    
    # Scale: Pulsing bounce effect (heartbeat)
    scale_pulse = 1.0 + 0.08 * np.sin(2 * np.pi * t * 1.5)
    
    # Vertical Motion: Subtle float up/down
    float_offset = 30 * np.sin(2 * np.pi * t * 0.5)
    
    # Base size for the cutout product inside the frame
    base_render_size = 700 
    target_size = (int(base_render_size * scale_pulse), int(base_render_size * scale_pulse))
    
    # --- PROCESS IMAGE ---
    # Resize and Rotate the transparent cutout product
    # Resampling LANCZOS/BICUBIC ensures high visual quality during spin
    scaled_sock = product_core.resize(target_size, Image.Resampling.LANCZOS)
    rotated_sock = scaled_sock.rotate(-angle, expand=True, resample=Image.Resampling.BICUBIC)
    
    # Paste centered product on canvas
    sock_w, sock_h = rotated_sock.size
    offset = ((1080 - sock_w) // 2, (1920 - sock_h) // 2 - 100 + int(float_offset))
    canvas.paste(rotated_sock, offset, rotated_sock)
    
    # --- ADD TEXT OVERLAYS (Hormozi Style) ---
    draw = ImageDraw.Draw(canvas)
    try:
        # Standard font available on default GitHub runners
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        font_cta = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
    except Exception:
        font = ImageFont.load_default()
        font_cta = font
        
    text_top = "LIMITED EDITION 🧽🔥"
    text_bottom = "SPONGEBOB DRIP SOCKS\nLINK IN BIO!"
    
    # Draw top dynamic text (pulsing in color)
    g_val = int(127 + 128 * np.sin(2 * np.pi * t * 1.0)) # Pulse green component 0-255
    draw.text((540, 300), text_top, fill=(255, 255, g_val), font=font, anchor="mm", align="center", stroke_width=4, stroke_fill="black")
    
    # Draw bottom yellow bold text
    draw.multiline_text((540, 1600), text_bottom, fill="yellow", font=font_cta, anchor="mm", align="center", stroke_width=5, stroke_fill="black")
    
    return np.array(canvas.convert("RGB"))

# ==========================================
# 4. Composite Final Video & Export
# ==========================================
print("--- Stitching video & audio... ---")
# Framerate (FPS) 24 provides smooth animation for short form reels
animated_clip = VideoClip(make_frame, duration=duration)
final_video = animated_clip.set_audio(audio_clip)

final_video.write_videofile(
    OUTPUT_VIDEO, 
    fps=24, 
    codec='libx264', 
    audio_codec='aac',
    threads=2, # Use cloud runner threads efficiently
    preset='fast' # Speed up encoding time on cloud runners
)

print(f"✅ Spinning, Transparent Cutout Reel Rendered Successfully: {OUTPUT_VIDEO}")
