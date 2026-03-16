import os
import shutil

root = r'C:\Users\hirak\Desktop\2nd-Brain'
src18 = os.path.join(root, '18_RPGツクールフォルダ')
dst05 = os.path.join(root, '05_RPGゲーム成果物')
final05 = os.path.join(root, '05_RPG制作')

# 1. 18の内容を05へ移動
print(f"Merging {src18} into {dst05}...")
if os.path.exists(src18) and os.path.exists(dst05):
    for item in os.listdir(src18):
        s = os.path.join(src18, item)
        d = os.path.join(dst05, item)
        
        # ディレクトリの場合は中身をマージ、ファイルの場合は上書き
        if os.path.isdir(s):
            if os.path.exists(d):
                for subitem in os.listdir(s):
                    shutil.move(os.path.join(s, subitem), os.path.join(d, subitem))
                os.rmdir(s) # 空になったはずなので削除
            else:
                shutil.move(s, d)
        else:
            if os.path.exists(d):
                os.remove(d)
            shutil.move(s, d)
        print(f" Moved: {item}")
    
    # 元フォルダの削除
    try:
        shutil.rmtree(src18)
        print(f"Deleted source directory: {src18}")
    except Exception as e:
        print(f"Could not delete {src18} (it might be in use): {e}")

# 2. 05をリネーム
if os.path.exists(dst05):
    os.rename(dst05, final05)
    print(f"Renamed {dst05} to {final05}")

# 3. 後続の番号を繰り上げ
renames = [
    ('19_プロレスゲーム', '18_プロレスゲーム'),
    ('20_アイAI', '19_アイAI')
]

for src, dst in renames:
    src_path = os.path.join(root, src)
    dst_path = os.path.join(root, dst)
    if os.path.exists(src_path):
        # 衝突を避けるために一度 temp を経由
        temp_path = src_path + "_temp_merge"
        os.rename(src_path, temp_path)
        os.rename(temp_path, dst_path)
        print(f"Moved and renamed: {src} -> {dst}")

print("Process finished.")
