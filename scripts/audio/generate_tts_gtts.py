from pathlib import Path

from gtts import gTTS

LYRICS = [
    {"text": "遘伜ｯ・", "filename": "01_secret.mp3"},
    {"text": "蝨ｰ蜻ｳ蟄撰ｼ・", "filename": "02_jimiko.mp3"},
    {"text": "譛ｬ豌暦ｼ・", "filename": "03_really.mp3"},
    {"text": "縺ｾ縺輔°・・", "filename": "04_noway.mp3"},
    {"text": "隕夐・", "filename": "05_awakening.mp3"},
    {"text": "鄒弱＠縺・", "filename": "06_beautiful.mp3"},
    {"text": "譛蠑ｷ", "filename": "07_strongest.mp3"},
]

OUTPUT_DIR = Path("mv-project/public/audio_parts")


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Starting TTS generation...")
    for line in LYRICS:
        path = OUTPUT_DIR / line["filename"]
        tts = gTTS(line["text"], lang="ja")
        tts.save(str(path))
        print(f"Generated: {line['text']} -> {path}")

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
