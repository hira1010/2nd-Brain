import os
import re
import manga_utils as utils

# Templates
TEMPLATE_1P_PATH = r"c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画\05_設定\00_漫画生成テンプレート_1P.md"
TEMPLATE_2P_PATH = r"c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画\05_設定\00_漫画生成テンプレート_2P.md"

def load_template(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

TEMPLATE_1P = load_template(TEMPLATE_1P_PATH)
TEMPLATE_2P = load_template(TEMPLATE_2P_PATH)

def generate_visual_instruction(title, description):
    """
    Generates a default visual instruction based on the title/description.
    """
    return f"Draw a conceptual illustration representing '{description}'."

def process_file(filepath):
    content = utils.read_file(filepath)
    meta = utils.parse_metadata(content)
    
    if 'number' not in meta:
        print(f"Skipping {filepath}: No number found.")
        return False
        
    # Determine Page Count
    # Default to 2, unless explicit 'page_count' in meta implies 1
    # OR if it's No.28 (Hardcoded special case if needed, but meta is better)
    page_count = int(meta.get('page_count', 2))
    
    # Select Template
    if page_count == 1:
        template = TEMPLATE_1P
    else:
        template = TEMPLATE_2P

    # Prepare Variables
    number = meta.get('number', '00')
    title = meta.get('title', 'Untitled')
    description = meta.get('description', 'No description')
    category = meta.get('category', 'Uncategorized')
    
    # Dialogues
    d_theme = f"優斗君、今日は『{title}』について教えるわよ。"
    d_teach_1 = meta.get('dialogue_teach', f"いい心がけね。でも、ただ知るだけじゃ意味がないわ。 つまり、{description}")
    d_action_1 = "なるほど…！ イメージできました！"
    
    d_summary = f"{description} これが投資の本質よ。しっかり頭に叩き込みなさい。"
    d_action_2 = f"そうか…{title}の本質はここにあったんですね。"
    
    # Visual Instructions (Try to preserve existing if available, otherwise generate)
    # Since we are essentially rewriting, we don't have "existing" visual instructions in a structured way 
    # unless we parse the old prompt block. 
    # For now, we will generate a generic one that the user can fill in.
    # OR we can try to be smart.
    
    visual_1 = generate_visual_instruction(title, description)
    visual_2 = "(Use symbolic imagery to represent the concept)"

    # Replacements
    new_content = template.replace("{NUMBER}", str(number))
    new_content = new_content.replace("{TITLE}", title)
    new_content = new_content.replace("{DESCRIPTION}", description)
    new_content = new_content.replace("{CATEGORY}", category)
    
    # Dialogue Replacements
    new_content = new_content.replace("{DIALOGUE_THEME}", d_theme)
    new_content = new_content.replace("{DIALOGUE_TEACH_1}", d_teach_1)
    new_content = new_content.replace("{DIALOGUE_ACTION_1}", d_action_1)
    
    if page_count > 1:
        new_content = new_content.replace("{DIALOGUE_SUMMARY}", d_summary)
        new_content = new_content.replace("{DIALOGUE_ACTION_2}", d_action_2)
        new_content = new_content.replace("{VISUAL_INSTRUCTION_2}", visual_2)

    new_content = new_content.replace("{VISUAL_INSTRUCTION_1}", visual_1)
    
    # Write Back
    utils.write_file(filepath, new_content)
    print(f"Updated {filepath} (Page Count: {page_count})")
    return True

def main():
    base_dir = r"c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画"
    count = 0
    for filepath in utils.find_manga_prompt_files(base_dir):
        # SKIP No26 and No28 as they are already manually handled/verified
        if "No26_" in filepath or "No28_" in filepath:
            print(f"Skipping {filepath} (Manually handled)")
            continue
            
        try:
            if process_file(filepath):
                count += 1
        except Exception as e:
            print(f"Error processing {filepath}: {e}")

    print(f"Done. Updated {count} files.")

if __name__ == "__main__":
    main()
