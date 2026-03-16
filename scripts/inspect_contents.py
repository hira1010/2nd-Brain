import os
import unicodedata
from datetime import datetime

def get_dir_info(path):
    if not os.path.exists(path):
        return None
    files = []
    for root, dirs, filenames in os.walk(path):
        for f in filenames:
            full_path = os.path.join(root, f)
            try:
                stat = os.stat(full_path)
                files.append({
                    'name': os.path.relpath(full_path, path),
                    'size': stat.st_size,
                    'mtime': stat.st_mtime
                })
            except Exception:
                pass
    return files

root = r'C:\Users\hirak\Desktop\2nd-Brain'
dirs_to_check = [
    'note作成用プロンプト', 'note作成用プロンプト',
    'ポスト作成プロンプト', 'ポスト作成プロンプト',
    '18_システム', '18_レミ投資漫画',
    '20_Godot_Pyxel', '20_Pyxel',
    '21_ComfyUI', '21_プロレスゲーム'
]

report_file = r'C:\Users\hirak\Desktop\2nd-Brain\scripts\contents_report.txt'
with open(report_file, 'w', encoding='utf-8') as f:
    for d in dirs_to_check:
        path = os.path.join(root, d)
        f.write(f"=== {d} ===\n")
        info = get_dir_info(path)
        if info is None:
            f.write("Does not exist.\n\n")
            continue
        
        f.write(f"Total files: {len(info)}\n")
        total_size = sum(x['size'] for x in info)
        f.write(f"Total size: {total_size} bytes\n")
        if info:
            latest_mtime = max(x['mtime'] for x in info)
            f.write(f"Latest modification: {datetime.fromtimestamp(latest_mtime)}\n")
            f.write("Sample files:\n")
            for sample in info[:5]:
                f.write(f"  - {sample['name']} ({sample['size']} bytes)\n")
        f.write("\n")
