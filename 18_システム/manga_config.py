"""
Manga production system configuration file.
Defines constants and paths for the manga prompt generation system.
"""

from pathlib import Path
from typing import List, Dict

# ==========================================
# Path Considerations
# ==========================================
# Base directory for the manga project
BASE_DIR = Path(r"c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画")

# Directory containing external templates
TEMPLATES_DIR = Path(__file__).parent / "templates"

# Target directories to process
TARGET_DIRS: List[str] = [
    "030プロンプト/01_現状把握と脱労働",
    "030プロンプト/02_投資の魔法と基礎",
    "030プロンプト/03_実践と準備",
    "030プロンプト/04_継続の技術",
    "030プロンプト/05_投資の果実と自由",
    "101プロンプト/01_投資の基礎知識",
    "101プロンプト/02_マインド・哲学",
    "101プロンプト/03_戦略・リスク管理",
    "101プロンプト/04_未来・テクノロジー"
]

# ==========================================
# Visual Settings
# ==========================================
# High Quality Vertical A4 Ratio (Approximate pixels for 300dpi A4)
# Note: The prompt uses "Vertical Portrait A4 Ratio" textual tag, 
# but these dimensions might be used for other programatic needs.
IMAGE_WIDTH: int = 2480
IMAGE_HEIGHT: int = 3508

# Scene variations (Background options)
SCENES: List[str] = [
    "Modern high-rise office with panoramic city view",
    "Stylish cafe with warm lighting and wooden furniture",
    "Luxurious lounge bar with night city view",
    "Bright meeting room with a large whiteboard",
    "Quiet library or study room with bookshelves"
]

# Character visual settings (visual lock) - Kept for reference, 
# though the template now strictly enforces them inline.
CHARACTER_SETTINGS_EN: str = """## Character Settings (Global)
### Remi - Visual Lock
- **Hair**: Waist-length straight silver hair, center-parted bangs
- **Eyes**: Sharp ruby red eyes, long eyelashes
- **Outfit**: Deep crimson business blazer (red buttons), white shirt, **NO gloves**
- **Figure**: Slim, tall, adult woman, elegant posture
- **Expression**: Intelligent, confident smile, calm

### Yuto - Visual Lock
- **Hair**: Short black hair, neat style
- **Eyes**: Black eyes, pure expression
- **Outfit**: Traditional black gakuran (school uniform), stand-up collar, **NO gloves**
- **Figure**: Standard teenage boy build
- **Expression**: Curious, earnest learning posture
"""
