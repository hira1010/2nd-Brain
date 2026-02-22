import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import requests

from lib.utils import setup_logger


VOICEVOX_URL = "http://127.0.0.1:50021"
SPEAKER_ID = 1
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma2")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

logger = setup_logger("scripts.elevenlabs_video_agent")


@dataclass
class VideoPlan:
    narration: str
    search_query: str
    text_overlay: str


PROMPT_TEMPLATE = """
You are a video producer. Create a short, engaging 15-second script about: "{topic}".
Response MUST be valid JSON with this exact structure:
{{
    "narration": "The text for the narrator to speak (Japanese).",
    "search_query": "English keyword to search for stock video (e.g., nature, technology, cats).",
    "text_overlay": "Short text keyword to show on screen."
}}
Do not add markdown formatting or extra text.
""".strip()


def parse_plan(content: Dict[str, Any]) -> VideoPlan:
    return VideoPlan(
        narration=str(content.get("narration", "")).strip(),
        search_query=str(content.get("search_query", "")).strip(),
        text_overlay=str(content.get("text_overlay", "")).strip(),
    )


def generate_script_with_ollama(topic: str) -> Optional[VideoPlan]:
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [{"role": "user", "content": PROMPT_TEMPLATE.format(topic=topic)}],
        "stream": False,
        "format": "json",
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        response.raise_for_status()
        raw = response.json()["message"]["content"]
        return parse_plan(json.loads(raw))
    except Exception as exc:
        logger.warning("Ollama failed: %s", exc)
        return None


def generate_script_with_openai(topic: str) -> Optional[VideoPlan]:
    if not OPENAI_API_KEY:
        return None

    try:
        import openai

        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": PROMPT_TEMPLATE.format(topic=topic)}],
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        return parse_plan(json.loads(content))
    except Exception as exc:
        logger.warning("OpenAI failed: %s", exc)
        return None


def generate_script(topic: str) -> VideoPlan:
    logger.info("Generating script for topic: %s", topic)

    plan = generate_script_with_ollama(topic)
    if plan and plan.narration:
        return plan

    plan = generate_script_with_openai(topic)
    if plan and plan.narration:
        return plan

    raise RuntimeError("No LLM available. Start Ollama or set OPENAI_API_KEY.")


def synthesize_voicevox(text: str, output_file: Path) -> Optional[Path]:
    params = {"text": text, "speaker": SPEAKER_ID}
    try:
        query_response = requests.post(f"{VOICEVOX_URL}/audio_query", params=params, timeout=30)
        query_response.raise_for_status()

        synth_response = requests.post(
            f"{VOICEVOX_URL}/synthesis",
            params={"speaker": SPEAKER_ID},
            json=query_response.json(),
            timeout=60,
        )
        synth_response.raise_for_status()

        output_file.write_bytes(synth_response.content)
        return output_file
    except Exception as exc:
        logger.error("VOICEVOX failed: %s", exc)
        return None


def download_pexels_video(query: str, output_file: Path) -> Optional[Path]:
    if not PEXELS_API_KEY:
        logger.info("PEXELS_API_KEY missing. Using fallback color background.")
        return None

    try:
        headers = {"Authorization": PEXELS_API_KEY}
        search_url = f"https://api.pexels.com/videos/search?query={query}&per_page=1&orientation=landscape"
        response = requests.get(search_url, headers=headers, timeout=30)
        response.raise_for_status()
        videos = response.json().get("videos", [])

        if not videos:
            return None

        video_files = videos[0].get("video_files", [])
        if not video_files:
            return None

        selected = next((item for item in video_files if item.get("width", 0) >= 1280), video_files[0])
        download_url = selected["link"]
        data = requests.get(download_url, timeout=60)
        data.raise_for_status()
        output_file.write_bytes(data.content)
        return output_file
    except Exception as exc:
        logger.warning("Pexels download failed: %s", exc)
        return None


def create_final_video(audio_path: Path, video_path: Optional[Path], text_overlay: str, output_path: Path) -> None:
    from moviepy.editor import (
        AudioFileClip,
        ColorClip,
        CompositeVideoClip,
        TextClip,
        VideoFileClip,
    )

    audio_clip = AudioFileClip(str(audio_path))
    final_duration = audio_clip.duration + 1.0

    if video_path and video_path.exists():
        video_clip = VideoFileClip(str(video_path))
        if video_clip.duration < final_duration:
            video_clip = video_clip.loop(duration=final_duration)
        else:
            video_clip = video_clip.subclip(0, final_duration)
    else:
        video_clip = ColorClip(size=(1280, 720), color=(50, 50, 100), duration=final_duration)

    video_clip = video_clip.set_audio(audio_clip)

    try:
        text_clip = TextClip(
            text_overlay,
            fontsize=80,
            color="white",
            font="Arial-Bold",
            stroke_color="black",
            stroke_width=2,
        ).set_pos("center").set_duration(final_duration)
        final_clip = CompositeVideoClip([video_clip, text_clip])
    except Exception as exc:
        logger.warning("Text overlay failed: %s", exc)
        final_clip = video_clip

    final_clip.write_videofile(str(output_path), fps=24, codec="libx264", audio_codec="aac")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate short AI video clips.")
    parser.add_argument("topic", help="Video topic")
    parser.add_argument("--work-dir", type=Path, default=Path.cwd())
    parser.add_argument("--audio", default="output_audio.wav")
    parser.add_argument("--video", default="stock_video.mp4")
    parser.add_argument("--output", default="final_result.mp4")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    work_dir = args.work_dir
    work_dir.mkdir(parents=True, exist_ok=True)

    plan = generate_script(args.topic)
    audio_path = synthesize_voicevox(plan.narration, work_dir / args.audio)
    if not audio_path:
        return 1

    video_path = download_pexels_video(plan.search_query, work_dir / args.video)
    create_final_video(audio_path=audio_path, video_path=video_path, text_overlay=plan.text_overlay, output_path=work_dir / args.output)
    logger.info("Video generated: %s", work_dir / args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
