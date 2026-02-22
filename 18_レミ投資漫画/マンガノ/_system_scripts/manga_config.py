# -*- coding: utf-8 -*-
import os

# Base paths
# Calculate BASE_DIR relative to this script file
# Script is in: .../マンガノ/_system_scripts
# Content is in: .../マンガノ/01_長編_希望の投資
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_MANGANO_DIR = os.path.dirname(_SCRIPT_DIR)
BASE_DIR = os.path.join(_MANGANO_DIR, "01_長編_希望の投資")
STORY_DIR = os.path.join(BASE_DIR, "01_ストーリー")

# Ensure they exist
if not os.path.exists(BASE_DIR):
    # Fallback or just warning
    print(f"Warning: BASE_DIR not found at {BASE_DIR}")

# Characters
CHAR_REMI = "- Remi: (Crimson RED blazer, Black lace top). (LONG STARK STRAIGHT SILVER hair). (GLOWING SOLID BLOOD-RED eyes). NO GLOVES."
CHAR_YUTO = "- Yuto: (NAVY BUSINESS SUIT, white shirt, ties). (Short Black hair). Salaryman attire."
CHAR_TANAKA = "- Tanaka: (Arrogant Japanese man, dark suit, loose tie). (Short messy brown hair). (Sneering smirk)."
CHAR_ZG = "- Zouzei-man: (Massive monster made of tax forms and coins). (Glowing purple eyes)."
CHAR_BUKKADAKA = "- Bukkadaka-man: (Bloated monster with red price tags). (Gaping sharp-toothed mouth)."
CHAR_MONEYTREE = "- MoneyTree: (Radiant golden tree/sapling). (Golden light aura)."
CHAR_NOISE = "- Noise: (Swirling black and purple mist with ghostly faces)."

# Header / Style
HEADER_TEMPLATE = """ARCHITECTURE: [v15.5 EDGE OBLITERATOR] FULL BLEED. ZERO PIXEL MARGINS. 110% OVERFILL. **VERTICAL PORTRAIT ORIENTATION. 12:17 RATIO.**

### Characters:
{remi}
{yuto}
{tanaka}
{zouzei}
{bukkadaka}
{moneytree}
{noise}

### Style: Premium manga, cinematic lighting, masterpiece, sharp focus, high contrast. 12:17 ratio. **CORE**: OBLITERATE ALL CANVAS MARGINS. FULL BLEED.
**NEGATIVE PROMPT**: white edges, side bars, pillarbox, letterbox, black bars, gutter, split screen, frame, border, text labels, low quality, blurry, margins, padding, cropped.
"""

# Episodes List
EPISODES = [
    {"no": 1, "title": "絶望の現代社会", "range": "P1-5", "desc": "増税マン・物価高マンの襲来と、優斗の経済困窮。"},
    {"no": 2, "title": "搾取の連鎖", "range": "P6-10", "desc": "手取りへの攻撃と、同僚田中のFX自慢。"},
    {"no": 3, "title": "甘い誘惑", "range": "P11-15", "desc": "田中の豪遊と優斗の焦り。レバレッジの誘惑。"},
    {"no": 4, "title": "救世主レミ", "range": "P16-20", "desc": "公園での運命の出会い。波動の乱れの指摘。"},
    {"no": 5, "title": "カメの歩み", "range": "P21-25", "desc": "レミによる投資教育開始。投機と投資の違い。"},
    {"no": 6, "title": "複利の魔法", "range": "P26-30", "desc": "宇宙最強の力、複利の視覚化。"},
    {"no": 7, "title": "苗木を植える", "range": "P31-35", "desc": "金のなる木の苗木を植える精神的儀式。"},
    {"no": 8, "title": "積立の開始", "range": "P36-40", "desc": "S&P500への入金。田中の冷笑。"},
    {"no": 9, "title": "嵐の予兆", "range": "P41-45", "desc": "数年後。順調な成長と田中の異常な膨張。"},
    {"no": 10, "title": "ブラック・スワン", "range": "P46-50", "desc": "暴落の発生。ノイズが世界を覆う。"},
    {"no": 11, "title": "田中の退場", "range": "P51-55", "desc": "ロスカットに泣く田中。投機の残酷さ。"},
    {"no": 12, "title": "握力の試練", "range": "P56-60", "desc": "苗木を引き抜こうとする優斗をレミが制止。"},
    {"no": 13, "title": "静かなる忍耐", "range": "P61-65", "desc": "レミの結界の中での沈黙。再上昇の兆し。"},
    {"no": 14, "title": "再生の緑", "range": "P66-70", "desc": "株価回復。苗木が以前より太くなる。"},
    {"no": 15, "title": "最初の果実", "range": "P71-75", "desc": "初めての配当。再投資の喜び。"},
    {"no": 16, "title": "落差の現実", "range": "P76-80", "desc": "リベンジFXでさらに沈む田中との対比。"},
    {"no": 17, "title": "資産の盾", "range": "P81-85", "desc": "資産という名のシールド。経済い防御の完成。"},
    {"no": 18, "title": "黄金の波動", "range": "P86-90", "desc": "精神的自立。レミが優斗の成長を認める。"},
    {"no": 19, "title": "20年後の朝", "range": "P91-95", "desc": "大樹となった資産。自由な時間の獲得。"},
    {"no": 20, "title": "F-U Money", "range": "P96-100", "desc": "嫌なことにNOと言える力。後輩への伝承。"},
    {"no": 21, "title": "お金の旅路", "range": "P101-105", "desc": "レミとの対話。お金は手段であること。"},
    {"no": 22, "title": "自分自身の道", "range": "P106-110", "desc": "夢への再挑戦。真の豊かさ。"},
    {"no": 23, "title": "希望の投資", "range": "P111-115", "desc": "エピローグ。次世代へ繋ぐバトン。"}
]

# Email Settings
EMAIL_SENDER = "hirakura10@gmail.com"
EMAIL_PASSWORD = "Teruki1982@@"
EMAIL_RECEIVER = "hirakura10@mail.com"
EMAIL_SUBJECT = "【レミ投資漫画】マンガノ長編構成プロンプト 全23ファイル"
EMAIL_BODY = "お疲れ様です。ご依頼いただいた全23ファイルのMarkdownプロンプトを添付にてお送りします。"

# Prompt formatting settings
PROMPT_VERSION = "v15.5 Edge Obliterator"
PROMPT_TEMPLATE = """---

## {p} ページ目プロンプト ({version})

```javascript
generate_image(
  ImageName: "remi_102_ep{ep_no}_p{p}_final",
  Prompt: "ARCHITECTURE: [{version_upper}] FULL BLEED. ZERO PIXEL MARGINS. 12:17. Characters: {{{{Remi}}}}, {{{{Yuto}}}}, {{{{Tanaka}}}}, {{{{Villains}}}}. [PANEL 1 - 40% height]: FULL WIDTH FILL. {desc}. Detailed 2D anime style. [PANEL 2 - 35% height]: FULL WIDTH FILL. Interaction in {title}. Blank speech bubbles. [PANEL 3 - 25% height]: FULL WIDTH FILL. Symbolic background. Cinematic lighting."
)
```

"""

def get_header():
    return HEADER_TEMPLATE.format(
        remi=CHAR_REMI,
        yuto=CHAR_YUTO,
        tanaka=CHAR_TANAKA,
        zouzei=CHAR_ZG,
        bukkadaka=CHAR_BUKKADAKA,
        moneytree=CHAR_MONEYTREE,
        noise=CHAR_NOISE
    )
