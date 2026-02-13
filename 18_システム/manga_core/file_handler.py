import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

class FileHandler:
    """
    Handles file I/O operations with robust error handling.
    """
    
    @staticmethod
    def read_file(path: Path) -> Optional[str]:
        """
        Reads a file safely, enforcing utf-8.
        """
        try:
            return path.read_text(encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to read file {path}: {e}")
            return None

    @staticmethod
    def write_file(path: Path, content: str) -> bool:
        """
        Writes content to a file safely.
        """
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            return True
        except Exception as e:
            logger.error(f"Failed to write file {path}: {e}")
            return False
