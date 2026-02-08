"""
Manga production system configuration file
ASCII-only version to prevent UnicodeDecodeError on Windows.
"""

import os
from pathlib import Path

# Target directory settings
BASE_DIR = Path(r"c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画")
TARGET_DIRS = [
    "01_Investment_Basics",
    "02_Mind_Philosophy",
    "03_Strategy_Risk_Management",
    "04_Future_Technology"
]

# Internal directory name mapping (English key : Japanese folder name)
DIR_MAP = {
    "01_Investment_Basics": "01_\u6295\u8cc7\u306e\u57fa\u790e\u77e5\u8b58",
    "02_Mind_Philosophy": "02_\u30de\u30a4\u30f3\u30c9\u30fb\u54f2\u5b66",
    "03_Strategy_Risk_Management": "03_\u6226\u7565\u30fb\u30ea\u30b9\u30af\u7ba1\u7406",
    "04_Future_Technology": "04_\u672a\u6765\u30fb\u30c6\u30af\u30ce\u30ed\u30b8\u30fc"
}

# Scene variations (Background)
SCENES = [
    "Modern high-rise office with panoramic city view",
    "Stylish cafe with warm lighting and wooden furniture",
    "Luxurious lounge bar with night city view",
    "Bright meeting room with a large whiteboard",
    "Quiet library or study room with bookshelves"
]

# Character visual settings (visual lock)
CHARACTER_SETTINGS_EN = """## Character Settings (Global)

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

IMAGE_WIDTH = 1200
IMAGE_HEIGHT = 1697

# 2P Manga Generation Common Template (English headings, parameters preserved)
TEMPLATE = """# No.{NO} {TITLE} 2P Manga Prompt

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
