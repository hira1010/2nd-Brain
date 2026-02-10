# -*- coding: utf-8 -*-
import sys
import manga_config as config
import manga_utils as utils

# Ensure stdout handles utf-8
sys.stdout.reconfigure(encoding='utf-8')

def generate():
    utils.ensure_directory(config.BASE_DIR)
    
    for ep in config.EPISODES:
        filepath = utils.get_episode_filename(ep, config.BASE_DIR)
        
        start_p = int(ep['range'].split('-')[0].replace('P', ''))
        end_p = int(ep['range'].split('-')[1])
        
        pages_content = ""
        for p in range(start_p, end_p + 1):
            pages_content += config.PROMPT_TEMPLATE.format(
                p=p,
                version=config.PROMPT_VERSION,
                version_upper=config.PROMPT_VERSION.upper(),
                ep_no=ep['no'],
                desc=ep['desc'],
                title=ep['title']
            )

        content = f"""# No102 Episode {ep['no']}: {ep['title']} ({ep['range']})

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
        utils.save_text_file(filepath, content)

if __name__ == "__main__":
    generate()
