import os
import time
import requests
import json
import random
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, ColorClip, concatenate_videoclips
import openai

# --- Configuration ---
# 1. VOICEVOX Settings (Must be running locally)
VOICEVOX_URL = "http://127.0.0.1:50021"
SPEAKER_ID = 1  # ずんだもん (Zundamon) - Change as needed

# 2. Free Video Settings
# Get a free API key from https://www.pexels.com/api/
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY") 

# 3. LLM Settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # Optional if using Ollama
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "gemma2" # or "llama3", "mistral", etc.

# --- Functions ---

def generate_script(topic):
    """
    Uses LLM (Ollama or OpenAI) to generate a short script and search keywords.
    """
    print(f"Thinking about: {topic}...")
    
    prompt = f"""
    You are a video producer. Create a short, engaging 15-second script about: "{topic}".
    Response MUST be valid JSON with this exact structure:
    {{
        "narration": "The text for the narrator to speak (Japanese).",
        "search_query": "English keyword to search for stock video (e.g., 'nature', 'technology', 'cats').",
        "text_overlay": "Short text keyword to show on screen."
    }}
    Do not add markdown formatting or extra text.
    """
    
    # Try Ollama First (Free)
    try:
        print(f"Attempting to use Local LLM (Ollama: {OLLAMA_MODEL})...")
        data = {
            "model": OLLAMA_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "format": "json"
        }
        res = requests.post(OLLAMA_URL, json=data)
        if res.status_code == 200:
            content = res.json()["message"]["content"]
            return json.loads(content)
        else:
             print(f"Ollama returned error: {res.status_code}. Trying fallback...")
    except Exception as e:
        print(f"Ollama connection failed ({e}). trying OpenAI...")

    # Fallback to OpenAI (Paid)
    if OPENAI_API_KEY:
        print("Using OpenAI API...")
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    
    raise Exception("No LLM available. Please ensure Ollama is running (localhost:11434) or OPENAI_API_KEY is set.")

def synthesize_voicevox(text, filename="output_audio.wav"):
    """
    Generates audio using local VOICEVOX engine.
    """
    print(f"Generating Audio via VOICEVOX: {text}")
    
    # 1. Create Audio Query
    params = {"text": text, "speaker": SPEAKER_ID}
    try:
        query_res = requests.post(f"{VOICEVOX_URL}/audio_query", params=params)
        query_res.raise_for_status()
        query_json = query_res.json()

        # 2. Synthesis
        synth_res = requests.post(
            f"{VOICEVOX_URL}/synthesis",
            params={"speaker": SPEAKER_ID},
            json=query_json
        )
        synth_res.raise_for_status()

        with open(filename, "wb") as f:
            f.write(synth_res.content)
        return filename
    except Exception as e:
        print(f"Error connecting to VOICEVOX: {e}")
        print("Please ensure VOICEVOX is running on port 50021.")
        return None

def download_pexels_video(query, filename="stock_video.mp4"):
    """
    Searches and downloads a video from Pexels (Free).
    """
    if not PEXELS_API_KEY:
        print("PEXELS_API_KEY not found. Switching to simple background mode.")
        return None

    print(f"Searching Pexels for: {query}")
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=1&orientation=landscape"
    
    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        data = res.json()
        
        if data["videos"]:
            video_files = data["videos"][0]["video_files"]
            # Find a suitable resolution (e.g. HD)
            target_video = next((v for v in video_files if v["width"] >= 1280), video_files[0])
            download_link = target_video["link"]
            
            print("Downloading video...")
            video_data = requests.get(download_link).content
            with open(filename, "wb") as f:
                f.write(video_data)
            return filename
        else:
            print("No video found on Pexels.")
            return None
    except Exception as e:
        print(f"Pexels API Error: {e}")
        return None

def create_final_video(audio_path, video_path, text_overlay, output_path="final_result.mp4"):
    """
    Combines Audio, Video (or Color Background), and Text Overlay.
    """
    print("Editing final video...")
    
    if not audio_path:
        print("No audio file. Aborting.")
        return

    # Load Audio
    audio_clip = AudioFileClip(audio_path)
    final_duration = audio_clip.duration + 1.0 # Add 1s padding
    
    # Prepare Video Track
    if video_path and os.path.exists(video_path):
        # Use downloaded stock video
        video_clip = VideoFileClip(video_path)
        # Loop video if shorter than audio
        if video_clip.duration < final_duration:
             video_clip = video_clip.loop(duration=final_duration)
        else:
             video_clip = video_clip.subclip(0, final_duration)
    else:
        # Fallback: Simple Color Background
        print("Using color background.")
        video_clip = ColorClip(size=(1280, 720), color=(50, 50, 100), duration=final_duration)
    
    video_clip = video_clip.set_audio(audio_clip)
    
    # Add Text Overlay
    try:
        # Note: If ImageMagick is not configured, TextClip might fail.
        # Ensure ImageMagick is installed and binary path is set if needed.
        txt_clip = TextClip(text_overlay, fontsize=80, color='white', font='Arial-Bold', stroke_color='black', stroke_width=2)
        txt_clip = txt_clip.set_pos('center').set_duration(final_duration)
        final_clip = CompositeVideoClip([video_clip, txt_clip])
    except Exception as e:
        print(f"Warning: Could not create text overlay: {e}")
        final_clip = video_clip

    final_clip.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
    print(f"Done! Saved to {output_path}")

# --- Main Workflow ---
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Free AI Video Agent")
    parser.add_argument("topic", help="Topic to create a video about")
    args = parser.parse_args()

    # 1. Plan
    content = generate_script(args.topic)
    
    # 2. Create Assets
    audio_file = synthesize_voicevox(content["narration"])
    
    # Try getting a video if API key exists, else None
    video_file = download_pexels_video(content["search_query"])
    
    # 3. Assemble
    if audio_file:
        create_final_video(audio_file, video_file, content["text_overlay"])
