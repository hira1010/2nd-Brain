"""
漫画制作システムの設定ファイル。
プロンプト生成システムのための定数とパスを定義します。
"""

import sys
import os
from pathlib import Path
from typing import List, Dict

# プロジェクトルートをパスに追加（libのインポート用）
lib_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'lib')
if lib_path not in sys.path:
    sys.path.append(os.path.dirname(lib_path))

from lib import config

# ==========================================
# パス設定
# ==========================================
# 漫画プロジェクトのベースディレクトリ（lib/config.py から取得）
BASE_DIR = config.MANGA_DIR

# 外部テンプレートを格納するディレクトリ
TEMPLATES_DIR = Path(__file__).parent / "templates"

# 処理対象のディレクトリ
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
# ビジュアル設定
# ==========================================
# 高画質 垂直 A4 比率 (300dpi A4 に基づく近似ピクセル)
IMAGE_WIDTH: int = 2480
IMAGE_HEIGHT: int = 3508

# シーン（背景）のバリエーション
SCENES: List[str] = [
    "Modern high-rise office with panoramic city view",
    "Stylish cafe with warm lighting and wooden furniture",
    "Luxurious lounge bar with night city view",
    "Bright meeting room with a large whiteboard",
    "Quiet library or study room with bookshelves"
]

# キャラクターのビジュアル設定 (Visual Lock)
# テンプレートにハードコードされるものですが、参照用に保持。
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
