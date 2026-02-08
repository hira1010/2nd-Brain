"""
スマート・リファクタリング・スクリプト
漫画プロンプトファイルを最新のテンプレートとキャラクター設定に更新します。
manga_config と manga_utils を使用する新バージョンです。
"""

import os
import random
import argparse
from datetime import datetime
from pathlib import Path

# 共通基盤のインポート
import manga_config
import manga_utils

logger = manga_utils.setup_logger("smart_refactor")

def process_single_file(file_path: str, dry_run: bool = False):
    """
    単一のファイルをリファクタリング
    """
    logger.info(f"Processing: {file_path}")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 情報抽出
        info = manga_utils.extract_info_from_md(content)
        dialogues = manga_utils.get_dialogues(content, info['title'], info['desc'])
        
        # カテゴリーの自動判別（パスから）
        parent_dir = os.path.basename(os.path.dirname(file_path))
        if parent_dir in manga_config.TARGET_DIRS:
            info['category'] = parent_dir
        
        # 安全なファイル名の生成
        title_safe = manga_utils.get_safe_filename(info['title'])
        
        # ランダムなシーンの選択
        scene = random.choice(manga_config.SCENES)
        
        # 新しいコンテンツの生成
        new_content = manga_config.TEMPLATE.format(
            NO=info['no'],
            TITLE=info['title'],
            DESC=info['desc'],
            CATEGORY=info['category'],
            CHARACTER_SETTINGS=manga_config.CHARACTER_SETTINGS,
            WIDTH=manga_config.IMAGE_WIDTH,
            HEIGHT=manga_config.IMAGE_HEIGHT,
            SCENE=scene,
            DIALOGUE_INTRO=dialogues["Intro"],
            DIALOGUE_TEACH=dialogues["Teach"],
            DIALOGUE_DESC=dialogues["Desc"],
            DIALOGUE_ACTION=dialogues["Action"],
            TITLE_SAFE=title_safe,
            TODAY=datetime.now().strftime('%Y-%m-%d')
        )
        
        if dry_run:
            logger.info(f"[DRY-RUN] Would update: {file_path}")
            # 最初の数行だけ表示
            logger.info(f"Summary: No.{info['no']} {info['title']}")
        else:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            logger.info(f"Successfully refactored: {file_path}")
            
    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Smart refactor manga prompts")
    parser.add_argument("--target", help="Specific file to process")
    parser.add_argument("--all", action="store_true", help="Process all files in target directories")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be changed without writing")
    args = parser.parse_args()
    
    if args.target:
        process_single_file(args.target, args.dry_run)
    elif args.all:
        total_count = 0
        for subdir in manga_config.TARGET_DIRS:
            dir_path = manga_config.BASE_DIR / subdir
            if not dir_path.exists():
                logger.warning(f"Directory not found: {dir_path}")
                continue
            
            for filename in os.listdir(dir_path):
                if filename.endswith(".md"):
                    process_single_file(str(dir_path / filename), args.dry_run)
                    total_count += 1
        
        logger.info(f"Total processed: {total_count}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
