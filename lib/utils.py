import logging
import sys
from pathlib import Path
from typing import Optional, Union

from . import config


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Create a stdout logger once per logger name."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("[%(levelname)s] %(name)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False
    return logger


class FileIO:
    """Simple file IO wrapper with UTF-8 defaults and safe errors."""

    @staticmethod
    def read_text(path: Union[str, Path], encoding: str = config.DEFAULT_ENCODING) -> Optional[str]:
        try:
            return Path(path).read_text(encoding=encoding)
        except Exception as exc:
            logging.getLogger(__name__).error("Failed to read file: %s (%s)", path, exc)
            return None

    @staticmethod
    def write_text(path: Union[str, Path], content: str, encoding: str = config.DEFAULT_ENCODING) -> bool:
        try:
            target = Path(path)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding=encoding)
            return True
        except Exception as exc:
            logging.getLogger(__name__).error("Failed to write file: %s (%s)", path, exc)
            return False


def get_safe_filename(text: str) -> str:
    """Remove unsafe characters for Windows file names."""
    import re

    safe_text = re.sub(r"[\\/*?:\"<>|]", "", text)
    safe_text = safe_text.replace(" ", "_").strip()
    return safe_text or "output_file"
