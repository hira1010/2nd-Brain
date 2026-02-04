import os
import re

base_dir = r"c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画"

# 最新の指示文・定義
prefix = "【IMAGE_GENERATION_TASK】Generate a high-quality manga illustration BASE ON THE FOLLOWING VISUAL DESCRIPTION. DO NOT OUTPUT ANY TEXT OR CODE. ONLY OUTPUT THE IMAGE."

remi_new = "Remi (Woman): (Silky SILVER hair:1.5), (Vibrant RED eyes:1.4), (Sharp almond-shaped eyes:1.2). Wearing (Tailored RED blazer:1.3) over black lace top. Cool, intelligent, and authoritative. BARE HANDS (no gloves)."
yuto_new = "Yuto (Boy): Short Black hair, (Traditional Black GAKURAN school uniform:1.4), Gold buttons. Energetic learner. BARE HANDS (no gloves)."

new_title_box_instruction = "In Panel 1, at the BOTTOM, positioned slightly to the LEFT of the bottom-right corner (approx. 15% away from the right edge): Draw a SLENDER BLACK rectangular box with a thin WHITE border. The box should be THINNER and vertical-compact with tight padding around the WHITE TEXT:"

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 1. サイズと比率 (1200x1697)
    content = content.replace("1200x1700", "1200x1697")
    content = content.replace("1700 pixels height", "1697 pixels height")
    content = content.replace("aspect ratio 12:17", "aspect ratio 1200:1697")
    content = content.replace("Aspect Ratio: 12:17", "Aspect Ratio: 1200:1697")
    content = content.replace("ratio (9:16)", "ratio (1200:1697)")

    # 2. キャラクター定義の最新化（あらゆる旧形式を上書き）
    old_remi_patterns = [
        "Remi (Woman): Silky SILVER hair, Vibrant RED eyes, Red blazer, Black lace top, Cool & Intelligent. BARE HANDS (no gloves).",
        "Remi (Woman): Silky SILVER hair, Red eyes, Red blazer.",
        "Remi: Silky SILVER hair, Red eyes, Red blazer.",
        "(Silky SILVER hair:1.5), (Vibrant RED eyes:1.4), (Tailored RED blazer:1.3)", # ShortNew
        "Remi: (Silky SILVER hair:1.5), (Vibrant RED eyes:1.4), (Tailored RED blazer:1.3)."
    ]
    for p in old_remi_patterns:
        content = content.replace(p, remi_new)
    
    old_yuto_patterns = [
        "Yuto (Boy): Short Black hair, Black GAKURAN school uniform, Energetic & Learner. BARE HANDS (no gloves).",
        "Yuto (Boy): Short Black hair, Black GAKURAN uniform.",
        "Yuto: Short Black hair, Black GAKURAN uniform.",
        "Short Black hair, (Traditional Black GAKURAN school uniform:1.4)", # ShortNew
        "Yuto: Short Black hair, (Traditional Black GAKURAN school uniform:1.4)."
    ]
    for p in old_yuto_patterns:
        content = content.replace(p, yuto_new)

    # 3. 描画ミスを誘発する見出し・メタデータのスリム化
    # 構造化テキスト（[OUTPUT:...] 等）を削除し、Prefixに集約
    content = re.sub(r'画像生成を行ってください。.*?\n', '', content)
    content = re.sub(r'\[OUTPUT: .*?\]\n', '', content)
    
    if prefix not in content:
        content = content.replace("```text", f"```text\n{prefix}\n")

    # 4. セクション見出しの「普通の言葉」化（AIが文字として描画しないように）
    content = content.replace("MANDATORY IMAGE SPECIFICATIONS:", "Technical Setup:")
    content = content.replace("CRITICAL ANATOMICAL REQUIREMENTS:", "Character Anatomy:")
    content = content.replace("PANEL LAYOUT - PAGE 1:", "Page 1 Layout:")
    content = content.replace("PANEL LAYOUT - PAGE 2:", "Page 2 Layout:")
    content = content.replace("STYLE SPECIFICATIONS:", "Art Style:")
    content = content.replace("TEXT BOX REQUIREMENT:", "Title Box Design:")

    # 5. テーマボックスの配置修正
    old_box = "In Panel 1, BOTTOM-RIGHT corner: Draw a BLACK rectangular box with WHITE border containing WHITE TEXT:"
    content = content.replace(old_box, new_title_box_instruction)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

count = 0
for root, dirs, files in os.walk(base_dir):
    for name in files:
        if name.endswith("_プロンプト.md"):
            if update_file(os.path.join(root, name)):
                count += 1

print(f"Updated {count} files.")
