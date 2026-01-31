# Audio Generation Script (gTTS)
from gtts import gTTS
import os

lyrics = [
    {"text": "秘密", "filename": "01_secret.mp3"},
    {"text": "地味子？", "filename": "02_jimiko.mp3"},
    {"text": "本気？", "filename": "03_really.mp3"},
    {"text": "まさか！", "filename": "04_noway.mp3"},
    {"text": "覚醒", "filename": "05_awakening.mp3"},
    {"text": "美しい", "filename": "06_beautiful.mp3"},
    {"text": "最強", "filename": "07_strongest.mp3"}
]

output_dir = "mv-project/public/audio_parts"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print("Starting TTS generation...")
for line in lyrics:
    path = os.path.join(output_dir, line["filename"])
    tts = gTTS(line["text"], lang='ja')
    tts.save(path)
    print(f"Generated: {line['text']} -> {path}")

print("Done.")
