import os
import re

target_dir = r"c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画"
anatomy_block = """CRITICAL ANATOMICAL REQUIREMENTS:
- Each character has EXACTLY TWO HANDS
- Each hand has EXACTLY FIVE FINGERS
- Remi wears NO GLOVES - bare hands only
- Yuto wears NO GLOVES - bare hands only
- Anatomically correct human proportions"""

prefix_text = "画像生成を行ってください。以下のプロンプトに基づいて、縦長のマンガ画像を生成してください。"

remi_old = "Remi (Woman): Silky SILVER hair, Vibrant RED eyes, Red blazer, Black lace top, Cool & Intelligent."
remi_new = "Remi (Woman): Silky SILVER hair, Vibrant RED eyes, Red blazer, Black lace top, Cool & Intelligent. BARE HANDS (no gloves)."

yuto_old = "Yuto (Boy): Short Black hair, Black GAKURAN school uniform, Energetic & Learner."
yuto_new = "Yuto (Boy): Short Black hair, Black GAKURAN school uniform, Energetic & Learner. BARE HANDS (no gloves)."

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content

    # 1. 解剖学的要件の追加
    if "CRITICAL ANATOMICAL REQUIREMENTS" not in content:
        target = "Resolution: High quality manga illustration"
        content = content.replace(target, f"{target}\n\n{anatomy_block}")

    # 2. キャラクター定義の更新 (Remi)
    if remi_old in content and "BARE HANDS" not in content[content.find(remi_old):content.find(remi_old)+200]:
        content = content.replace(remi_old, remi_new)

    # 3. キャラクター定義の更新 (Yuto)
    if yuto_old in content and "BARE HANDS" not in content[content.find(yuto_old):content.find(yuto_old)+200]:
        content = content.replace(yuto_old, yuto_new)

    # 4. 命令プレフィックスの追加
    # ```text の直後に prefix_text がなければ追加
    # re.sub で最初の出現のみに限定せず、全ての ```text ブロックに適用
    def add_prefix(match):
        block_content = match.group(1)
        if prefix_text not in block_content:
            return f"```text\n{prefix_text}\n{block_content}```"
        return match.group(0)

    content = re.sub(r"```text\n(.*?)```", add_prefix, content, flags=re.DOTALL)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

count = 0
updated_count = 0
for root, dirs, files in os.walk(target_dir):
    for file in files:
        if file.startswith("No") and file.endswith("_プロンプト.md"):
            count += 1
            if update_file(os.path.join(root, file)):
                updated_count += 1

print(f"Total files found: {count}")
print(f"Files updated: {updated_count}")
