import os
import requests
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip

# Ensure output directory exists
os.makedirs("assets/ig-media", exist_ok=True)

IMAGE_URL = "https://raw.githubusercontent.com/safetyfirstsolarLLC/Europe-Northamerica-network/main/assets/ig-media/spongebob1%20.jpg"
LOCAL_IMG = "product_temp.jpg"
LOCAL_AUDIO = "voiceover.mp3"
OUTPUT_VIDEO = "assets/ig-media/spongebob_reel1.mp4"

# 1. Download image
r = requests.get(IMAGE_URL)
with open(LOCAL_IMG, 'wb') as f:
    f.write(r.content)

# 2. Generate AI Voiceover
voice_text = "Stop buying plain socks! Grab your limited edition SpongeBob 3D streetwear socks today. Link in bio!"
tts = gTTS(text=voice_text, lang='en', slow=False)
tts.save(LOCAL_AUDIO)

# 3. Stitch 9:16 HD Reel Video
audio_clip = AudioFileClip(LOCAL_AUDIO)
duration = audio_clip.duration + 1.5

image_clip = ImageClip(LOCAL_IMG).set_duration(duration).resize((1080, 1920))

# Standard MoviePy v1.0.3 TextClip syntax
txt_clip = TextClip(
    "SPONGEBOB STREETWEAR 🧽🔥\nLINK IN BIO!", 
    fontsize=55, 
    color='yellow', 
    font='DejaVu-Sans-Bold',
    method='caption',
    size=(900, None)
).set_position(('center', 1450)).set_duration(duration)

video = CompositeVideoClip([image_clip, txt_clip]).set_audio(audio_clip)
video.write_videofile(OUTPUT_VIDEO, fps=24, codec='libx264', audio_codec='aac')

print(f"✅ Video successfully created in cloud: {OUTPUT_VIDEO}")
