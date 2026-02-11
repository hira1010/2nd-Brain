# -*- coding: utf-8 -*-
import sys
from typing import Dict, List

import manga_config as config
import manga_utils as utils

# Ensure stdout handles utf-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def _build_pages_content(ep: Dict[str, object]) -> str:
    start_page, end_page = utils.parse_page_range(str(ep["range"]))
    pages: List[str] = []
    for page in range(start_page, end_page + 1):
        pages.append(
            config.PROMPT_TEMPLATE.format(
                p=page,
                version=config.PROMPT_VERSION,
                version_upper=config.PROMPT_VERSION.upper(),
                ep_no=ep["no"],
                desc=ep["desc"],
                title=ep["title"],
            )
        )
    return "".join(pages)


def _build_markdown(ep: Dict[str, object], pages_content: str) -> str:
    return f"""# No102 Episode {ep['no']}: {ep['title']} ({ep['range']})

## TIP諠・ｱ

| 鬆・岼 | 蜀・ｮｹ |
| :--- | :--- |
| EP | {ep['no']} |
| 繧ｿ繧､繝医Ν | {ep['title']} |
| 隗｣隱ｬ | {ep['desc']} |

---

{pages_content}

菴懈・譌･: 2026-02-07
繧ｹ繝・・繧ｿ繧ｹ: {ep['range']} {config.PROMPT_VERSION} 螳悟ｙ
"""


def generate() -> None:
    utils.ensure_directory(config.BASE_DIR)

    for ep in config.EPISODES:
        filepath = utils.get_episode_filename(ep, config.BASE_DIR)
        pages_content = _build_pages_content(ep)
        content = _build_markdown(ep, pages_content)
        utils.save_text_file(filepath, content)


if __name__ == "__main__":
    generate()
