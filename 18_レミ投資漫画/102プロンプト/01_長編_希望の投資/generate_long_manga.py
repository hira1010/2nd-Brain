# -*- coding: utf-8 -*-
import os
import sys

# Force UTF-8 for stdout
sys.stdout.reconfigure(encoding='utf-8')

# Configuration
BASE_DIR = r"c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画\102プロンプト\01_長編_希望の投資"
STORY_FILE = os.path.join(BASE_DIR, "00_ストーリー構成.md")

# Master Prompts (from apply_master_fix.js)
MASTER_ARCHITECTURE = "ARCHITECTURE: [v15.5 EDGE OBLITERATOR] FULL BLEED. ZERO PIXEL MARGINS. 110% OVERFILL. 12:17."
MASTER_REMI = "- Remi: (Crimson RED blazer, Black lace top). (LONG STARK STRAIGHT SILVER hair). (GLOWING SOLID BLOOD-RED eyes). NO GLOVES."
MASTER_YUTO = "- Yuto: (BLACK Gakuran, gold buttons). (Short Black hair). BARE HANDS."
MASTER_STYLE = "### Style: Premium manga, cinematic lighting, best quality, masterpiece, sharp focus, high contrast. 12:17 ratio. **CORE**: OBLITERATE ALL CANVAS MARGINS. ALL ART MUST BE FULL BLEED."
MASTER_NEGATIVE = "**NEGATIVE PROMPT**: white edges, side bars, pillarbox, letterbox, black bars, gutter, split screen, frame, border, text labels, low quality, blurry, margins, padding, cropped."

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

# Panel Templates (approx 3 pages per file)
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

| タイトル | {title} |
| 解説 | {summary} |
"""

def create_file(filename, content):
    filepath = os.path.join(BASE_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {filename}")

# Story Data (Simplified mapping for generation)
# I will generate placeholder files with the correct structure, 
# and fill them with the specific plot points based on the chapter.

chapters = [
    {"num": 1, "title": "絶望と誘惑", "pages": range(1, 21), "desc": "増税マン・物価高マンの襲撃、田中の誘惑"},
    {"num": 2, "title": "種を蒔く決意", "pages": range(21, 41), "desc": "レミの説教、複利の魔法、苗木を植える"},
    {"num": 3, "title": "嵐と試練", "pages": range(41, 66), "desc": "暴落、ノイズ、田中の退場、耐える優斗"},
    {"num": 4, "title": "成長と開花", "pages": range(66, 91), "desc": "資産回復、金のなる木の成長、精神的自立"},
    {"num": 5, "title": "未来への継承", "pages": range(91, 116), "desc": "20年後、F-U Money、後輩への指導、エピローグ"}
]

def generate_prompts():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    file_counter = 1
    
    for chapter in chapters:
        pages = list(chapter["pages"])
        # Chunk pages into groups of 3
        chunks = [pages[i:i + 3] for i in range(0, len(pages), 3)]
        
        for chunk in chunks:
            # Handle last chunk if less than 3 pages
            current_pages = chunk
            while len(current_pages) < 3:
                current_pages.append(current_pages[-1]) # Repeat last page placeholder if needed
            
            p_start = current_pages[0]
            p_end = current_pages[-1] 
            if p_end == p_start: # if only one page actual
                 filename = f"No102_{file_counter:03d}_Ch{chapter['num']}_P{p_start:03d}_プロンプト.md"
            else:
                filename = f"No102_{file_counter:03d}_Ch{chapter['num']}_P{p_start:03d}-{p_end:03d}_プロンプト.md"
            
            
            # Contextual Prompt Content Generation
            # This is a basic template, specific scene details would ideally come from a detailed CSV or JSON
            # For now, I will use generic prompts that align with the chapter theme
            
            scene_desc = chapter['desc']
            title = f"第{chapter['num']}章 {chapter['title']} ({p_start}-{p_end})"
            
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
                title=title,
                summary=f"{scene_desc}"
            )
            
            create_file(filename, content)
            file_counter += 1

if __name__ == "__main__":
    generate_prompts()
