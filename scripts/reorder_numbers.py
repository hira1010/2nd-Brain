import os
import shutil

root = r'C:\Users\hirak\Desktop\2nd-Brain'

# 1. 09_年間お楽しみ を削除
dir_09 = os.path.join(root, '09_年間お楽しみ')
if os.path.exists(dir_09):
    print(f"Deleting: {dir_09}")
    shutil.rmtree(dir_09)

# 2. リネーム計画の定義
# 衝突を避けるために、一度一時的な名前に設定してから最終的な名前に戻す
renames = [
    ('05_Remotion', '04_Remotion'),
    ('06_RPGゲーム成果物', '05_RPGゲーム成果物'),
    ('07_株', '06_株'),
    ('08_節約', '07_節約'),
    ('10_健康', '08_健康'),
    ('12_目標', '09_目標'),
    ('13_ドラマ・漫画テク', '10_ドラマ・漫画テク'),
    ('14_HP作成スキル', '11_HP作成スキル'),
    ('18_システム', '12_システム'),
    ('19_レミ投資漫画', '13_レミ投資漫画'),
    ('20_Pyxel_Godot', '14_Pyxel_Godot'),
    ('21_ComfyUI', '15_ComfyUI'),
    ('22_遺伝子解析', '16_遺伝子解析'),
    ('23_重曹クエン酸', '17_重曹クエン酸'),
    ('25_RPGツクールフォルダ', '18_RPGツクールフォルダ'),
    ('26_プロレスゲーム', '19_プロレスゲーム'),
    ('27_アイAI', '20_アイAI')
]

print("--- Start Renaming ---")

# ステップ1: 一時的な名前にリネーム（衝突回避）
temp_names = []
for src, dst in renames:
    src_path = os.path.join(root, src)
    if os.path.exists(src_path):
        temp_path = src_path + "_temp_cleanup"
        os.rename(src_path, temp_path)
        temp_names.append((temp_path, dst))
    else:
        print(f"Warning: Source not found: {src}")

# ステップ2: 最終的な名前にリネーム
for temp_path, dst in temp_names:
    dst_path = os.path.join(root, dst)
    if os.path.exists(dst_path):
        print(f"Error: Destination already exists: {dst_path}")
    else:
        os.rename(temp_path, dst_path)
        print(f"Renamed to: {dst}")

print("--- Renaming Finished ---")
