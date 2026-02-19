#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📁 エピソード整理スクリプト (Refactored)
"""

import sys
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.append(str(Path(__file__).resolve().parent.parent))

import re
import shutil
import glob
from lib import config, utils

# 初期化
logger = utils.initialize_script("organize_selection")

# 章番号とフォルダ名のマッピング
CHAPTER_MAP = {
    1: "01_現状把握と脱労働",
    2: "02_投資の魔法と基礎",
    3: "03_実践と準備",
    4: "04_継続の技術",
    5: "05_投資の果実と自由"
}

# 同名回避のためのキーワード
TITLE_KEYWORDS = {
    1: "配当貴族",
}

def parse_selection_list():
    content = utils.FileIO.read_text(config.SELECTION_LIST_FILE)
    if content is None: return []
    
    selections = []
    current_chapter = 0
    
    for line in content.splitlines():
        # Chapter検出
        m_chap = re.match(r"^## 第(\d+)章", line)
        if m_chap:
            current_chapter = int(m_chap.group(1))
            continue
        
        # テーブル行検出
        if not line.strip().startswith('|'):
            continue
        
        parts = [p.strip() for p in line.strip().split('|')]
        if len(parts) < 4: continue
        
        no_str = parts[1]
        title_str = parts[2]
        
        if not no_str.isdigit():
            continue
            
        no = int(no_str)
        title = title_str.replace('*', '').strip()
        
        selections.append({
            'chapter': current_chapter,
            'no': no,
            'title': title
        })
    return selections

def main():
    selections = parse_selection_list()
    logger.info("Loaded %d episodes from selection list.", len(selections))
    
    # ターゲットディレクトリの作成
    for folder in CHAPTER_MAP.values():
        path = config.MANGA_DIR / folder
        path.mkdir(parents=True, exist_ok=True)

    files_moved = 0
    for item in selections:
        folder_name = CHAPTER_MAP.get(item['chapter'])
        if not folder_name:
            logger.warning("Unknown chapter %d for No.%d", item['chapter'], item['no'])
            continue
            
        target_dir = config.MANGA_DIR / folder_name
        pattern = f"No{item['no']:02d}_*プロンプト.md"
        candidates = glob.glob(str(config.MANGA_DIR / "**" / pattern), recursive=True)
        
        # フィルタリング
        valid_candidates = []
        keyword = TITLE_KEYWORDS.get(item['no'])
        
        for p in candidates:
            if keyword and keyword not in Path(p).name:
                continue
            valid_candidates.append(p)
            
        if not valid_candidates:
            logger.debug("No.%d (%s) - File NOT FOUND.", item['no'], item['title'])
            continue
            
        src_path = valid_candidates[0]
        if len(valid_candidates) > 1:
            for vc in valid_candidates:
                if item['title'] in Path(vc).name:
                    src_path = vc
                    break
        
        src_path = Path(src_path)
        dest_path = target_dir / src_path.name
        
        if src_path.resolve() == dest_path.resolve():
            logger.debug("OK (Already in place): %s", src_path.name)
            continue
            
        try:
            shutil.move(str(src_path), str(dest_path))
            logger.info("MOVED: %s -> %s", src_path.name, folder_name)
            files_moved += 1
        except Exception as e:
            logger.error("ERROR moving %s: %s", src_path.name, e)

    logger.info("Operation Complete. Moved %d files.", files_moved)

if __name__ == "__main__":
    main()
