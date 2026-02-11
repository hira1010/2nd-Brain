# -*- coding: utf-8 -*-
import os
import re

import manga_config as config

_EXCLUDED_FILE = "00_繧ｹ繝医・繝ｪ繝ｼ讒区・.md"
_ARCH_PATTERN = re.compile(r"ARCHITECTURE: \[v15\.5 EDGE OBLITERATOR\].*?12:17\.")


def _iter_target_markdown_files(base_dir: str):
    for filename in os.listdir(base_dir):
        if not filename.endswith(".md"):
            continue
        if filename == _EXCLUDED_FILE:
            continue
        yield filename, os.path.join(base_dir, filename)


def _apply_replacements(content: str, new_arch_line: str) -> str:
    updated = content

    # Keep original replacement behavior.
    updated = updated.replace(
        "- Yuto: (BLACK Gakuran, gold buttons). (Short Black hair). BARE HANDS.",
        config.CHAR_YUTO,
    )
    updated = updated.replace("- Yuto: (BLACK Gakuran).", "- Yuto: (NAVY BUSINESS SUIT).")
    updated = updated.replace("{Yuto: (BLACK Gakuran)}", "{Yuto: (NAVY BUSINESS SUIT)}")
    updated = _ARCH_PATTERN.sub(new_arch_line, updated)
    updated = updated.replace("Gakuran", "Business Suit")

    return updated


def fix_files() -> None:
    base_dir = config.BASE_DIR
    if not os.path.exists(base_dir):
        print(f"Directory not found: {base_dir}")
        return

    new_arch_line = config.HEADER_TEMPLATE.split("\n", 1)[0]

    for filename, filepath in _iter_target_markdown_files(base_dir):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        fixed_content = _apply_replacements(content, new_arch_line)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(fixed_content)
        print(f"Fixed: {filename}")


if __name__ == "__main__":
    fix_files()
