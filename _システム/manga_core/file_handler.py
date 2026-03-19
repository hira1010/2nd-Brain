import logging
from pathlib import Path
from typing import Optional, Union

from lib.utils import FileIO

logger = logging.getLogger(__name__)
PathLike = Union[str, Path]


class FileHandler:
    """
    lib.utils.FileIO をラップした、漫画システム用ファイル操作クラス。
    """
    
    @staticmethod
    def read_file(path: PathLike) -> Optional[str]:
        """
        ファイルをテキストとして安全に読み込みます。
        """
        return FileIO.read_text(path)

    @staticmethod
    def write_file(path: PathLike, content: str) -> bool:
        """
        コンテンツをファイルに安全に書き込みます。
        """
        return FileIO.write_text(path, content)
