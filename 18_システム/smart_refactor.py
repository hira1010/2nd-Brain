"""
Smart Refactoring Script.
Updates manga prompt files to the latest template and character settings.
Refactored to use a class-based structure for better maintainability (User Request: Feature unchanged).
"""

import os
import sys
import random
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List

# Add current directory to path to ensure imports work if run from elsewhere
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import manga_config
import manga_utils

logger = manga_utils.setup_logger("smart_refactor")

class MangaRefactorer:
    """
    Handles the refactoring process for manga prompt files.
    """

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run

    def process_file(self, file_path: str) -> bool:
        """
        Refactors a single file. Returns True if successful.
        """
        path = Path(file_path)
        logger.info(f"Processing: {path}")

        try:
            content = self._read_file(path)
            if not content:
                return False

            # Extract Information
            info = manga_utils.extract_info_from_md(content)
            
            # Auto-detect category from parent folder if possible
            parent_dir_name = path.parent.name
            if parent_dir_name in manga_config.TARGET_DIRS:
                info['category'] = parent_dir_name
            elif 'category' not in info or not info['category']:
                info['category'] = "Uncategorized"

            # Get Dialogues (Preserves existing or uses defaults)
            dialogues = manga_utils.get_dialogues(content, info['title'], info['desc'])

            # Generate New Content
            new_content = self._generate_content(info, dialogues)

            # Write or Log
            if self.dry_run:
                logger.info(f"[DRY-RUN] Would update {path} (No.{info['no']} {info['title']})")
                logger.debug(f"Preview:\n{new_content[:200]}...")
            else:
                self._write_file(path, new_content)
                logger.info(f"Successfully refactored: {path}")
            
            return True

        except Exception as e:
            logger.error(f"Error processing {path}: {e}")
            return False

    def _read_file(self, path: Path) -> Optional[str]:
        try:
            # Modern Python 3 defaults to utf-8, but explicit is better
            return path.read_text(encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to read file {path}: {e}")
            return None

    def _write_file(self, path: Path, content: str):
        path.write_text(content, encoding="utf-8")

    def _generate_content(self, info: Dict[str, str], dialogues: Dict[str, str]) -> str:
        """
        Generates the full markdown content using the template.
        """
        # Select a random scene for variety
        scene = random.choice(manga_config.SCENES)
        
        # Get safe title for filenames/internal logic if needed (unused in template but good practice)
        # title_safe = manga_utils.get_safe_filename(info['title']) 
        
        # Format the template
        # Note: Using CHARACTER_SETTINGS_EN from config. 
        # If the original code used 'CHARACTER_SETTINGS', it likely meant this one or a missing one.
        # We assume EN is correct for this context.
        return manga_config.TEMPLATE.format(
            NO=info['no'],
            TITLE=info['title'],
            DESC=info['desc'],
            CATEGORY=info['category'],
            CHARACTER_SETTINGS=manga_config.CHARACTER_SETTINGS_EN,
            WIDTH=manga_config.IMAGE_WIDTH,
            HEIGHT=manga_config.IMAGE_HEIGHT,
            SCENE=scene,
            DIALOGUE_INTRO=dialogues["Intro"],
            DIALOGUE_TEACH=dialogues["Teach"],
            DIALOGUE_DESC=dialogues["Desc"],
            DIALOGUE_ACTION=dialogues["Action"],
            TODAY=datetime.now().strftime('%Y-%m-%d')
        )

    def run_all(self):
        """
        Processes all files in the target directories defined in config.
        """
        total_count = 0
        success_count = 0
        
        for subdir in manga_config.TARGET_DIRS:
            # Construct path using the BASE_DIR from config
            target_dir = manga_config.BASE_DIR / subdir
            
            if not target_dir.exists():
                logger.warning(f"Directory not found: {target_dir}")
                continue
                
            logger.info(f"Scanning directory: {subdir}")
            for item in target_dir.iterdir():
                if item.is_file() and item.suffix.lower() == ".md":
                    if self.process_file(str(item)):
                        success_count += 1
                    total_count += 1
        
        logger.info(f"Batch processing complete. Total: {total_count}, Success: {success_count}")

def main():
    parser = argparse.ArgumentParser(description="Smart refactor manga prompts")
    parser.add_argument("--target", help="Specific file to process")
    parser.add_argument("--all", action="store_true", help="Process all files in target directories")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be changed without writing")
    args = parser.parse_args()
    
    refactorer = MangaRefactorer(dry_run=args.dry_run)
    
    if args.target:
        refactorer.process_file(args.target)
    elif args.all:
        refactorer.run_all()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
