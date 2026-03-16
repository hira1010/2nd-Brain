import sys
import traceback
from pathlib import Path

# Add the target directory to sys.path
TARGET_DIR = Path(r"c:\Users\hirak\Desktop\2nd-Brain\18_繝ｬ繝滓兜雉・ｼｫ逕ｻ\05_險ｭ螳喀ACE-Step-1.5")


def main() -> int:
    sys.path.append(str(TARGET_DIR))
    try:
        from acestep import model_downloader

        print("Starting download...")
        model_downloader.main()
        return 0
    except Exception as e:
        traceback.print_exc()
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
