import sys
import os

# Add the target directory to sys.path
target_dir = r"c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画\05_設定\ACE-Step-1.5"
sys.path.append(target_dir)

try:
    from acestep import model_downloader
    print("Starting download...")
    model_downloader.main()
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"Error: {e}")
