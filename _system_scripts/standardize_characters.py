#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎭 登場人物設定標準化スクリプト (Refactored)
"""

import sys
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.append(str(Path(__file__).resolve().parent.parent))

import re
import glob
from lib import config, utils

# 初期化
logger = utils.initialize_script("standardize_characters")

# 標準化されたキャラクターブロック
NEW_CHARS = """### Characters:
- Remi: (Crimson RED blazer, Black lace top). (Silky SILVER hair), (RED eyes). NO GLOVES. (ONLY ONE Remi per panel).
- Yuto: (Traditional SOLID BLACK Gakuran school uniform, gold buttons). (Short Black hair). BARE HANDS. (ONLY ONE Yuto per panel).
- Ai: (Navy blue school blazer, Red necktie, Beige cardigan). (Short BLACK hair), (Amber eyes). NO GLOVES. (ONLY ONE Ai per panel).
- Hibiki: (Long straight BLACK hair), (BROWN eyes). (Adult woman).
- Suguru: (Messy DARK GREEN hair), (BLUE eyes). (Brown hoodie or Gakuran).
- Manager: (Short WHITE hair, Smiling slit eyes). (White shirt, Black apron, Black bow tie)."""

# 正規表現パターン
PATTERN = r"### Characters:\s*\n\s*- Remi:.*?\n\s*- Yuto:.*?\n\s*- Ai:.*?\n\s*- Hibiki:.*?\n\s*- Suguru:.*?\n\s*- Manager:.*?(?=(\n\s*\n|\n\s*\[))"

def main():
    logger.info("Scanning files in %s...", config.MANGA_DIR)
    # config.CHAR_PROMPT_PATTERN は "**/*プロンプト.md"
    pattern_path = str(config.MANGA_DIR / config.CHAR_PROMPT_PATTERN)
    files = glob.glob(pattern_path, recursive=True)
    logger.info("Found %d files.", len(files))

    updated_files = 0
    for filepath in files:
        try:
            content = utils.FileIO.read_text(filepath)
            if content is None: continue
            
            # 置換実行
            new_content, n = re.subn(PATTERN, NEW_CHARS, content, flags=re.IGNORECASE | re.DOTALL)
            
            if n > 0 and new_content != content:
                if utils.FileIO.write_text(filepath, new_content):
                    logger.info("Updated: %s (%d sections updated)", Path(filepath).name, n)
                    updated_files += 1
            elif n == 0:
                logger.debug("Skipped (No match): %s", Path(filepath).name)
        except Exception as e:
            logger.error("Error processing %s: %s", filepath, e)

    logger.info("Summary: Updated %d files out of %d.", updated_files, len(files))

if __name__ == "__main__":
    main()
