import os
import shutil
import sys
from pathlib import Path

# Project root setup for logging
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))
from lib import utils

logger = utils.initialize_script("cleanup_temp")

def main():
    temp_dir = Path(os.environ.get("TEMP", ""))
    if not temp_dir.exists():
        logger.error("Could not locate %TEMP% directory.")
        return

    logger.info(f"--- Starting Cleanup of {temp_dir} ---")
    
    files_deleted = 0
    dirs_deleted = 0
    errors = 0
    
    # Iterate through contents
    for item in temp_dir.iterdir():
        try:
            if item.is_file():
                item.unlink()
                files_deleted += 1
            elif item.is_dir():
                shutil.rmtree(item)
                dirs_deleted += 1
        except Exception:
            # Many files in Temp will be in use, which is expected
            errors += 1
            
    logger.info(f"Cleanup finished: Deleted {files_deleted} files and {dirs_deleted} directories.")
    logger.info(f"Skipped {errors} items (currently in use or permission denied).")

if __name__ == "__main__":
    main()
