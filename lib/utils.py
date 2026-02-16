import logging
import sys
from pathlib import Path
from typing import Optional, Union
from . import config

def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    標準出力にログを出力するロガーをセットアップします。
    日本語が文字化けしないよう、Windows環境でも配慮した設定を行います。
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        # Windowsのコマンドプロンプト等で日本語が正しく表示されるよう、フォーマットを指定
        formatter = logging.Formatter('[%(levelname)s] %(name)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)
    return logger

class FileIO:
    """
    UTF-8を原則とした、堅牢なファイル入出力機能を提供します。
    """
    
    @staticmethod
    def read_text(path: Union[str, Path], encoding: str = config.DEFAULT_ENCODING) -> Optional[str]:
        """ファイルを安全に読み込みます。"""
        try:
            return Path(path).read_text(encoding=encoding)
        except Exception as e:
            logging.error(f"ファイルの読み込みに失敗しました: {path} ({e})")
            return None

    @staticmethod
    def write_text(path: Union[str, Path], content: str, encoding: str = config.DEFAULT_ENCODING) -> bool:
        """ファイルを安全に書き込みます。"""
        try:
            p = Path(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding=encoding)
            return True
        except Exception as e:
            logging.error(f"ファイルの書き出しに失敗しました: {path} ({e})")
            return False

def get_safe_filename(text: str) -> str:
    """不適切な文字を除去した安全なファイル名を返します。"""
    import re
    safe_text = re.sub(r'[\\/*?:"<>|]', "", text)
    safe_text = safe_text.replace(" ", "_").strip()
    return safe_text if safe_text else "output_file"
