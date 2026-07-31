import os
import requests
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip

os.makedirs("assets/ig-media", exist_ok=True)

IMAGE_URL = "https://raw.githubusercontent.com/safetyfirstsolarLLC/Europe-Northamerica-network/main/assets/ig-media/spongebob1%20.jpg"
TEMP_RAW_IMG = "raw_product.jpg"
TEMP_TEXT_IMG = "overlay_product.jpg"
LOCAL_AUDIO = "voiceover.mp3"
OUTPUT_VIDEO = "assets/ig-media/spongebob_reel1.mp4"

# 1. Download source image
r = requests.get(IMAGE_URL)
with open(TEMP_RAW_IMG, 'wb') as f:
    f.write(r.content)

# 2. Draw text using Pillow (No ImageMagick reliance)
img = Image.open(TEMP_RAW_IMG).convert("RGB")
img = img.resize((1080, 1920))

draw = ImageDraw.Draw(img)

# Standard font on Ubuntu runners
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 55)
except Exception:
    font = ImageFont.load_default()

text = "SPONGEBOB STREETWEAR 🧽🔥\nLINK IN BIO!"
# Draw banner text near bottom center
draw.multiline_text((540, 1500), text, fill="yellow", font=font, anchor="mm", align="center")

img.save(TEMP_TEXT_IMG)

# 3. Generate TTS Audio
voice_text = "Stop buying plain socks! Grab your limited edition SpongeBob 3D streetwear socks today. Link in bio!"
tts = gTTS(text=voice_text, lang='en', slow=False)
tts.save(LOCAL_AUDIO)

# 4. Render Video via MoviePy
audio_clip = AudioFileClip(LOCAL_AUDIO)
duration = audio_clip.duration + 1.5

video_clip = ImageClip(TEMP_TEXT_IMG).set_duration(duration)
final_video = video_clip.set_audio(audio_clip)

final_video.write_videofile(
    OUTPUT_VIDEO, 
    fps=24, 
    codec='libx264', 
    audio_codec='aac',
    threads=2
)

print(f"✅ Reel rendered successfully: {OUTPUT_VIDEO}")
