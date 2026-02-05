import re
import os
import manga_config as config
import manga_utils as utils

def update_manga_prompt(filepath):
    print(f"Processing: {os.path.basename(filepath)}")
    content = utils.read_file(filepath)

    # 1. Parse Metadata
    meta = utils.parse_metadata(content)
    if 'number' not in meta:
        print(f"  SKIP: Required metadata not found in {os.path.basename(filepath)}")
        return False

    no = int(meta['number'])
    title = meta.get('title', 'Unknown Title')
    
    # Logic to fix "She's not explaining" (Copied from apply_variations logic)
    d_teach = meta['dialogue_teach']
    d_desc = meta.get('description', '')
    
    generic_phrases = ["いい心がけね", "詳細を教えるわ", "いいわよ", "聞いて驚きなさい", "Description"]
    is_generic = any(phrase in d_teach for phrase in generic_phrases)

    if is_generic and d_desc and d_desc != d_teach:
        d_teach = f"{d_teach} つまり、{d_desc}"
        
    dialogue_teach = d_teach
    dialogue_intro = meta['dialogue_intro']
    dialogue_desc = meta['dialogue_desc']
    dialogue_action = meta['dialogue_action']

    # キャラクターアンカー（各パネルで繰り返す用）
    REMI_ANK = "Remi (in the SAME RED blazer)"
    YUTO_ANK = "Yuto (in the SAME Black Gakuran)"

    # 1Pテンプレート
    p1_visual_bridge = "イメージで捉えるとこういうことよ。"
    p1_reaction = "なるほど…！\nイメージできました！"

    if no % 2 == 0:
        # レミ主導
        p1_template = f"""### INSTRUCTION: CRITICAL - DO NOT DRAW ANY ENGLISH TEXT. NO VARIATIONS in clothing.
### CHARACTER SETTING
- Remi: {config.REMI_DEF}
- Yuto: {config.YUTO_DEF}
### PAGE LAYOUT (Portrait 1200x1697) Flow: Theme -> Explain -> Visual -> Understand
Panel 1 (Top 25%): {REMI_ANK} introduces topic. {YUTO_ANK} listens. Remi says "優斗君、今日は『{title}』について教えるわよ。" in a Japanese speech bubble. Title box: Black box with white Japanese text "{title}".
Panel 2 (Middle-Top 25%): {REMI_ANK} teaching. Verbal explanation. She says "{dialogue_teach}" in a Japanese speech bubble.
Panel 3 (Middle-Bottom 35%): VISUAL EXPLANATION. Conceptual illustration of '{title}'. Remi pointing at it. She says "{p1_visual_bridge}"
Panel 4 (Bottom 15%): {YUTO_ANK} nodding, looking at the visual. "{p1_reaction}" in a bubble.
### STYLE: Japanese manga, cel shaded. NO GLOVES."""
    else:
        # 優斗主導
        p1_template = f"""### INSTRUCTION: CRITICAL - DO NOT DRAW ANY ENGLISH TEXT. NO VARIATIONS in clothing.
### CHARACTER SETTING
- Remi: {config.REMI_DEF}
- Yuto: {config.YUTO_DEF}
### PAGE LAYOUT (Portrait 1200x1697) Flow: Theme -> Explain -> Visual -> Understand
Panel 1 (Top 25%): {YUTO_ANK} asks question. {REMI_ANK} listens. Yuto says "{dialogue_intro}" in a Japanese speech bubble. Title box: Black slender box with white Japanese text "{title}".
Panel 2 (Middle-Top 25%): {REMI_ANK} explaining verbally. She says "{dialogue_teach}" in a Japanese speech bubble.
Panel 3 (Middle-Bottom 35%): VISUAL EXPLANATION. Large visual metaphor of '{title}'. Remi points to it. She says "{p1_visual_bridge}"
Panel 4 (Bottom 15%): {YUTO_ANK} enlightened reaction. "{p1_reaction}"
### STYLE: Japanese manga, cel shaded. NO GLOVES."""

    # 2Pテンプレート
    p2_template = f"""### INSTRUCTION: CRITICAL - DO NOT DRAW ANY ENGLISH TEXT. NO VARIATIONS in clothing.
### CHARACTER SETTING
- Remi: {config.REMI_DEF}
- Yuto: {config.YUTO_DEF}
### PAGE LAYOUT (Portrait 1200x1697)
Panel 1: EPIC METAPHOR SCENE. {REMI_ANK} navigating a symbolic world of '{title}'. Digital charts in background. Remi has absolute authority.
Panel 2: {REMI_ANK} making a sharp gesture. She says "{dialogue_desc}" in a Japanese speech bubble.
Panel 3: {YUTO_ANK} visualizing profit with golden icons.
Panel 4: {YUTO_ANK} determined, {REMI_ANK} proud. Yuto says "{dialogue_action}" in a bubble. Remi thinks "期待しているわよ。" in a small thoughts bubble.
### STYLE: Cinematic lighting, Gold/Purple theme. NO GLOVES."""

    # 置換
    p1_full = f"{config.PREFIX}\n\n{p1_template}"
    p2_full = f"{config.PREFIX}\n\n{p2_template}"

    # 正規表現で見出し内の中身だけ差し替え
    # NOTE: apply_variations used '## 1ページ目プロンプト...'. This file used the same.
    # We should preserve the structure.
    
    new_content = content
    p1_pattern = r'(## 1ページ目プロンプト\s*\n\s*```text\s*\n).*?(\n```)'
    p2_pattern = r'(## 2ページ目プロンプト\s*\n\s*```text\s*\n).*?(\n```)'

    new_content = re.sub(p1_pattern, r'\1' + p1_full.replace('\\', '\\\\') + r'\2', new_content, flags=re.DOTALL)
    new_content = re.sub(p2_pattern, r'\1' + p2_full.replace('\\', '\\\\') + r'\2', new_content, flags=re.DOTALL)

    if new_content != content:
        utils.write_file(filepath, new_content)
        return True
    return False

count = 0
for filepath in utils.find_manga_prompt_files(config.BASE_DIR):
    if update_manga_prompt(filepath):
        count += 1

print(f"\nSuccessfully updated {count} files.")
