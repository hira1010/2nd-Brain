"""Refactor manga prompt markdown files using a common template."""

import argparse
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterator, Optional, Set, Tuple

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

import manga_config
import manga_utils
from manga_core.file_handler import FileHandler
from manga_core.models import MangaEpisode
from manga_core.template_manager import TemplateManager

logger = manga_utils.setup_logger("smart_refactor")

DEFAULT_CATEGORY = "Uncategorized"
TEMPLATE_NAME = "manga_prompt.md"
DEFAULT_DIALOGUES: Dict[str, str] = {
    "Intro": "Dialogue Intro",
    "Teach": "Dialogue Teach",
    "Desc": "Dialogue Desc",
    "Action": "Dialogue Action",
}


class MangaRefactorer:
    """Handle prompt refactoring for one file or a batch of files."""

    def __init__(self, dry_run: bool = False) -> None:
        self.dry_run = dry_run
        self.template_manager = TemplateManager(manga_config.TEMPLATES_DIR)
        self.target_leaf_dirs: Set[str] = {
            Path(target).name for target in manga_config.TARGET_DIRS
        }

    def process_file(self, file_path: Path) -> bool:
        """Refactor a single markdown file and return success state."""
        path = Path(file_path)
        logger.info("Processing: %s", path)

        content = FileHandler.read_file(path)
        if not content:
            logger.error("File content is empty or unreadable: %s", path)
            return False

        try:
            episode = self._build_episode(path, content)
            extracted_dialogues = manga_utils.get_dialogues(
                content, episode.title, episode.desc
            )
            dialogues = {**DEFAULT_DIALOGUES, **extracted_dialogues}
            new_content = self._generate_content(episode, dialogues)
        except Exception as exc:
            logger.error("Error preparing refactor for %s: %s", path, exc)
            return False

        if not new_content:
            logger.error("Failed to generate content for %s", path)
            return False

        if self.dry_run:
            logger.info(
                "[DRY-RUN] Would update %s (No.%s %s)",
                path,
                episode.no,
                episode.title,
            )
            return True

        success = FileHandler.write_file(path, new_content)
        if success:
            logger.info("Successfully refactored: %s", path)
        else:
            logger.error("Failed to write to %s", path)
        return success

    def _build_episode(self, path: Path, content: str) -> MangaEpisode:
        info = manga_utils.extract_info_from_md(content)
        return MangaEpisode(
            no=info.get("no", "00"),
            title=info.get("title", "Unknown"),
            desc=info.get("desc", ""),
            category=self._resolve_category(info.get("category"), path.parent.name),
        )

    def _resolve_category(
        self, extracted_category: Optional[str], parent_dir_name: str
    ) -> str:
        if parent_dir_name in self.target_leaf_dirs:
            return parent_dir_name
        return extracted_category or DEFAULT_CATEGORY

    def _generate_content(
        self, episode: MangaEpisode, dialogues: Dict[str, str]
    ) -> Optional[str]:
        """Generate markdown from the configured template."""
        template_content = self.template_manager.load_template(TEMPLATE_NAME)
        if not template_content:
            return None

        scene = random.choice(manga_config.SCENES)
        try:
            return template_content.format(
                NO=episode.no,
                NO_CLEAN=episode.no.lstrip("0") or "0",
                TITLE=episode.title,
                DESC=episode.desc,
                CATEGORY=episode.category,
                SCENE=scene,
                DIALOGUE_INTRO=dialogues["Intro"],
                DIALOGUE_TEACH=dialogues["Teach"],
                DIALOGUE_DESC=dialogues["Desc"],
                DIALOGUE_ACTION=dialogues["Action"],
                TODAY=datetime.now().strftime("%Y-%m-%d"),
            )
        except KeyError as exc:
            logger.error("Template placeholder missing: %s", exc)
            return None

    def iter_target_files(self) -> Iterator[Path]:
        """Yield markdown files from configured target directories."""
        for subdir in manga_config.TARGET_DIRS:
            target_dir = manga_config.BASE_DIR / subdir
            if not target_dir.exists():
                logger.warning("Directory not found: %s", target_dir)
                continue

            logger.info("Scanning directory: %s", subdir)
            for item in sorted(target_dir.iterdir()):
                if item.is_file() and item.suffix.lower() == ".md":
                    yield item

    def run_all(self) -> Tuple[int, int]:
        """Process all configured markdown files and return (total, success)."""
        total_count = 0
        success_count = 0

        for file_path in self.iter_target_files():
            total_count += 1
            if self.process_file(file_path):
                success_count += 1

        logger.info(
            "Batch processing complete. Total: %s, Success: %s",
            total_count,
            success_count,
        )
        return total_count, success_count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smart refactor manga prompts")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--target", help="Specific file to process")
    mode.add_argument(
        "--all", action="store_true", help="Process all files in target directories"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Show changes without writing"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    refactorer = MangaRefactorer(dry_run=args.dry_run)

    if args.target:
        return 0 if refactorer.process_file(Path(args.target)) else 1

    total, success = refactorer.run_all()
    return 0 if total == success else 1


if __name__ == "__main__":
    raise SystemExit(main())
