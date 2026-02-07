import os
import re
import shutil
import glob

ROOT_DIR = r"c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画"

# Mapping from Chapter Number to Target Folder Name
CHAPTER_MAP = {
    1: "01_現状把握と脱労働",
    2: "02_投資の魔法と基礎",
    3: "03_実践と準備",
    4: "04_継続の技術",
    5: "05_投資の果実と自由"
}

# Specific title mapping for disambiguation (No -> Title Keyword)
# This helps distinguish No.1 配当貴族 vs No.1 投資は最強の武器
TITLE_KEYWORDS = {
    1: "配当貴族",
    # Add others if collisions are expected, but typically No. is unique except for No.1
}

def parse_selection_list():
    selection_file = os.path.join(ROOT_DIR, "05_設定", "初心者向け連載30選.md")
    selections = []
    current_chapter = 0
    
    with open(selection_file, 'r', encoding='utf-8') as f:
        for line in f:
            # Detect Chapter Header
            m_chap = re.match(r"^## 第(\d+)章", line)
            if m_chap:
                current_chapter = int(m_chap.group(1))
                continue
            
            # Detect Table Row: | No | Title | ...
            if not line.strip().startswith('|'):
                continue
            
            parts = [p.strip() for p in line.strip().split('|')]
            if len(parts) < 4: continue
            
            # parts[0] is empty (before first |), parts[1] is No, parts[2] is Title
            no_str = parts[1]
            title_str = parts[2]
            
            if not no_str.isdigit():
                continue
                
            no = int(no_str)
            # clean title **Title** -> Title
            title = title_str.replace('*', '').strip()
            
            selections.append({
                'chapter': current_chapter,
                'no': no,
                'title': title
            })
    return selections

def main():
    selections = parse_selection_list()
    print(f"Loaded {len(selections)} episodes from selection list.")
    
    # Ensure target directories exist
    for folder in CHAPTER_MAP.values():
        path = os.path.join(ROOT_DIR, folder)
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Created directory: {folder}")

    files_moved = 0
    
    for item in selections:
        target_folder_name = CHAPTER_MAP.get(item['chapter'])
        if not target_folder_name:
            print(f"Warning: Unknown chapter {item['chapter']} for No.{item['no']}")
            continue
            
        target_dir = os.path.join(ROOT_DIR, target_folder_name)
        
        # Search for the file
        # Pattern: NoXX_*プロンプト.md
        pattern = f"No{item['no']:02d}_*プロンプト.md"
        # We search specifically to avoid partial matches on numbers (like No10 matching No100)
        # using glob with recursive=True
        candidates = glob.glob(os.path.join(ROOT_DIR, "**", pattern), recursive=True)
        
        # Filter candidates
        valid_candidates = []
        target_keyword = TITLE_KEYWORDS.get(item['no'])
        
        for p in candidates:
            filename = os.path.basename(p)
            # If we have a specific keyword for this No (like 配当貴族), ensure it's in the filename
            if target_keyword:
                if target_keyword not in filename:
                    continue
            valid_candidates.append(p)
            
        if not valid_candidates:
            print(f"Received No.{item['no']} ({item['title']}) - File NOT FOUND.")
            continue
            
        # If multiple, take the one that contains the title from the list if possible, else the first
        src_path = valid_candidates[0]
        if len(valid_candidates) > 1:
            # Try to match the title from the markdown list
            for vc in valid_candidates:
                if item['title'] in os.path.basename(vc):
                    src_path = vc
                    break
        
        fname = os.path.basename(src_path)
        dest_path = os.path.join(target_dir, fname)
        
        # Check if already in place
        if os.path.abspath(src_path) == os.path.abspath(dest_path):
            print(f"OK (Already in place): {fname}")
            continue
            
        try:
            shutil.move(src_path, dest_path)
            print(f"MOVED: {fname} -> {target_folder_name}")
            files_moved += 1
        except Exception as e:
            print(f"ERROR moving {fname}: {e}")

    print(f"\nOperation Complete. Moved {files_moved} files.")

if __name__ == "__main__":
    main()
