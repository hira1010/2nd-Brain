
import sys
import os
import requests
import argparse
import time
from datetime import datetime

# Import configuration
try:
    import vidu_config as config
except ImportError:
    # Handle case where script is run from a different directory
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import vidu_config as config

def generate_video(prompt, output_file=None):
    if not config.VIDU_API_KEY:
        print("Error: VIDU_API_KEY not found. Please set it in .env or env vars.")
        return

    print(f"Generating Video via Vidu AI...")
    print(f"Prompt: {prompt}")

    headers = {
        "Authorization": f"Bearer {config.VIDU_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt,
        "resolution": config.DEFAULT_RESOLUTION,
        "aspect_ratio": config.DEFAULT_ASPECT_RATIO,
        "duration": config.DEFAULT_DURATION
    }

    try:
        # 1. Send Generation Request
        # Note: This is a hypothetical sync/async flow. Adjust based on real API.
        response = requests.post(config.VIDU_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        # Assume response contains a URL or Job ID. 
        # For this template, we assume it returns a direct video URL or we catch the logic here.
        video_url = data.get("video_url") # Hypothetical key
        
        if not video_url:
            print(f"API Response did not contain video_url: {data}")
            return

        print(f"Video generated successfully. Downloading from {video_url}...")

        # 2. Download Video
        video_data = requests.get(video_url).content
        
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"vidu_{timestamp}.mp4"
            
        with open(output_file, "wb") as f:
            f.write(video_data)
            
        print(f"✅ Saved to: {output_file}")

    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate video using Vidu AI")
    parser.add_argument("--prompt", type=str, required=True, help="Text description for the video")
    parser.add_argument("--out", type=str, help="Output filename")
    
    args = parser.parse_args()
    
    generate_video(args.prompt, args.out)
