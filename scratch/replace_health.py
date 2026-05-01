import os

root_dir = r"c:\Users\hirak\My project (3)\Assets\Scripts"
target_word = "Health"
replacement_word = "AntigravityHealth"

for filename in os.listdir(root_dir):
    if filename.endswith(".cs"):
        filepath = os.path.join(root_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 単語境界を意識して置換
        import re
        new_content = re.sub(r'\b' + target_word + r'\b', replacement_word, content)
        
        if content != new_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated: {filename}")
