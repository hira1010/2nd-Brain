import os
import sys
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))
from lib import utils

logger = utils.initialize_script("verify_all_updates")

def get_latest_mod_time(directory: Path):
    latest_time = 0
    latest_file = ""
    try:
        for entry in directory.iterdir():
            if entry.is_file():
                mtime = entry.stat().st_mtime
            elif entry.is_dir() and not entry.name.startswith(('.', '_')) and entry.name != 'node_modules':
                mtime, _ = get_latest_mod_time(entry)
            else:
                continue
                
            if mtime > latest_time:
                latest_time = mtime
                latest_file = str(entry.relative_to(ROOT_DIR))
    except (PermissionError, FileNotFoundError):
        pass
    return latest_time, latest_file

def main():
    logger.info("=== Workspace Update Verification Report ===")
    
    # Check top-level content directories
    reports = []
    for d in ROOT_DIR.iterdir():
        if d.is_dir() and not d.name.startswith(('.', '_')) and d.name not in ['scripts', 'lib', 'skills', 'node_modules']:
            mtime, lfile = get_latest_mod_time(d)
            if mtime > 0:
                reports.append({
                    "name": d.name,
                    "time": datetime.fromtimestamp(mtime),
                    "file": lfile
                })
    
    # Sort by time descending
    reports.sort(key=lambda x: x['time'], reverse=True)
    
    print(f"{'Directory':<25} | {'Last Updated':<20} | {'Latest File'}")
    print("-" * 80)
    for r in reports:
        print(f"{r['name']:<25} | {r['time'].strftime('%Y-%m-%d %H:%M'):<20} | {r['file']}")
    
    logger.info("Verification complete.")

if __name__ == "__main__":
    main()
