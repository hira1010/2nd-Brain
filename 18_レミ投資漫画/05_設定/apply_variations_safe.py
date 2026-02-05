import re
import os
import manga_config as config
import manga_utils as utils

def update_file_safely(filepath):
    try:
        content = utils.read_file(filepath)
        if not content.strip():
            print(f"Skipping empty file: {filepath}")
            return False
            
        # 1. Parse Metadata
        meta = utils.parse_metadata(content)
        if 'number' not in meta:
            return False

        no = int(meta['number'])
        title = meta.get('title', '投資')
        
        # Logic to fix "She's not explaining"
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
        
        # 2. 1ページ目のプロンプト内容自体をスリム化＆バリエーション化
        if no % 2 == 0:
            # 偶数：レミ主導
            new_p1 = f"""{config.PREFIX}

PAGE 1 LAYOUT: 1200x1697 pixels portrait. Vertical dynamic layout.
Panel 1 (Top 40%): Bright meeting room. Remi (Silver hair, Red eyes, Red blazer) stands confidently, pointing at a whiteboard to start a surprise lecture. Yuto (Black hair, Gakuran) looks surprised but eager. Remi says "優斗君、今日は『{title}』について教えるわよ。しっかり聞きなさい。" (In a speech bubble). Title box: BLACK SLENDER box at bottom-left offset (15% from right) with white text "{title}".
Panel 2 (Middle 30%): Close-up of Remi's face, explaining authoritative yet kindly. {dialogue_teach}
Panel 3 (Bottom-Right 30%): Yuto looking impressed and nodding. "はい、レミさん！"
Panel 4 (Bottom-Left 30%): Remi's mysterious side profile.
Art style: Japanese manga style, cel shading, professional quality. Characters: Remi has Silver hair, Red eyes, Red blazer. Yuto has Black Gakuran. NO GLOVES."""
        else:
            # 奇数：優斗主導
            new_p1 = f"""{config.PREFIX}

PAGE 1 LAYOUT: 1200x1697 pixels portrait. Vertical dynamic layout.
Panel 1 (Top 40%): Bright meeting room. Yuto (Black hair, Gakuran) approaches Remi with a question. Remi (Silver hair, Red eyes, Red blazer) arms crossed, listening. Yuto says "{dialogue_intro}" (In a speech bubble). Title box: BLACK SLENDER box at bottom-left offset (15% from right) with white text "{title}".
Panel 2 (Middle 30%): Close-up of Remi's face, explaining the core truth. {dialogue_teach}
Panel 3 (Bottom-Right 30%): Yuto's shock/realization face with shock lines.
Panel 4 (Bottom-Left 30%): Remi's small cool smile.
Art style: Japanese manga style, cel shading, professional quality. Characters: Remi has Silver hair, Red eyes, Red blazer. Yuto has Black Gakuran. NO GLOVES."""

        # プロンプトセクションの置換
        # Use Regex to allow updating even if file content changed slightly
        new_content = content
        p1_regex = r'## 1ページ目プロンプト\s*\n\s*```text\s*\n(.*?)\n```'
        new_content = re.sub(p1_regex, f"## 1ページ目プロンプト\n\n```text\n{new_p1}\n```", new_content, flags=re.DOTALL)

        # 2ページ目のプロンプトもスリム化
        new_p2 = f"""{config.PREFIX}

PAGE 2 LAYOUT: 1200x1697 pixels portrait. Lecture style.
Panel 1 (Top 50%): Remi in front of a monitor showing '{title}'. Charts and symbolic icons.
Panel 2 (Middle-Right 25%): Vertical panel. Remi emphasizing key points. Speech: "{dialogue_desc}"
Panel 3 (Middle-Left 25%): Vertical panel. Yuto understanding with visuals.
Panel 4 (Bottom 25%): Wide shot. Yuto determined, Remi proud. Yuto says "{dialogue_action}".
Colors: GOLD and ROYAL PURPLE theme. Remi: SILVER hair, RED blazer. Yuto: BLACK Gakuran. Cinematic lighting."""

        p2_regex = r'## 2ページ目プロンプト\s*\n\s*```text\s*\n(.*?)\n```'
        
        # Only replace if the safe script intends to replace all (original script had some conditional logic but here we enforcing consistency as requested by 'overall refactoring')
        # Original: if "Technical Setup:" not in p2_old ...
        # Since I am refactoring, I will standardize usage.
        
        new_content = re.sub(p2_regex, f"## 2ページ目プロンプト\n\n```text\n{new_p2}\n```", new_content, flags=re.DOTALL)

        if new_content != content:
            utils.write_file(filepath, new_content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

count = 0
for filepath in utils.find_manga_prompt_files(config.BASE_DIR):
    if update_file_safely(filepath):
        count += 1
print(f"Successfully updated {count} files with variations and slim prompts.")
