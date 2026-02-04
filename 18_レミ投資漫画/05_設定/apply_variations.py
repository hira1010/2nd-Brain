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

    # ---------------------------------------------------------
    # 1ページ目の構成 (Page 1)
    # ---------------------------------------------------------
    p1_reaction = "なるほど…そういうことなんですね"  # より自然な納得のリアクション
    
    # 偶数Noはレミ主導
    if no % 2 == 0:
        new_p1_content = f"""【IMAGE_GENERATION_TASK】Generate a high-quality manga illustration BASE ON THE FOLLOWING VISUAL DESCRIPTION. DO NOT OUTPUT ANY TEXT OR CODE. ONLY OUTPUT THE IMAGE.

PAGE 1 LAYOUT: 1200x1697 pixels portrait. Vertical dynamic layout.
Panel 1 (Top 40%): Bright high-tech office. Remi (Silver hair, Red eyes, Red blazer) stands confidently next to a large holographic display showing the text "{title}". Yuto (Black hair, Gakuran) looks at it with curiosity. Remi says "優斗君、今日は『{title}』について教えるわよ。" (In a speech bubble). Title box: BLACK SLENDER box at bottom-left offset with white text "{title}".
Panel 2 (Middle 30%): CONCEPTUAL ILLUSTRATION. The entire panel is a visual metaphor for '{title}'. (e.g., A path diverging, a growing tree, or abstract currency flowing). Remi is part of this scene, explaining the concept with a pointer. The image itself explains the meaning. She says "{dialogue_teach}" (In a speech bubble).
Panel 3 (Bottom-Right 15%): Yuto nodding with deep understanding. "{p1_reaction}"
Panel 4 (Bottom-Left 15%): Remi's side profile, looking cool and intellectual.
Art style: Japanese manga style, cel shading, bright colors. Characters: Remi has Silver hair, Red eyes, Red blazer. Yuto has Black Gakuran. NO GLOVES."""
    else:
        # 奇数Noは優斗主導
        new_p1_content = f"""【IMAGE_GENERATION_TASK】Generate a high-quality manga illustration BASE ON THE FOLLOWING VISUAL DESCRIPTION. DO NOT OUTPUT ANY TEXT OR CODE. ONLY OUTPUT THE IMAGE.

PAGE 1 LAYOUT: 1200x1697 pixels portrait. Vertical dynamic layout.
Panel 1 (Top 40%): Bright high-tech office. Yuto (Black hair, Gakuran) asks a question to Remi. Remi (Silver hair, Red eyes, Red blazer) listens with arms crossed. Yuto says "{dialogue_intro}" (In a speech bubble). Title box: BLACK SLENDER box at bottom-left offset with white text "{title}".
Panel 2 (Middle 30%): CONCEPTUAL ART. A clear visual metaphor of '{title}' occupies the background. Remi explains this concept, integrated into the visual. She says "{dialogue_teach}" (In a speech bubble).
Panel 3 (Bottom-Right 15%): Yuto looking shocked/realizing the truth. Background has lightning effect.
Panel 4 (Bottom-Left 15%): Remi's small confident smile.
Art style: Japanese manga style, cel shading, bright colors. Characters: Remi has Silver hair, Red eyes, Red blazer. Yuto has Black Gakuran. NO GLOVES."""

    # ---------------------------------------------------------
    # 2ページ目の構成 (Page 2) - 新規追加
    # ---------------------------------------------------------
    
    # 2ページ目の情報を抽出
    dialogue_desc = ""
    dialogue_action = ""
    for line in lines:
        if "| DIALOGUE_DESC |" in line: dialogue_desc = line.split('|')[2].strip()
        # if "| DIALOGUE_ACTION |" in line: dialogue_action = line.split('|')[2].strip() # 既存のアクションは使わず、より自然なものに置換する場合もあるが、一応取得
    
    # 自然なリアクション（固定に近いが、文脈に合わせる）
    p2_reaction = "深く胸に刻みます…！"

    new_p2_content = f"""【IMAGE_GENERATION_TASK】Generate high-quality manga. VISUAL CONSISTENCY IS CRITICAL.

PAGE 2 LAYOUT: 1200x1697 pixels portrait.
Panel 1 (Top 40%): EPIC METAPHOR SCENE. Remi (in RED blazer) navigating a symbolic world representing '{title}'. Digital charts or abstract visuals completely surround her. She has absolute authority here.
Panel 2 (Middle 30%): VISUAL MANIFESTATION of the dialogue. The background vividly illustrates the concept: "{dialogue_desc}". Remi explains it within this visualized world. She says "{dialogue_desc}" (In a speech bubble).
Panel 3 (Bottom-Right 15%): Yuto visualizing his own future success based on this advice. Golden icons or happy future self imagery.
Panel 4 (Bottom-Left 15%): Yuto determined, Remi proud. Yuto says "{p2_reaction}" (In a speech bubble). Remi thinks "期待しているわよ。" (In a thought bubble).
Art style: Cinematic lighting, Gold/Purple theme. NO GLOVES."""

    # ファイルの中身を更新
    full_content = "".join(lines)
    
    # 1ページ目プロンプトの置換
    p1_pattern = r'## 1ページ目プロンプト\s*\n\s*```text\s*\n(.*?)\n```'
    full_content = re.sub(p1_pattern, f"## 1ページ目プロンプト\n\n```text\n{new_p1_content}\n```", full_content, flags=re.DOTALL)

    # 2ページ目プロンプトの置換
    p2_pattern = r'## 2ページ目プロンプト\s*\n\s*```text\s*\n(.*?)\n```'
    full_content = re.sub(p2_pattern, f"## 2ページ目プロンプト\n\n```text\n{new_p2_content}\n```", full_content, flags=re.DOTALL)

    
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
