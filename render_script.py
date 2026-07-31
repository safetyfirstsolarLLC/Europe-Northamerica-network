import os
import glob
import random
import requests
from gtts import gTTS
from moviepy import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

# Ensure output directory exists
os.makedirs("assets/ig-media", exist_ok=True)

LOCAL_AUDIO = "voiceover.mp3"
OUTPUT_VIDEO = "assets/ig-media/spongebob_reel1.mp4"

# 1. Grab all image files inside your GitHub media folder
image_files = glob.glob("assets/ig-media/*.jpg") + glob.glob("assets/ig-media/*.png")

# If no images are found locally yet, download a fallback
if not image_files:
    fallback_url = "https://raw.githubusercontent.com/safetyfirstsolarLLC/Europe-Northamerica-network/main/assets/ig-media/spongebob1%20.jpg"
    r = requests.get(fallback_url)
    with open("assets/ig-media/temp.jpg", 'wb') as f:
        f.write(r.content)
    image_files = ["assets/ig-media/temp.jpg"]

# 2. Pick a random script to keep videos fresh
SCRIPTS = [
    "Stop buying plain socks! Grab your limited edition SpongeBob 3D streetwear socks today. Link in bio!",
    "Why pay $40 for basic socks when you can rock 3D SpongeBob drip? Grab yours before we sell out!",
    "Nostalgia on your feet. Upgrade your streetwear game today. Click the link in bio to shop now!"
]
voice_text = random.choice(SCRIPTS)

# Generate AI Voiceover
tts = gTTS(text=voice_text, lang='en', slow=False)
tts.save(LOCAL_AUDIO)
audio_clip = AudioFileClip(LOCAL_AUDIO)
total_duration = audio_clip.duration + 1.0

# 3. Build a Multi-Image Cut (Changes picture every 2–3 seconds)
num_images = min(len(image_files), 3) # Pick up to 3 images
selected_imgs = random.sample(image_files, num_images)
img_duration = total_duration / num_images

image_clips = []
for img_path in selected_imgs:
    # Resize each image to 9:16 vertical Reel format (1080x1920)
    clip = ImageClip(img_path).with_duration(img_duration).resized((1080, 1920))
    image_clips.append(clip)

# Stitch the images into a sequence
background_video = concatenate_videoclips(image_clips)

# 4. Add Bold Dynamic Text Overlay
txt_clip = TextClip(
    font="Arial.ttf", 
    text="SPONGEBOB STREETWEAR 🧽🔥\nLINK IN BIO!", 
    font_size=55, 
    color='yellow'
).with_position(('center', 1450)).with_duration(total_duration)

# 5. Composite Final Video & Audio
final_video = CompositeVideoClip([background_video, txt_clip]).with_audio(audio_clip)
final_video.write_videofile(OUTPUT_VIDEO, fps=24, codec='libx264', audio_codec='aac')

print(f"✅ Dynamic video created: {OUTPUT_VIDEO}")
