# -*- coding: utf-8 -*-
import os
import re

# Base directory for the manga files
BASE_DIR = r"c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画\マンガノ\01_長編_希望の投資"

# Character and Style Updates
OLD_YUTO = r"- Yuto: \(BLACK Gakuran, gold buttons\)\. \(Short Black hair\)\. BARE HANDS\."
NEW_YUTO = "- Yuto: (NAVY BUSINESS SUIT, white shirt, ties). (Short Black hair). Salaryman attire."

# Stronger Vertical Instruction
OLD_ARCH = r"ARCHITECTURE: \[v15\.5 EDGE OBLITERATOR\] FULL BLEED\. ZERO PIXEL MARGINS\. 110% OVERFILL\. 12:17\."
NEW_ARCH = "ARCHITECTURE: [v15.5 EDGE OBLITERATOR] FULL BLEED. ZERO PIXEL MARGINS. 110% OVERFILL. **VERTICAL PORTRAIT ORIENTATION. 12:17 RATIO.**"

def fix_files():
    if not os.path.exists(BASE_DIR):
        print(f"Directory not found: {BASE_DIR}")
        return

    for filename in os.listdir(BASE_DIR):
        if filename.endswith(".md") and filename != "00_ストーリー構成.md":
            filepath = os.path.join(BASE_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Replace Yuto's description (regex or direct string)
            # Handling both escaped and non-escaped versions just in case
            content = content.replace("- Yuto: (BLACK Gakuran, gold buttons). (Short Black hair). BARE HANDS.", NEW_YUTO)
            content = content.replace("- Yuto: (BLACK Gakuran).", "- Yuto: (NAVY BUSINESS SUIT).")
            content = content.replace("{Yuto: (BLACK Gakuran)}", "{Yuto: (NAVY BUSINESS SUIT)}")
            
            # Use regex for more flexible replacement of the architecture line
            content = re.sub(r"ARCHITECTURE: \[v15\.5 EDGE OBLITERATOR\].*?12:17\.", NEW_ARCH, content)

            # Fix any other mentions of Gakuran
            content = content.replace("Gakuran", "Business Suit")

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {filename}")

if __name__ == "__main__":
    fix_files()
