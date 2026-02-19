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

SYSTEM_DIR = ROOT_DIR / "18_システム"
SCRIPTS_DIR = ROOT_DIR / "scripts"
DIET_DIR = ROOT_DIR / "01_ダイエット"
STOCKS_DIR = ROOT_DIR / "07_株"
MANGA_DIR = ROOT_DIR / "18_レミ投資漫画"

DIET_SHEET_ID = "1-5kRLKDWkEHd7BKwXqnft0_fISJ4KnDXLf1CAGEKHyc"
ASSETS_SHEET_ID = "1lnN_z84DLknNWbQX0YWzHiyn5Ea_Hue9TbxQeHSe3HA"

DEFAULT_ENCODING = "utf-8"
