import os
import re

base_dir = r"c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画"

# 最新の指示文・定義
prefix = "【IMAGE_GENERATION_TASK】Generate a high-quality manga illustration BASE ON THE FOLLOWING VISUAL DESCRIPTION. DO NOT OUTPUT ANY TEXT OR CODE. ONLY OUTPUT THE IMAGE."

remi_new = "Remi (Woman): (Silky SILVER hair:1.5), (Vibrant RED eyes:1.4), (Sharp almond-shaped eyes:1.2). Wearing (Tailored RED blazer:1.3) over black lace top. Cool, intelligent, and authoritative. BARE HANDS (no gloves)."
yuto_new = "Yuto (Boy): Short Black hair, (Traditional Black GAKURAN school uniform:1.4), Gold buttons. Energetic learner. BARE HANDS (no gloves)."

new_title_box_instruction = "In Panel 1, at the BOTTOM, positioned slightly to the LEFT of the bottom-right corner (approx. 15% away from the right edge): Draw a SLENDER BLACK rectangular box with a thin WHITE border. The box should be THINNER and vertical-compact with tight padding around the WHITE TEXT:"

def update_file_safely(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content.strip():
            print(f"Skipping empty file: {filepath}")
            return False
            
        original = content
        
        # 1. ファイル名からNoを抽出してバリエーションを決定
        filename = os.path.basename(filepath)
        match = re.search(r'No(\d+)', filename)
        no = int(match.group(1)) if match else 1
        
        # タイトルと既存の台詞を抽出（置換用）
        title_match = re.search(r'\| タイトル \| (.*?) \|', content)
        title = title_match.group(1).strip() if title_match else "投資"
        
        intro_match = re.search(r'\| DIALOGUE_INTRO \| (.*?) \|', content)
        intro = intro_match.group(1).strip() if intro_match else "教えてください！"
        
        teach_match = re.search(r'\| DIALOGUE_TEACH \| (.*?) \|', content)
        teach = teach_match.group(1).strip() if teach_match else "いいわよ。"

        # 2. 1ページ目のプロンプト内容自体をスリム化＆バリエーション化
        if no % 2 == 0:
            # 偶数：レミ主導
            new_p1 = f"""{prefix}

PAGE 1 LAYOUT: 1200x1697 pixels portrait. Vertical dynamic layout.
Panel 1 (Top 40%): Bright meeting room. Remi (Silver hair, Red eyes, Red blazer) stands confidently, pointing at a whiteboard to start a surprise lecture. Yuto (Black hair, Gakuran) looks surprised but eager. Remi says "優斗君、今日は『{title}』について教えるわよ。しっかり聞きなさい。" (In a speech bubble). Title box: BLACK SLENDER box at bottom-left offset (15% from right) with white text "{title}".
Panel 2 (Middle 30%): Close-up of Remi's face, explaining authoritative yet kindly. {teach}
Panel 3 (Bottom-Right 30%): Yuto looking impressed and nodding. "はい、レミさん！"
Panel 4 (Bottom-Left 30%): Remi's mysterious side profile.
Art style: Japanese manga style, cel shading, professional quality. Characters: Remi has Silver hair, Red eyes, Red blazer. Yuto has Black Gakuran. NO GLOVES."""
        else:
            # 奇数：優斗主導
            new_p1 = f"""{prefix}

PAGE 1 LAYOUT: 1200x1697 pixels portrait. Vertical dynamic layout.
Panel 1 (Top 40%): Bright meeting room. Yuto (Black hair, Gakuran) approaches Remi with a question. Remi (Silver hair, Red eyes, Red blazer) arms crossed, listening. Yuto says "{intro}" (In a speech bubble). Title box: BLACK SLENDER box at bottom-left offset (15% from right) with white text "{title}".
Panel 2 (Middle 30%): Close-up of Remi's face, explaining the core truth. {teach}
Panel 3 (Bottom-Right 30%): Yuto's shock/realization face with shock lines.
Panel 4 (Bottom-Left 30%): Remi's small cool smile.
Art style: Japanese manga style, cel shading, professional quality. Characters: Remi has Silver hair, Red eyes, Red blazer. Yuto has Black Gakuran. NO GLOVES."""

        # プロンプトセクションの置換
        p1_regex = r'## 1ページ目プロンプト\s*\n\s*```text\s*\n(.*?)\n```'
        content = re.sub(p1_regex, f"## 1ページ目プロンプト\n\n```text\n{new_p1}\n```", content, flags=re.DOTALL)

        # 2ページ目のプロンプトもスリム化
        p2_match = re.search(r'## 2ページ目プロンプト\s*\n\s*```text\s*\n(.*?)\n```', content, flags=re.DOTALL)
        if p2_match:
            p2_old = p2_match.group(1)
            # すでにスリム化されていなければ処理
            if "Technical Setup:" not in p2_old and "【IMAGE_GENERATION_TASK】" not in p2_old:
                # DIALOGUE_DESC 等を抽出
                desc_match = re.search(r'\| DIALOGUE_DESC \| (.*?) \|', content)
                desc = desc_match.group(1).strip() if desc_match else "これが本質よ。"
                action_match = re.search(r'\| DIALOGUE_ACTION \| (.*?) \|', content)
                action = action_match.group(1).strip() if action_match else "やってみます！"
                
                new_p2 = f"""{prefix}

PAGE 2 LAYOUT: 1200x1697 pixels portrait. Lecture style.
Panel 1 (Top 50%): Remi in front of a monitor showing '{title}'. Charts and symbolic icons.
Panel 2 (Middle-Right 25%): Vertical panel. Remi emphasizing key points. Speech: "{desc}"
Panel 3 (Middle-Left 25%): Vertical panel. Yuto understanding with visuals.
Panel 4 (Bottom 25%): Wide shot. Yuto determined, Remi proud. Yuto says "{action}".
Colors: GOLD and ROYAL PURPLE theme. Remi: SILVER hair, RED blazer. Yuto: BLACK Gakuran. Cinematic lighting."""
                content = content.replace(p2_old, new_p2)

        # 3. 全体的な微調整（サイズ、比率、キャラ名正規化、不要な見出し削除）
        content = content.replace("1200x1700", "1200x1697")
        content = content.replace("aspect ratio 12:17", "aspect ratio 1200:1697")
        # 重複置換の修正（念のため）
        content = content.replace("Yuto (Boy): Yuto (Boy):", "Yuto (Boy):")
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

count = 0
for root, dirs, files in os.walk(base_dir):
    for name in files:
        if name.endswith("_プロンプト.md"):
            if update_file_safely(os.path.join(root, name)):
                count += 1
print(f"Successfully updated {count} files with variations and slim prompts.")
