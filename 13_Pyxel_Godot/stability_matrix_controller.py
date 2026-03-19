import subprocess
import os
import sys
import psutil
from pathlib import Path

# プロジェクトルートのパスを通す
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from lib import config

def is_running():
    """Stability Matrixが起動中かどうかを確認する"""
    target = config.STABILITY_MATRIX_EXE.name
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] == target:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def start_stability_matrix():
    """Stability Matrixを起動する"""
    if is_running():
        print("Stability Matrix is already running.")
        return

    exe_path = config.STABILITY_MATRIX_EXE
    if not exe_path.exists():
        print(f"Error: Stability Matrix executable not found at {exe_path}")
        return

    print(f"Starting Stability Matrix from {exe_path}...")
    try:
        # バックグラウンドで起動
        subprocess.Popen([str(exe_path)], creationflags=subprocess.CREATE_NEW_CONSOLE)
        print("Successfully launched Stability Matrix.")
    except Exception as e:
        print(f"Failed to launch Stability Matrix: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Stability Matrix Controller")
    parser.add_argument("--start", action="store_true", help="Start Stability Matrix")
    parser.add_argument("--status", action="store_true", help="Check status of Stability Matrix")

    args = parser.parse_args()

    if args.start:
        start_stability_matrix()
    elif args.status:
        if is_running():
            print("Status: Stability Matrix is RUNNING")
        else:
            print("Status: Stability Matrix is NOT RUNNING")
    else:
        parser.print_help()
