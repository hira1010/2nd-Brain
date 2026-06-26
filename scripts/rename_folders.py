# -*- coding: utf-8 -*-
import os
import re
import sys
import subprocess
from pathlib import Path

# 文字コードをUTF-8に設定
sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent

def rename_folders():
    print("--- フォルダのナンバリング自動整理を開始（PowerShell版） ---")
    
    # ワークスペース直下のファイル・フォルダ一覧を取得
    items = sorted(os.listdir(ROOT_DIR))
    
    # 「数値_名前」の形式になっているフォルダを抽出
    numbered_folders = []
    pattern = re.compile(r"^(\d+)_(.+)$")
    
    for item in items:
        path = ROOT_DIR / item
        if path.is_dir() and pattern.match(item):
            match = pattern.match(item)
            original_num = int(match.group(1))
            name = match.group(2)
            numbered_folders.append((original_num, name, item))
            
    # 元の番号順に正しく並べ替え
    numbered_folders.sort(key=lambda x: x[0])
    
    # 01 から順に隙間なく名前を変更
    game_folder_new_num = None
    
    for i, (orig_num, name, orig_name) in enumerate(numbered_folders):
        new_num_str = f"{i+1:02d}"
        new_name = f"{new_num_str}_{name}"
        
        # 「ゲーム制作」フォルダの新しい番号を記憶しておく（後の設定変更用）
        if "ゲーム制作" in name:
            game_folder_new_num = new_num_str
            
        if orig_name != new_name:
            orig_path = ROOT_DIR / orig_name
            new_path = ROOT_DIR / new_name
            print(f"名前変更: {orig_name} -> {new_name}")
            
            # Windows標準のPowerShellコマンドを呼び出して強制的に名前を変更します
            cmd = f'[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; Rename-Item -Path "{orig_path}" -NewName "{new_name}"'
            res = subprocess.run(
                ["powershell", "-Command", cmd],
                capture_output=True,
                text=True,
                encoding="utf-8",
                shell=True
            )
            
            # 失敗した場合はエラーを出力
            if res.returncode != 0:
                print(f"[エラー] {orig_name} の名前変更に失敗しました: {res.stderr.strip()}")
                sys.exit(1)
            
    # 2. 健康診断プログラム（scripts/antigravity_check.py）のパス設定を自動更新
    if game_folder_new_num:
        check_script_path = ROOT_DIR / "scripts" / "antigravity_check.py"
        if check_script_path.exists():
            with open(check_script_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            new_define = f'"RENPY": ROOT_DIR / "{game_folder_new_num}_ゲーム制作" / "16_RenPy"'
            
            # 正規表現で「"RENPY": ROOT_DIR / "数字_ゲーム制作" / "16_RenPy"」の部分を置換
            updated_content = re.sub(
                r'"RENPY":\s*ROOT_DIR\s*/\s*"\d+_ゲーム制作"\s*/\s*"16_RenPy"',
                new_define,
                content
            )
            
            if content != updated_content:
                with open(check_script_path, "w", encoding="utf-8") as f:
                    f.write(updated_content)
                print(f"[更新] 検証プログラム内のパスを {game_folder_new_num}_ゲーム制作 に更新しました。")

    print("--- フォルダのナンバリング自動整理が完了しました ---")

if __name__ == "__main__":
    rename_folders()
