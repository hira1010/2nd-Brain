import re
import manga_config as config
import manga_utils as utils

def update_file(filepath):
    content = utils.read_file(filepath)
    original_content = content

    # 1. 解剖学的要件の追加
    if "Character Anatomy:" not in content and "CRITICAL ANATOMICAL REQUIREMENTS" not in content:
        # Note: manga_config.ANATOMY_BLOCK uses "Character Anatomy:"
        # If the file uses old format, we might want to standardize.
        target = "Resolution: High quality manga illustration"
        content = content.replace(target, f"{target}\n\n{config.ANATOMY_BLOCK}")

    # 2. キャラクター定義の更新 (Remi)
    # This script seems to have been doing targeted replacement.
    # While apply_slim_prompts does full replacement.
    # We will keep the logic similar but use config values.
    # However, replacing specific "old strings" with new config.
    
    # Actually, let's just do what the script tried to do: Ensure Bare Hands.
    # But since we have config.REMI_DEF which includes bare hands, we can try to replace known old definitions.
    
    # For now, let's stick to the specific logic of specific strings if they exist.
    remi_old = "Remi (Woman): Silky SILVER hair, Vibrant RED eyes, Red blazer, Black lace top, Cool & Intelligent."
    if remi_old in content and "BARE HANDS" not in content[content.find(remi_old):content.find(remi_old)+200]:
        content = content.replace(remi_old, config.REMI_DEF) # Note: This might replace with a string that doesn't match the old surrounding exactly if old prompt was different.
        # But REPO seems to be moving towards using the standard DEF everywhere.

    yuto_old = "Yuto (Boy): Short Black hair, Black GAKURAN school uniform, Energetic & Learner."
    if yuto_old in content and "BARE HANDS" not in content[content.find(yuto_old):content.find(yuto_old)+200]:
        content = content.replace(yuto_old, config.YUTO_DEF)

    # 3. 命令プレフィックスの追加
    def add_prefix(match):
        block_content = match.group(1)
        if config.PREFIX not in block_content and "【IMAGE_GENERATION_TASK】" not in block_content:
             return f"```text\n{config.PREFIX}\n{block_content}```"
        return match.group(0)

    content = re.sub(r"```text\n(.*?)```", add_prefix, content, flags=re.DOTALL)

    if content != original_content:
        utils.write_file(filepath, content)
        return True
    return False

count = 0
updated_count = 0
for filepath in utils.find_manga_prompt_files(config.BASE_DIR):
    count += 1
    if update_file(filepath):
        updated_count += 1

print(f"Total files found: {count}")
print(f"Files updated: {updated_count}")
