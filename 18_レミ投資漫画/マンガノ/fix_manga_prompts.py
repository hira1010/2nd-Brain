# -*- coding: utf-8 -*-
import os
import re
import manga_config as config

def fix_files():
    if not os.path.exists(config.BASE_DIR):
        print(f"Directory not found: {config.BASE_DIR}")
        return

    for filename in os.listdir(config.BASE_DIR):
        if filename.endswith(".md") and filename != "00_スト�Eリー構�E.md":
            filepath = os.path.join(config.BASE_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Using centralized logic is tricky because this is a *fix* script that 
            # might be looking for OLD strings to replace with NEW ones.
            # The original script had hardcoded OLD strings. We should keep them or define them in config if they are constants.
            # However, for checking against the NEW definitions, we should use config.
            
            # Note: The original script's regex replacement logic for Architecture is:
            # content = re.sub(r"ARCHITECTURE: \[v15\.5 EDGE OBLITERATOR\].*?12:17\.", NEW_ARCH, content)
            # We need to construct NEW_ARCH from config or just use the header part.
            
            # Let's extract the header first line from config.HEADER_TEMPLATE for replacement
            # But the original script had a specific string for NEW_ARCH.
            # Let's see: NEW_ARCH = "ARCHITECTURE: ... **VERTICAL PORTRAIT ORIENTATION. 12:17 RATIO.**"
            # This matches the first line of config.HEADER_TEMPLATE (mostly).
            
            new_arch_line = config.HEADER_TEMPLATE.split('\n')[0]
            
            # Replace Yuto's description
            # We can use config.CHAR_YUTO as the target replacement
            content = content.replace("- Yuto: (BLACK Gakuran, gold buttons). (Short Black hair). BARE HANDS.", config.CHAR_YUTO)
            content = content.replace("- Yuto: (BLACK Gakuran).", "- Yuto: (NAVY BUSINESS SUIT).")
            content = content.replace("{Yuto: (BLACK Gakuran)}", "{Yuto: (NAVY BUSINESS SUIT)}")
            
            # Architecture replacement
            content = re.sub(r"ARCHITECTURE: \[v15\.5 EDGE OBLITERATOR\].*?12:17\.", new_arch_line, content)

            # Fix any other mentions of Gakuran
            content = content.replace("Gakuran", "Business Suit")

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {filename}")

if __name__ == "__main__":
    fix_files()
