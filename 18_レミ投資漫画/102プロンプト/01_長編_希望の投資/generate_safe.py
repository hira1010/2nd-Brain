# -*- coding: utf-8 -*-
import os
import sys

# Ensure stdout handles utf-8 (though we won't print non-ascii)
sys.stdout.reconfigure(encoding='utf-8')

# Use current working directory to avoid path encoding issues in source code
BASE_DIR = os.getcwd()

# Master Prompts (ASCII safe)
MASTER_ARCHITECTURE = "ARCHITECTURE: [v15.5 EDGE OBLITERATOR] FULL BLEED. ZERO PIXEL MARGINS. 110% OVERFILL. 12:17."
MASTER_REMI = "- Remi: (Crimson RED blazer, Black lace top). (LONG STARK STRAIGHT SILVER hair). (GLOWING SOLID BLOOD-RED eyes). NO GLOVES."
MASTER_YUTO = "- Yuto: (BLACK Gakuran, gold buttons). (Short Black hair). BARE HANDS."
MASTER_STYLE = "### Style: Premium manga, cinematic lighting, best quality, masterpiece, sharp focus, high contrast. 12:17 ratio. **CORE**: OBLITERATE ALL CANVAS MARGINS. ALL ART MUST BE FULL BLEED."
MASTER_NEGATIVE = "**NEGATIVE PROMPT**: white edges, side bars, pillarbox, letterbox, black bars, gutter, split screen, frame, border, text labels, low quality, blurry, margins, padding, cropped."

# Japanese strings escaped
# Tanaka: ... (Short messy brown hair).
# Zouzei-man: ... (Dark shadowy aura).
# Bukkadaka-man: ... (Red angry aura).
# MoneyTree: ... (Radiant energy).

HEADER_TEMPLATE = f"""{MASTER_ARCHITECTURE}

### Characters:
{MASTER_REMI}
{MASTER_YUTO}
- Tanaka: (Dark suit, loose tie, arrogant smirk). (Short messy brown hair).
- Zouzei-man: (Giant monstrous figure made of tax forms and coins). (Dark shadowy aura).
- Bukkadaka-man: (Bloated monster with price tags). (Red angry aura).
- MoneyTree: (Glowing golden sapling/tree). (Radiant energy).

{MASTER_STYLE}
{MASTER_NEGATIVE}

"""

PANEL_TEMPLATE = """
# Page {page_num}
[Panel 1]: {p1_desc}
[Panel 2]: {p2_desc}
[Panel 3]: {p3_desc}

# Page {page_num_2}
[Panel 1]: {p4_desc}
[Panel 2]: {p5_desc}
[Panel 3]: {p6_desc}

# Page {page_num_3}
[Panel 1]: {p7_desc}
[Panel 2]: {p8_desc}
[Panel 3]: {p9_desc}

| \u30bf\u30a4\u30c8\u30eb | {title} |
| \u89e3\u8aac | {summary} |
"""

def create_file(filename, content):
    filepath = os.path.join(BASE_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {filename}")

# Chapters
# 1: Despair and Temptation
# 2: Determination
# 3: Storm and Trial
# 4: Growth and Bloom
# 5: Inheritance
chapters = [
    {"num": 1, "title": "\u7d76\u671b\u3068\u8a98\u60d1", "pages": range(1, 21), "desc": "\u5897\u7a0e\u30de\u30f3\u30fb\u7269\u4fa1\u9ad8\u30de\u30f3\u306e\u8972\u6483\u3001\u7530\u4e2d\u306e\u8a98\u60d1"},
    {"num": 2, "title": "\u7a2e\u3092\u8494\u304f\u6c7a\u610f", "pages": range(21, 41), "desc": "\u30ec\u30bf\u306e\u8aac\u6559\u3001\u8907\u5229\u306e\u9b54\u6cd5\u3001\u82d7\u6728\u3092\u690d\u3048\u308b"},
    {"num": 3, "title": "\u5d50\u3068\u8a66\u7df4", "pages": range(41, 66), "desc": "\u66b4\u843d\u3001\u30ce\u30a4\u30ba\u3001\u7530\u4e2d\u306e\u9000\u5834\u3001\u8010\u3048\u308b\u512a\u6597"},
    {"num": 4, "title": "\u6210\u9577\u3068\u958b\u82b1", "pages": range(66, 91), "desc": "\u8cc7\u7523\u56de\u5fa9\u3001\u91d1\u306e\u306a\u308b\u6728\u306e\u6210\u9577\u3001\u7cbe\u795e\u7684\u81ea\u7acb"},
    {"num": 5, "title": "\u672a\u6765\u3078\u306e\u7d99\u627f", "pages": range(91, 116), "desc": "20\u5e74\u5f8c\u3001F-U Money\u3001\u5f8c\u8f29\u3078\u306e\u6307\u5c0e\u3001\u30a8\u30d4\u30ed\u30fc\u30b0"}
]

def generate_prompts():
    file_counter = 1
    
    for chapter in chapters:
        pages = list(chapter["pages"])
        chunks = [pages[i:i + 3] for i in range(0, len(pages), 3)]
        
        for chunk in chunks:
            current_pages = chunk
            while len(current_pages) < 3:
                current_pages.append(current_pages[-1])
            
            p_start = current_pages[0]
            p_end = current_pages[-1] 
            
            # Formatting title with escaped chars
            # 第{num}章 {title} (P...)
            title_str = f"\u7b2c{chapter['num']}\u7ae0 {chapter['title']} (P{p_start}-{p_end})"

            if p_end == p_start:
                 filename = f"No102_{file_counter:03d}_Ch{chapter['num']}_P{p_start:03d}_\u30d7\u30ed\u30f3\u30d7\u30c8.md"
            else:
                 filename = f"No102_{file_counter:03d}_Ch{chapter['num']}_P{p_start:03d}-{p_end:03d}_\u30d7\u30ed\u30f3\u30d7\u30c8.md"
            
            scene_desc = chapter['desc']
            
            content = HEADER_TEMPLATE + PANEL_TEMPLATE.format(
                page_num=current_pages[0],
                page_num_2=current_pages[1],
                page_num_3=current_pages[2],
                p1_desc=f"High quality manga panel. {scene_desc}. Focus on emotion and atmosphere. Masterpiece.",
                p2_desc=f"High quality manga panel. Character interaction. {scene_desc}. Detailed background.",
                p3_desc=f"High quality manga panel. Dramatic angle. {scene_desc}. 12:17 vertical ratio.",
                p4_desc=f"High quality manga panel. {scene_desc}. Progressing story.",
                p5_desc=f"High quality manga panel. {scene_desc}. Emotional reaction.",
                p6_desc=f"High quality manga panel. {scene_desc}. Symbolic imagery.",
                p7_desc=f"High quality manga panel. {scene_desc}. Climax of the sequence.",
                p8_desc=f"High quality manga panel. {scene_desc}. Reflective moment.",
                p9_desc=f"High quality manga panel. {scene_desc}. Transition to next scene.",
                title=title_str,
                summary=f"{scene_desc}"
            )
            
            create_file(filename, content)
            file_counter += 1

if __name__ == "__main__":
    generate_prompts()
