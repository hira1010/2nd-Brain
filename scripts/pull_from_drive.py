import os
import shutil
import sys
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))
from lib import utils

logger = utils.initialize_script("pull_from_drive")

# Google Drive backup destination
BACKUP_DEST = Path("G:/マイドライブ/2nd-Brain_Backup")

# We should skip Git-managed directories if we want to avoid accidental overwrites
# However, for full sync, we might want to be more liberal.
# For now, let's focus on non-git folders or folders that might be huge.
SYNC_DIRS = [
    "05_RPG制作",
    "02_漫画",
    "12_レミ投資漫画",
    "24_RPGツクールMCP"
]

def pull_directory(dirname: str):
    src = BACKUP_DEST / dirname
    dst = ROOT_DIR / dirname
    
    if not src.exists():
        logger.info(f"Source {dirname} not found on Drive. Skipping.")
        return

    logger.info(f"Mirroring {dirname} from Drive (Downloads + Local Clean)...")
    
    files_pulled = 0
    items_deleted = 0
    
    # --- Step 1: Download newer/missing files ---
    for root, dirs, files in os.walk(src):
        rel_path = os.path.relpath(root, src)
        dest_dir = dst / rel_path
        
        if not dest_dir.exists():
            dest_dir.mkdir(parents=True, exist_ok=True)
            
        for f in files:
            src_file = Path(root) / f
            dst_file = dest_dir / f
            
            if not dst_file.exists() or src_file.stat().st_mtime > dst_file.stat().st_mtime:
                shutil.copy2(src_file, dst_file)
                files_pulled += 1

    # --- Step 2: Delete local items not on Drive (Mirror) ---
    for root, dirs, files in os.walk(dst, topdown=False):
        rel_path = os.path.relpath(root, dst)
        src_root = src / rel_path
        
        # Check files
        for f in files:
            local_file = Path(root) / f
            remote_file = src_root / f
            if not remote_file.exists():
                local_file.unlink()
                items_deleted += 1
                
        # Check directories
        for d in dirs:
            local_dir = Path(root) / d
            remote_dir = src_root / d
            if not remote_dir.exists():
                shutil.rmtree(local_dir)
                items_deleted += 1
                
    if files_pulled > 0 or items_deleted > 0:
        logger.info(f"Result: Pulled {files_pulled} files, Deleted {items_deleted} local discrepancies.")
    else:
        logger.info(f"{dirname} is already perfectly mirrored with Drive.")

def main():
    if not BACKUP_DEST.exists():
        logger.error("Google Drive (G:/) is not mounted. Cannot pull updates.")
        return
        
    logger.info("--- Starting Bilateral Pull from Google Drive ---")
    for d in SYNC_DIRS:
        pull_directory(d)
    logger.info("--- Bilateral Pull Finished ---")

if __name__ == "__main__":
    main()
