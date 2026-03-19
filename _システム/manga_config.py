"""Configuration for manga prompt refactoring scripts."""

import os
import sys
from pathlib import Path
from typing import List

# Ensure project root is importable so `from lib import config` works.
LIB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lib"
)
PROJECT_ROOT = os.path.dirname(LIB_PATH)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from lib import config

# Base directory containing manga assets.
BASE_DIR = config.MANGA_DIR / "99_資産_Assets"

# Directory containing prompt templates.
TEMPLATES_DIR = Path(__file__).parent / "Templates"

# Relative directories to process from BASE_DIR.
TARGET_DIRS: List[str] = [
    "030プロンプト/01_現状把握と脱労働",
    "030プロンプト/02_投資の魔法と基礎",
    "030プロンプト/03_実践と準備",
    "030プロンプト/04_継続の技術",
    "030プロンプト/05_投資の果実と自由",
    "101プロンプト/01_投資の基礎知識",
    "101プロンプト/02_マインド・哲学",
    "101プロンプト/03_戦略・リスク管理",
    "101プロンプト/04_未来・テクノロジー",
]

# A4 portrait at 300dpi.
IMAGE_WIDTH: int = 2480
IMAGE_HEIGHT: int = 3508

# Candidate background scenes.
SCENES: List[str] = [
    "Modern high-rise office with panoramic city view",
    "Stylish cafe with warm lighting and wooden furniture",
    "Luxurious lounge bar with night city view",
    "Bright meeting room with a large whiteboard",
    "Quiet library or study room with bookshelves",
]

# Legacy constant kept for compatibility with older scripts/templates.
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

### Ai - Visual Lock
- **Hair**: Short black hair, neat style
- **Eyes**: Amber/Brown eyes, calm expression
- **Outfit**: Navy blue school blazer, red necktie, beige cardigan, **NO gloves**
- **Figure**: Slim, teenage girl
- **Expression**: Cool, intelligent, slightly sharp

### Hibiki (香坂響) - Visual Lock
- **Hair**: Long straight black hair
- **Eyes**: Deep brown eyes
- **Style**: Elegant adult woman, office casual
- **Expression**: Calm, mysterious smile

### Suguru (千早優) - Visual Lock
- **Hair**: Messy dark green hair
- **Eyes**: Light blue eyes
- **Outfit**: Brown hoodie or Navy blue school blazer
- **Expression**: Nervous, earnest

### Manager (店長) - Visual Lock
- **Hair**: Short silver/white hair
- **Eyes**: Thin slit eyes, always smiling
- **Outfit**: White shirt, black apron, black bow tie
- **Expression**: Kind, gentle grandfather-like smile
"""
