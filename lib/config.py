import os
from pathlib import Path

def get_project_root() -> Path:
    """
    プロジェクトのルートディレクトリ（SOUL.md または .git が存在する場所）を動的に検索します。
    """
    current = Path(__file__).resolve().parent
    for parent in [current] + list(current.parents):
        if (parent / "SOUL.md").exists() or (parent / ".git").exists():
            return parent
    # 見つからない場合は現在のパスの2つ上（libの親等）をデフォルトとする
    return current.parent

# 定数定義
ROOT_DIR = get_project_root()

# 各種主要ディレクトリ
SYSTEM_DIR = ROOT_DIR / "18_システム"
SCRIPTS_DIR = ROOT_DIR / "scripts"
DIET_DIR = ROOT_DIR / "01_ダイエット"
STOCKS_DIR = ROOT_DIR / "07_株"
MANGA_DIR = ROOT_DIR / "18_レミ投資漫画"

# スプレッドシート関連
DIET_SHEET_ID = "1-5kRLKDWkEHd7BKwXqnft0_fISJ4KnDXLf1CAGEKHyc"
ASSETS_SHEET_ID = "1lnN_z84DLknNWbQX0YWzHiyn5Ea_Hue9TbxQeHSe3HA"

# 文字コード設定
DEFAULT_ENCODING = "utf-8"
