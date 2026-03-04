import io
import logging
import re
import sys
from pathlib import Path
from typing import IO, Any, Optional, Union, cast

from . import config

_LOGGER = logging.getLogger(__name__)
PathLike = Union[str, Path]


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """指定された名前のロガーを作成し、標準出力へのハンドラを設定します。
    
    Args:
        name: ロガーの名前
        level: ログレベル (デフォルト: logging.INFO)
        
    Returns:
        設定済みの logging.Logger オブジェクト
    """
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


def initialize_script(name: str) -> logging.Logger:
    """Windows環境でのUTF-8出力を保証し、ロガーを初期化します。
    
    Args:
        name: 初期化するスクリプトの名前
        
    Returns:
        初期化されたロガーオブジェクト
    """
    if sys.platform == "win32":
        try:
            sys.stdout = cast(IO[str], _ensure_utf8_stream(sys.stdout))
            sys.stderr = cast(IO[str], _ensure_utf8_stream(sys.stderr))
        except Exception as exc:
            _LOGGER.debug("Failed to set UTF-8 encoding for streams: %s", exc)
    return setup_logger(name)


def _ensure_utf8_stream(stream: Any) -> Any:
    """ストリームがUTF-8でない場合、TextIOWrapperでラップして返します。"""
    if hasattr(stream, "buffer") and getattr(stream, "encoding", "").lower() != "utf-8":
        try:
            return io.TextIOWrapper(stream.buffer, encoding="utf-8")
        except (AttributeError, io.UnsupportedOperation):
            return stream
    return stream


class FileIO:
    """UTF-8をデフォルトとした汎用的なファイル入出力ラッパー。"""

    @staticmethod
    def read_text(path: PathLike, encoding: str = config.DEFAULT_ENCODING) -> Optional[str]:
        """ファイルをテキストとして読み込みます。失敗した場合は None を返します。"""
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
        """テキストをファイルに書き込みます。ディレクトリがない場合は自動作成します。"""
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
    """Windowsで不適切な文字を除去した安全なファイル名を返します。"""
    safe_text = re.sub(r"[\\/*?:\"<>|]", "", text)
    safe_text = safe_text.replace(" ", "_").strip()
    return safe_text or "output_file"
