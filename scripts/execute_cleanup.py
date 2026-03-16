import os
import shutil

root = r'C:\Users\hirak\Desktop\2nd-Brain'

# 削除対象 (NFD 形式の空フォルダ)
# 直接文字列を扱うと環境によって正規化される可能性があるため注意
dirs_to_delete = [
    'note作成用プロンプト', # NFD
    'ポスト作成プロンプト'  # NFD
]

# リネーム対象 (インデックス番号の重複解消)
renames = {
    '18_レミ投資漫画': '19_レミ投資漫画',
    '20_Pyxel': '24_Pyxel',
    '21_プロレスゲーム': '26_プロレスゲーム'
}

print("--- Data Cleanup Started ---")

for d in dirs_to_delete:
    path = os.path.join(root, d)
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
            print(f"Deleted: {d}")
        except Exception as e:
            print(f"Error deleting {d}: {e}")
    else:
        print(f"Not found (already deleted?): {d}")

for src, dst in renames.items():
    src_path = os.path.join(root, src)
    dst_path = os.path.join(root, dst)
    if os.path.exists(src_path):
        try:
            os.rename(src_path, dst_path)
            print(f"Renamed: {src} -> {dst}")
        except Exception as e:
            print(f"Error renaming {src}: {e}")
    else:
        print(f"Source not found: {src}")

print("--- Cleanup Finished ---")
