import os
import shutil

ROOT_DIR = r"c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画"
ARCHIVE_DIR = os.path.join(ROOT_DIR, "99_知識保管庫")

# Folders to move to Archive
TARGET_FOLDERS = [
    "01_投資の基礎知識",
    "02_マインド・哲学",
    "03_戦略・リスク管理",
    "04_未来・テクノロジー"
]

def main():
    if not os.path.exists(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR)
        print(f"Created archive directory: {ARCHIVE_DIR}")
        
    for folder_name in TARGET_FOLDERS:
        src_path = os.path.join(ROOT_DIR, folder_name)
        dest_path = os.path.join(ARCHIVE_DIR, folder_name)
        
        if os.path.exists(src_path):
            try:
                # If destination already exists, we might have a conflict.
                # shutil.move will move the folder INSIDE if dest exists and is a dir, 
                # or rename if it doesn't. We want to be careful.
                # Best to ensure dest parent exists (it does) and dest itself does NOT exist?
                # Or just merge?
                
                # If dest archive folder exists, we should probably merge or rename contents.
                # simple move:
                if os.path.exists(dest_path):
                    print(f"Destination {dest_path} already exists. Merging contents...")
                    # Allow move to merge? No, shutil.move might fail or nest.
                    # Let's use a function to move contents if dir exists.
                    for item in os.listdir(src_path):
                        s = os.path.join(src_path, item)
                        d = os.path.join(dest_path, item)
                        if os.path.exists(d):
                            print(f"  Skipping {item} (already in archive)")
                        else:
                            shutil.move(s, d)
                    # Try to remove empty src dir
                    try:
                        os.rmdir(src_path)
                        print(f"Moved contents and removed source: {folder_name}")
                    except OSError:
                        print(f"Moved contents but source not empty: {folder_name}")
                else:
                    shutil.move(src_path, dest_path)
                    print(f"Moved: {folder_name} -> 99_知識保管庫")
                    
            except Exception as e:
                print(f"Error moving {folder_name}: {e}")
        else:
            print(f"Not found (skipping): {folder_name}")

if __name__ == "__main__":
    main()
