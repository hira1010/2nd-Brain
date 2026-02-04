import os
import re

base_dir = r"c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画"

# 最新のキャラクター定義
REMI_DEF = "Remi: (Silky SILVER hair:1.5), (Vibrant RED eyes:1.4). OUTFIT: Always wearing a (Tailored RED blazer:1.3) with a (Black lace camisole:1.2) underneath. Identical clothes in every panel. NO GLOVES."
YUTO_DEF = "Yuto: (Short Black hair:1.3). OUTFIT: (Traditional Black GAKURAN school uniform:1.4) with gold buttons. Identical clothes in every panel. NO GLOVES."

# プロンプトのプレフィックス
PREFIX = "【IMAGE_GENERATION_TASK】Generate high-quality manga. VISUAL CONSISTENCY IS CRITICAL: Characters MUST wear the EXACT SAME OUTFIT in every panel. DO NOT DRAW ANY ENGLISH TEXT."

def update_manga_prompt(filepath):
    print(f"Processing: {os.path.basename(filepath)}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # No、タイトル、ダイアログの抽出
    no_match = re.search(r'\| No \| (\d+) \|', content)
    title_match = re.search(r'\| タイトル \| (.*?) \|', content)
    intro_match = re.search(r'\| DIALOGUE_INTRO \| (.*?) \|', content)
    teach_match = re.search(r'\| DIALOGUE_TEACH \| (.*?) \|', content)
    desc_match = re.search(r'\| DIALOGUE_DESC \| (.*?) \|', content)
    action_match = re.search(r'\| DIALOGUE_ACTION \| (.*?) \|', content)

    if not (no_match and title_match):
        print(f"  SKIP: Required metadata not found in {os.path.basename(filepath)}")
        return False

    no = int(no_match.group(1))
    title = title_match.group(1).strip()
    intro = intro_match.group(1).strip() if intro_match else "レミさん！教えてください！"
    teach = teach_match.group(1).strip() if teach_match else "いいわよ。しっかり聞きなさい。"
    desc = desc_match.group(1).strip() if desc_match else "これが投資の本質よ。"
    action = action_match.group(1).strip() if action_match else "なるほど！実践してみます！"

    # キャラクターアンカー（各パネルで繰り返す用）
    REMI_ANK = "Remi (in the SAME RED blazer)"
    YUTO_ANK = "Yuto (in the SAME Black Gakuran)"

    # 1Pテンプレート
    if no % 2 == 0:
        # レミ主導
        p1_template = f"""### INSTRUCTION: CRITICAL - DO NOT DRAW ANY ENGLISH TEXT. NO VARIATIONS in clothing.
### CHARACTER SETTING
- Remi: {REMI_DEF}
- Yuto: {YUTO_DEF}
### PAGE LAYOUT (Portrait 1200x1697)
Panel 1: {REMI_ANK} pointing at whiteboard, {YUTO_ANK} taking notes. Remi says "優斗君、今日は『{title}』について教えるわよ。" in a Japanese speech bubble. Title box: Black box with white Japanese text "{title}".
Panel 2: {REMI_ANK} explaining concepts. She says "{teach}" in a Japanese speech bubble.
Panel 3: {YUTO_ANK} nodding. "はい、レミさん！" in a bubble.
Panel 4: {REMI_ANK}'s side profile.
### STYLE: Japanese manga, cel shaded. NO GLOVES."""
    else:
        # 優斗主導
        p1_template = f"""### INSTRUCTION: CRITICAL - DO NOT DRAW ANY ENGLISH TEXT. NO VARIATIONS in clothing.
### CHARACTER SETTING
- Remi: {REMI_DEF}
- Yuto: {YUTO_DEF}
### PAGE LAYOUT (Portrait 1200x1697)
Panel 1: {YUTO_ANK} and {REMI_ANK} in a meeting room. Yuto says "{intro}" in a Japanese speech bubble. Title box: Black slender box with white Japanese text "{title}".
Panel 2: Extreme Close-up of {REMI_ANK}'s red eyes. She says "{teach}" in a Japanese speech bubble.
Panel 3: {YUTO_ANK} with manga shock lines.
Panel 4: {REMI_ANK} smiling coolly.
### STYLE: Japanese manga, cel shaded. NO GLOVES."""

    # 2Pテンプレート
    p2_template = f"""### INSTRUCTION: CRITICAL - DO NOT DRAW ANY ENGLISH TEXT. NO VARIATIONS in clothing.
### CHARACTER SETTING
- Remi: {REMI_DEF}
- Yuto: {YUTO_DEF}
### PAGE LAYOUT (Portrait 1200x1697)
Panel 1: EPIC METAPHOR SCENE. {REMI_ANK} navigating a symbolic world of '{title}'. Digital charts in background. Remi has absolute authority.
Panel 2: {REMI_ANK} making a sharp gesture. She says "{desc}" in a Japanese speech bubble.
Panel 3: {YUTO_ANK} visualizing profit with golden icons.
Panel 4: {YUTO_ANK} determined, {REMI_ANK} proud. Yuto says "{action}" in a bubble. Remi thinks "期待しているわよ。" in a small thoughts bubble.
### STYLE: Cinematic lighting, Gold/Purple theme. NO GLOVES."""

    # 置換
    p1_full = f"{PREFIX}\n\n{p1_template}"
    p2_full = f"{PREFIX}\n\n{p2_template}"

    # 正規表現で見出し内の中身だけ差し替え
    p1_pattern = r'(## 1ページ目プロンプト\s*\n\s*```text\s*\n).*?(\n```)'
    p2_pattern = r'(## 2ページ目プロンプト\s*\n\s*```text\s*\n).*?(\n```)'

    new_content = re.sub(p1_pattern, r'\1' + p1_full.replace('\\', '\\\\') + r'\2', content, flags=re.DOTALL)
    new_content = re.sub(p2_pattern, r'\1' + p2_full.replace('\\', '\\\\') + r'\2', new_content, flags=re.DOTALL)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

count = 0
for root, dirs, files in os.walk(base_dir):
    for name in files:
        if name.endswith("_プロンプト.md"):
            if update_manga_prompt(os.path.join(root, name)):
                count += 1

print(f"\nSuccessfully updated {count} files.")
