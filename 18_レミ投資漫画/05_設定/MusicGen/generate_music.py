
import os
import sys
import argparse
import time
from datetime import datetime
import torch

# Add configuration
import music_config as config

# Force UTF-8 Output for Windows consoles
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Ensure the ACE-Step library is accessible
# Assuming setup_music_gen.ps1 installed it in editable mode (-e) in the subdir
sys.path.append(config.ACE_STEP_REPO_PATH)

try:
    from acestep import ACEStepPipeline
except ImportError:
    print("Error: 'acestep' module incorrectly installed or not found.")
    print(f"Please run 'setup_music_gen.ps1' first or ensure {config.ACE_STEP_REPO_PATH} is in PYTHONPATH.")
    sys.exit(1)


def generate_music(
    prompt,
    lyrics=None,
    duration=config.DEFAULT_DURATION,
    filename=None,
    bpm=config.DEFAULT_BPM
):
    print("Initializing ACE-Step Pipeline...")
    try:
        pipe = ACEStepPipeline.from_pretrained(
            config.DEFAULT_MODEL,
            dit_model=config.DEFAULT_DIT_MODEL,
            lm_model=config.DEFAULT_LM_MODEL
        )
        
        # Optimize for VRAM if needed (optional offloading)
        # pipe.enable_model_cpu_offload() 
        
    except Exception as e:
        print(f"Failed to load pipeline: {e}")
        return

    import traceback

    # ... (existing imports)

    print(f"Generating Music...")
    print(f"Prompt: {prompt}")
    print(f"Duration: {duration}s")
    if lyrics:
        print(f"Lyrics provided: Yes ({len(lyrics)} chars)")

    start_time = time.time()
    
    try:
        audio = pipe(
            prompt=prompt,
            lyrics=lyrics,
            duration=duration,
            bpm=bpm
        )
    except Exception as e:
        print(f"Generation failed: {e}")
        with open("error_log.txt", "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())
        return

    elapsed = time.time() - start_time
    print(f"Generation finished in {elapsed:.2f} seconds.")

    # Save
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"music_{timestamp}.wav"
    
    if not filename.endswith(".wav"):
        filename += ".wav"
        
    save_path = os.path.join(config.OUTPUT_DIR, filename)
    audio.save(save_path)
    
    print(f"Saved to: {save_path}") # Removed emoji
    return save_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate music using ACE-Step 1.5")
    parser.add_argument("--prompt", type=str, required=True, help="Description of the music style")
    parser.add_argument("--lyrics", type=str, help="Lyrics for the song (optional)")
    parser.add_argument("--duration", type=int, default=config.DEFAULT_DURATION, help="Duration in seconds")
    parser.add_argument("--bpm", type=int, default=config.DEFAULT_BPM, help="Beats per minute")
    parser.add_argument("--out", type=str, help="Output filename")
    
    args = parser.parse_args()
    
    generate_music(
        prompt=args.prompt,
        lyrics=args.lyrics,
        duration=args.duration,
        filename=args.out,
        bpm=args.bpm
    )
