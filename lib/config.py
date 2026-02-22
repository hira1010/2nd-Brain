import os
from pathlib import Path


def get_project_root() -> Path:
    """Find the project root by looking for SOUL.md or .git."""
    current = Path(__file__).resolve().parent
    for parent in [current] + list(current.parents):
        if (parent / "SOUL.md").exists() or (parent / ".git").exists():
            return parent
    return current.parent


def get_desktop_dir() -> Path:
    """Resolve Desktop path in a cross-machine friendly way."""
    user_profile = os.environ.get("USERPROFILE")
    if user_profile:
        return Path(user_profile) / "Desktop"
    return Path.home() / "Desktop"


ROOT_DIR = get_project_root()
DESKTOP_DIR = get_desktop_dir()

# General directories
SYSTEM_DIR = ROOT_DIR / "18_システム"
SCRIPTS_DIR = ROOT_DIR / "scripts"
MANGA_DIR = ROOT_DIR / "18_レミ投資漫画"

# Specific directories
DIET_DIR = ROOT_DIR / "01_ダイエット"
STOCKS_DIR = ROOT_DIR / "07_株"
SYSTEM_SCRIPTS_DIR = ROOT_DIR / "_system_scripts"

# File naming conventions
DIET_RECORD_FILE = DIET_DIR / "記録.md"
DIVIDEND_RECORD_FILE = STOCKS_DIR / "配当金・資産推移.md"
CHAR_PROMPT_PATTERN = "**/*プロンプト.md"
SELECTION_LIST_FILE = MANGA_DIR / "05_設定" / "初心者向け連載30選.md"

# API and Sheets
CREDENTIALS_FILE = ROOT_DIR / "credentials.json"
DIET_SHEET_ID = "1-5kRLKDWkEHd7BKwXqnft0_fISJ4KnDXLf1CAGEKHyc"
ASSETS_SHEET_ID = "1lnN_z84DLknNWbQX0YWzHiyn5Ea_Hue9TbxQeHSe3HA"

DEFAULT_ENCODING = "utf-8"
