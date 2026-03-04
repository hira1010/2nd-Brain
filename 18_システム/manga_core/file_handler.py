import logging
from pathlib import Path
from typing import Optional, Union

logger = logging.getLogger(__name__)
PathLike = Union[str, Path]
DEFAULT_ENCODING = "utf-8"


class FileHandler:
    """
    Handles file I/O operations with robust error handling.
    """
    
    @staticmethod
    def read_file(path: PathLike) -> Optional[str]:
        """
        Reads a file safely, enforcing utf-8.
        """
        target = FileHandler._as_path(path)
        try:
            return target.read_text(encoding=DEFAULT_ENCODING)
        except (OSError, UnicodeError) as e:
            logger.error("Failed to read file %s: %s", target, e)
            return None

    @staticmethod
    def write_file(path: PathLike, content: str) -> bool:
        """
        Writes content to a file safely.
        """
        target = FileHandler._as_path(path)
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding=DEFAULT_ENCODING)
            return True
        except (OSError, UnicodeError) as e:
            logger.error("Failed to write file %s: %s", target, e)
            return False

    @staticmethod
    def _as_path(path: PathLike) -> Path:
        return path if isinstance(path, Path) else Path(path)
