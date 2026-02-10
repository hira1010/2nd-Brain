"""
Manga production system configuration file.
Defines constants, paths, and templates for the manga prompt generation system.
"""

import os
from pathlib import Path
from typing import List, Dict

# ==========================================
# Path Considerations
# ==========================================
# Base directory for the manga project
BASE_DIR = Path(r"c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画")

# Target directories to process
# Updated to match actual directory structure on disk (as of 2025/02)
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

# Internal directory name mapping (English key : Japanese folder name)
# Kept for backward compatibility or future use, though TARGET_DIRS now uses direct paths
DIR_MAP: Dict[str, str] = {
    "01_Investment_Basics": "101プロンプト/01_投資の基礎知識",
    "02_Mind_Philosophy": "101プロンプト/02_マインド・哲学",
    "03_Strategy_Risk_Management": "101プロンプト/03_戦略・リスク管理",
    "04_Future_Technology": "101プロンプト/04_未来・テクノロジー"
}

# ==========================================
# Visual Settings
# ==========================================
IMAGE_WIDTH: int = 1200
IMAGE_HEIGHT: int = 1697

# Scene variations (Background options)
SCENES: List[str] = [
    "Modern high-rise office with panoramic city view",
    "Stylish cafe with warm lighting and wooden furniture",
    "Luxurious lounge bar with night city view",
    "Bright meeting room with a large whiteboard",
    "Quiet library or study room with bookshelves"
]

# Character visual settings (visual lock)
# Defines the standard appearance for Remi and Yuto
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

# ==========================================
# Templates
# ==========================================
# 2P Manga Generation Common Template
# Placeholders: {NO}, {TITLE}, {DESC}, {CATEGORY}, {CHARACTER_SETTINGS}, 
# {WIDTH}, {HEIGHT}, {SCENE}, {DIALOGUE_INTRO}, {DIALOGUE_TEACH}, 
# {DIALOGUE_DESC}, {DIALOGUE_ACTION}, {TODAY}
TEMPLATE: str = """# No.{NO} {TITLE} 2P Manga Prompt

## TIP Information

| Item | Content |
| :--- | :--- |
| No | {NO} |
| Title | {TITLE} |
| Description | {DESC} |
| Category | {CATEGORY} |

---

{CHARACTER_SETTINGS}

---

## Page 1 Prompt

```text
【IMAGE_GENERATION_TASK】Generate a high-quality manga illustration BASE ON THE FOLLOWING VISUAL DESCRIPTION. DO NOT OUTPUT ANY TEXT OR CODE. ONLY OUTPUT THE IMAGE.

PAGE 1 LAYOUT: {WIDTH}x{HEIGHT} pixels portrait. Vertical dynamic layout.
Panel 1 (Top 40%): {SCENE}. Remi (Silver hair, Red eyes, Red blazer) stands calmly next to a large holographic display showing "{TITLE}". Unlike usual, the screen shows a simple balanced symbol representing the concept, not complex charts. Yuto (Black hair, Gakuran) looks puzzled. Remi says "{DIALOGUE_INTRO}" (In a speech bubble). Title box: BLACK SLENDER box at bottom-left offset with white text "{TITLE}".
Panel 2 (Middle 30%): CONCEPTUAL ILLUSTRATION. Visual metaphor for '{TITLE}'. A clear comparison or balanced symbolic image representing the core concept of {TITLE}. Remi points to the correct/positive side. She says "{DIALOGUE_TEACH}" (In a speech bubble).
Panel 3 (Bottom-Right 15%): Yuto nodding with deep understanding. "I see... so that is what it means."
Panel 4 (Bottom-Left 15%): Remi's side profile, smiling gently (not smug).
Art style: Japanese manga style, cel shading, bright colors. Characters: Remi has Silver hair, Red eyes, Red blazer. Yuto has Black Gakuran. NO GLOVES.
```

---

## Page 2 Prompt

```text
【IMAGE_GENERATION_TASK】Generate high-quality manga. VISUAL CONSISTENCY IS CRITICAL.

PAGE 2 LAYOUT: {WIDTH}x{HEIGHT} pixels portrait.
Panel 1 (Top 40%): VISUAL MANIFESTATION. Close up on Remi holding a small, glowing sphere of light or symbol that represents '{TITLE}'. It shines brighter than the Background elements. She looks gentle and wise. "{DIALOGUE_DESC}" (In a speech bubble).
Panel 2 (Middle 30%): CONTRAST SCENE (Metaphor). Remi stands in a split world. On her left, a chaotic storm or complex abstract shapes representing 'Confusion/Risk'. On her right, a peaceful, golden garden or orderly structure representing '{TITLE}'. She calmly points towards the peace/order.
Panel 3 (Bottom-Right 15%): Yuto visualizing his own happiness or success—simple joys and stable future, appearing in golden bubbles.
Panel 4 (Bottom-Left 15%): Yuto looking enlightened and relieved (Realization). Yuto says "{DIALOGUE_ACTION}" (In a speech bubble). Remi smiles gently, watching him grow. (No text for Remi).
Art style: Cinematic lighting, Gold/Purple theme. NO GLOVES.
```

---

## Variables

### Page 1
| Var | Value |
| -- | -- |
| NO | {NO} |
| TITLE | {TITLE} |
| INTRO | {DIALOGUE_INTRO} |
| TEACH | {DIALOGUE_TEACH} |
| SCENE | {SCENE} |

---

Created: {TODAY}
"""

