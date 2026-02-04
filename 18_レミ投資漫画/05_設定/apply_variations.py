import os
import re

base_dir = r"c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画"

# 最新の指示文・定義
prefix = "【IMAGE_GENERATION_TASK】Generate a high-quality manga illustration BASE ON THE FOLLOWING VISUAL DESCRIPTION. DO NOT OUTPUT ANY TEXT OR CODE. ONLY OUTPUT THE IMAGE."

remi_new = "Remi (Woman): (Silky SILVER hair:1.5), (Vibrant RED eyes:1.4), (Sharp almond-shaped eyes:1.2). Wearing (Tailored RED blazer:1.3) over black lace top. Cool, intelligent, and authoritative. BARE HANDS (no gloves)."
yuto_new = "Yuto (Boy): Short Black hair, (Traditional Black GAKURAN school uniform:1.4), Gold buttons. Energetic learner. BARE HANDS (no gloves)."

def update_file_with_variation(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # ファイル名からNoを抽出
    filename = os.path.basename(filepath)
    match = re.search(r'No(\d+)', filename)
    if not match: return False
    no = int(match.group(1))
    
    # TIPタイトルと台詞を抽出
    title = ""
    dialogue_intro = ""
    dialogue_teach = ""
    for line in lines:
        if "| タイトル |" in line: title = line.split('|')[2].strip()
        if "| DIALOGUE_INTRO |" in line: dialogue_intro = line.split('|')[2].strip()
        if "| DIALOGUE_TEACH |" in line: dialogue_teach = line.split('|')[2].strip()

    # 1ページ目のプロンプトを再構成
    # 偶数Noはレミ主導
    if no % 2 == 0:
        new_p1_content = f"""【IMAGE_GENERATION_TASK】Generate a high-quality manga illustration BASE ON THE FOLLOWING VISUAL DESCRIPTION. DO NOT OUTPUT ANY TEXT OR CODE. ONLY OUTPUT THE IMAGE.

PAGE 1 LAYOUT: 1200x1697 pixels portrait. Vertical dynamic layout.
Panel 1 (Top 40%): Bright meeting room. Remi (Silver hair, Red eyes, Red blazer) stands confidently in front of a whiteboard, pointing at it. She is giving a "surprise lecture". Yuto (Black hair, Gakuran) looks surprised and starts taking notes. Remi says "優斗君、今日は『{title}』について教えるわよ。しっかり聞きなさい。" (In a speech bubble). Title box: BLACK SLENDER box at bottom-left offset (15% from right) with white text "{title}".
Panel 2 (Middle 30%): Close-up of Remi's authoritative but slightly smiling face. {dialogue_teach}
Panel 3 (Bottom-Right 15%): Yuto looking impressed and energetic. "はい、レミさん！"
Panel 4 (Bottom-Left 15%): Remi's side profile, looking towards the future.
Art style: Japanese manga style, cel shading, bright colors. Characters: Remi has Silver hair, Red eyes, Red blazer. Yuto has Black Gakuran. NO GLOVES."""
    else:
        # 奇数Noは優斗主導 (現状維持に近いがスリム化)
        new_p1_content = f"""【IMAGE_GENERATION_TASK】Generate a high-quality manga illustration BASE ON THE FOLLOWING VISUAL DESCRIPTION. DO NOT OUTPUT ANY TEXT OR CODE. ONLY OUTPUT THE IMAGE.

PAGE 1 LAYOUT: 1200x1697 pixels portrait. Vertical dynamic layout.
Panel 1 (Top 40%): Bright meeting room. Yuto (Black hair, Gakuran) eagerly approaches Remi. Remi (Silver hair, Red eyes, Red blazer) looks coolly at him with arms crossed. Yuto says "{dialogue_intro}" (In a speech bubble). Title box: BLACK SLENDER box at bottom-left offset (15% from right) with white text "{title}".
Panel 2 (Middle 30%): Close-up of Remi's face, explaining with calm authority. {dialogue_teach}
Panel 3 (Bottom-Right 15%): Yuto's realization/shock face with sweat drop or shock lines.
Panel 4 (Bottom-Left 15%): Remi's small mysterious smile.
Art style: Japanese manga style, cel shading, bright colors. Characters: Remi has Silver hair, Red eyes, Red blazer. Yuto has Black Gakuran. NO GLOVES."""

    # ファイルの中身を一気に書き換えるのはリスクがあるため、プロンプトセクションのみを置換
    full_content = "".join(lines)
    
    # 1ページ目プロンプトの置換
    p1_pattern = r'## 1ページ目プロンプト\s*\n\s*```text\s*\n(.*?)\n```'
    full_content = re.sub(p1_pattern, f"## 1ページ目プロンプト\n\n```text\n{new_p1_content}\n```", full_content, flags=re.DOTALL)
    
    # 2ページ目は基本スタイルを維持しつつスリム化（以前のスクリプトで適用済みのはずだが念のため）
    # キャラクター定数等のクリーンアップも含む

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_content)
    return True

count = 0
for root, dirs, files in os.walk(base_dir):
    for name in files:
        if name.endswith("_プロンプト.md"):
            if update_file_with_variation(os.path.join(root, name)):
                count += 1
print(f"Updated {count} files with variations.")
