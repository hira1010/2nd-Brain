"""
Smart Refactoring Script.
Updates manga prompt files to the latest high-quality template.
Refactored to use modular `manga_core` package.
"""

import os
import sys
import argparse
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import manga_config
import manga_utils
from manga_core.file_handler import FileHandler
from manga_core.template_manager import TemplateManager
from manga_core.models import MangaEpisode

logger = manga_utils.setup_logger("smart_refactor")
DEFAULT_CATEGORY = "Uncategorized"

class MangaRefactorer:
    """
    Handles the refactoring process using the new core modules.
    """

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.template_manager = TemplateManager(manga_config.TEMPLATES_DIR)

    def process_file(self, file_path: str) -> bool:
        """
        Refactors a single file. Returns True if successful.
        """
        path = Path(file_path)
        logger.info(f"Processing: {path}")

        try:
            content = FileHandler.read_file(path)
            if not content:
                return False

            # Extract Information
            info = manga_utils.extract_info_from_md(content)
            
            # Auto-detect category
            parent_dir_name = path.parent.name
            info["category"] = self._resolve_category(info, parent_dir_name)

            # Get Dialogues
            dialogues = manga_utils.get_dialogues(content, info['title'], info['desc'])

            # Generate New Content
            new_content = self._generate_content(info, dialogues)

            if not new_content:
                logger.error("Failed to generate content.")
                return False

            # Write or Log
            if self.dry_run:
                logger.info(f"[DRY-RUN] Would update {path} (No.{info['no']} {info['title']})")
                logger.debug(f"Preview:\n{new_content[:500]}...")
            else:
                success = FileHandler.write_file(path, new_content)
                if success:
                    logger.info(f"Successfully refactored: {path}")
                else:
                    logger.error(f"Failed to write to {path}")
            
            return True

        except Exception as e:
            logger.error(f"Error processing {path}: {e}")
            return False

    def _resolve_category(self, info: Dict[str, str], parent_dir_name: str) -> str:
        # Check against config target dirs, allowing partial matches key logic if needed
        # For simple check:
        for target in manga_config.TARGET_DIRS:
            if parent_dir_name in target:
                return parent_dir_name
        return info.get("category") or DEFAULT_CATEGORY

    def _generate_content(self, info: Dict[str, str], dialogues: Dict[str, str]) -> Optional[str]:
        """
        Generates the full markdown content using the external template.
        """
        template_content = self.template_manager.load_template("manga_prompt.md")
        if not template_content:
            return None

        # Select a random scene
        scene = random.choice(manga_config.SCENES)
        
        # Prepare template variables
        # Note: Visual locks are now hardcoded in the template for strict consistency,
        # so we don't need to inject CHARACTER_SETTINGS anymore.
        
        return template_content.format(
            NO=info['no'],
            # Clean NO for filenames (remove leading zeros if needed, or keep as is)
            NO_CLEAN=info['no'].lstrip('0') or '0', 
            TITLE=info['title'],
            DESC=info['desc'],
            CATEGORY=info['category'],
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

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smart refactor manga prompts")
    parser.add_argument("--target", help="Specific file to process")
    parser.add_argument("--all", action="store_true", help="Process all files in target directories")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be changed without writing")
    return parser.parse_args()


def main():
    args = parse_args()
    
    refactorer = MangaRefactorer(dry_run=args.dry_run)
    
    if args.target:
        refactorer.process_file(args.target)
    elif args.all:
        refactorer.run_all()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
