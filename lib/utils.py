import logging
import re
import sys
from pathlib import Path
from typing import Optional, Union

from . import config

_LOGGER = logging.getLogger(__name__)
PathLike = Union[str, Path]


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Create a stdout logger once per logger name."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    handler = logging.StreamHandler(sys.stdout)
    # Windows環境での日本語化防止のため、エンコーディングを指定したいがStreamHandlerは通常sys.stdoutを使う
    # initialize_script で一括設定を行う
    formatter = logging.Formatter("[%(levelname)s] %(name)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False
    return logger


def initialize_script(name: str) -> logging.Logger:
    """Initialize environment for Windows UTF-8 and returns a logger."""
    import io

    if sys.platform == "win32":
        try:
            if hasattr(sys.stdout, "buffer") and getattr(sys.stdout, "encoding", "").lower() != "utf-8":
                sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
            if hasattr(sys.stderr, "buffer") and getattr(sys.stderr, "encoding", "").lower() != "utf-8":
                sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")
        except Exception:
            pass
    return setup_logger(name)


class FileIO:
    """Simple file IO wrapper with UTF-8 defaults and safe errors."""

    @staticmethod
    def read_text(path: PathLike, encoding: str = config.DEFAULT_ENCODING) -> Optional[str]:
        try:
            return Path(path).read_text(encoding=encoding)
        except Exception as exc:
            _LOGGER.error("Failed to read file: %s (%s)", path, exc)
            return None

    @staticmethod
    def write_text(
        path: PathLike,
        content: str,
        encoding: str = config.DEFAULT_ENCODING,
        make_backup: bool = False,
    ) -> bool:
        try:
            target = Path(path)
            if make_backup and target.exists():
                backup = target.with_suffix(target.suffix + ".bak")
                backup.write_bytes(target.read_bytes())

            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding=encoding)
            return True
        except Exception as exc:
            _LOGGER.error("Failed to write file: %s (%s)", path, exc)
            return False


def get_safe_filename(text: str) -> str:
    """Remove unsafe characters for Windows file names."""
    safe_text = re.sub(r"[\\/*?:\"<>|]", "", text)
    safe_text = safe_text.replace(" ", "_").strip()
    return safe_text or "output_file"
