# -*- coding: utf-8 -*-
import os
import sys

# Ensure stdout handles utf-8
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.join(os.getcwd(), "01_\u9577\u7de8_\u5e0c\u671b\u306e\u6295\u8cc7")
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

# Characters
CHAR_REMI = "- Remi: (Crimson RED blazer, Black lace top). (LONG STARK STRAIGHT SILVER hair). (GLOWING SOLID BLOOD-RED eyes). NO GLOVES."
CHAR_YUTO = "- Yuto: (BLACK Gakuran, gold buttons). (Short Black hair). BARE HANDS."
CHAR_TANAKA = "- Tanaka: (Arrogant Japanese man, dark suit, loose tie). (Short messy brown hair). (Sneering smirk)."
CHAR_ZOUZEI = "- Zouzei-man: (Massive monster made of tax forms and coins). (Glowing purple eyes)."
CHAR_BUKKADAKA = "- Bukkadaka-man: (Bloated monster with red price tags). (Gaping sharp-toothed mouth)."
CHAR_MONEYTREE = "- MoneyTree: (Radiant golden tree/sapling). (Golden light aura)."
CHAR_NOISE = "- Noise: (Swirling black and purple mist with ghostly faces)."

HEADER = f"""ARCHITECTURE: [v15.5 EDGE OBLITERATOR] FULL BLEED. ZERO PIXEL MARGINS. 110% OVERFILL. 12:17.

### Characters:
{CHAR_REMI}
{CHAR_YUTO}
{CHAR_TANAKA}
{CHAR_ZOUZEI}
{CHAR_BUKKADAKA}
{CHAR_MONEYTREE}
{CHAR_NOISE}

### Style: Premium manga, cinematic lighting, masterpiece, sharp focus, high contrast. 12:17 ratio. **CORE**: OBLITERATE ALL CANVAS MARGINS. FULL BLEED.
**NEGATIVE PROMPT**: white edges, side bars, pillarbox, letterbox, black bars, gutter, split screen, frame, border, text labels, low quality, blurry, margins, padding, cropped.
"""

episodes = [
    {"no": 1, "title": "\u7d76\u671b\u306e\u73fe\u4ee3\u793e\u4f1a", "range": "P1-5", "desc": "\u5897\u7a0e\u30de\u30f3\u30fb\u7269\u4fa1\u9ad8\u30de\u30f3\u306e\u8972\u6765\u3068\u3001\u512a\u6597\u306e\u7d4c\u6e08\u3004\u56f0\u7aae\u3002"},
    {"no": 2, "title": "\u643e\u53d6\u306e\u9023\u9396", "range": "P6-10", "desc": "\u624b\u53d6\u308a\u3078\u306e\u653b\u6483\u3068\u3001\u540c\u50da\u7530\u4e2d\u306eFX\u81ea\u6162\u3002"},
    {"no": 3, "title": "\u7518\u3044\u8a98\u60d1", "range": "P11-15", "desc": "\u7530\u4e2d\u306e\u8c6a\u904a\u3068\u512a\u6597\u306e\u7126\u308a\u3002\u30ec\u30d0\u30ec\u30c3\u30b8\u306e\u8a98\u60d1\u3002"},
    {"no": 4, "title": "\u6551\u4e16\u4e3b\u30ec\u30df", "range": "P16-20", "desc": "\u516c\u5712\u3067\u306e\u904b\u547d\u306e\u51fa\u4f1a\u3044\u3002\u6ce2\u52d5\u306e\u4e71\u308c\u306e\u6307\u6458\u3002"},
    {"no": 5, "title": "\u30ab\u30e1\u306e\u6b69\u307f", "range": "P21-25", "desc": "\u30ec\u30df\u306b\u3088\u308b\u6295\u8cc7\u6559\u80b2\u958b\u59cb\u3002\u6295\u6a5f\u3068\u6295\u8cc7\u306e\u9055\u3044\u3002"},
    {"no": 6, "title": "\u8907\u5229\u306e\u9b54\u6cd5", "range": "P26-30", "desc": "\u5b87\u5b99\u6700\u5f37\u306e\u529b\u3001\u8907\u5229\u306e\u8996\u899a\u5316\u3002"},
    {"no": 7, "title": "\u82d7\u6728\u3092\u690d\u3048\u308b", "range": "P31-35", "desc": "\u91d1\u306e\u306a\u308b\u6728\u306e\u82d7\u6728\u3092\u690d\u3048\u308b\u7cbe\u795e\u7684\u5100\u5f0f\u3002"},
    {"no": 8, "title": "\u7a4d\u7acb\u306e\u958b\u59cb", "range": "P36-40", "desc": "S&P500\u3078\u306e\u5165\u91d1\u3002\u7530\u4e2d\u306e\u51b7\u7b11\u3002"},
    {"no": 9, "title": "\u5d50\u306e\u4e88\u5146", "range": "P41-45", "desc": "\u6570\u5e74\u5f8c\u3002\u9806\u8abf\u306a\u6210\u9577\u3068\u7530\u4e2d\u306e\u7570\u5e38\u306a\u81a8\u5f35\u3002"},
    {"no": 10, "title": "\u30d6\u30e9\u30c3\u30af\u30fb\u30b9\u30ef\u30f3", "range": "P46-50", "desc": "\u66b4\u843d\u306e\u767a\u751f\u3002\u30ce\u30a4\u30ba\u304c\u4e16\u754c\u3092\u8986\u3046\u3002"},
    {"no": 11, "title": "\u7530\u4e2d\u306e\u9000\u5834", "range": "P51-55", "desc": "\u30ed\u30b9\u30ab\u30c3\u30c8\u306b\u6ce3\u304f\u7530\u4e2d\u3002\u6295\u6a5f\u306e\u6b8b\u9177\u3055\u3002"},
    {"no": 12, "title": "\u63e1\u529b\u306e\u8a66\u7df4", "range": "P56-60", "desc": "\u82d7\u6728\u3092\u5f15\u304d\u629c\u3053\u3046\u3068\u3059\u308b\u512a\u6597\u3092\u30ec\u30d0\u304c\u5236\u6b62\u3002"},
    {"no": 13, "title": "\u9759\u304b\u306a\u308b\u5fcd\u8010", "range": "P61-65", "desc": "\u30ec\u30df\u306e\u7d50\u754c\u306e\u4e2d\u3067\u306e\u6c88\u9ed9\u3002\u518d\u4e0a\u6607\u306e\u5146\u3057\u3002"},
    {"no": 14, "title": "\u518d\u751f\u306e\u7dd1", "range": "P66-70", "desc": "\u682a\u4fa1\u56de\u5fa9\u3002\u82d7\u6728\u304c\u4ee5\u524d\u3088\u308a\u592a\u304f\u306a\u308b\u3002"},
    {"no": 15, "title": "\u6700\u521d\u306e\u679c\u5b9f", "range": "P71-75", "desc": "\u521d\u3081\u3066\u306e\u914d\u5f53\u3002\u518d\u6295\u8cc7\u306e\u559c\u3073\u3002"},
    {"no": 16, "title": "\u843d\u5dee\u306e\u73fe\u4ee3", "range": "P76-80", "desc": "\u30ea\u30d9\u30f3\u30b8FX\u3067\u3055\u3089\u306b\u6c88\u3080\u7530\u4e2d\u3068\u306e\u5bfe\u6bd4\u3002"},
    {"no": 17, "title": "\u8cc7\u7523\u306e\u76fe", "range": "P81-85", "desc": "\u8cc7\u7523\u3068\u3044\u3046\u540d\u306e\u30b7\u30fc\u30eb\u30c9\u3002\u7d4c\u6e08\u3044\u9632\u5fa1\u306e\u5b8c\u6210\u3002"},
    {"no": 18, "title": "\u9ec4\u91d1\u306e\u6ce2\u52d5", "range": "P86-90", "desc": "\u7cbe\u795e\u7684\u81ea\u7acb\u3002\u30ec\u30df\u304c\u512a\u6597\u306e\u6210\u9577\u3092\u8a8d\u3081\u308b\u3002"},
    {"no": 19, "title": "20\u5e74\u5f8c\u306e\u671d", "range": "P91-95", "desc": "\u5927\u6a39\u3068\u306a\u3063\u305f\u8cc7\u7523\u3002\u81ea\u7531\u306a\u6642\u9593\u306e\u7372\u5f97\u3002"},
    {"no": 20, "title": "F-U Money", "range": "P96-100", "desc": "\u5acc\u306a\u3053\u3068\u306bNO\u3068\u8a00\u3048\u308b\u529b\u3002\u5f8c\u8f29\u3078\u306e\u4f1d\u627f\u3002"},
    {"no": 21, "title": "\u304a\u91d1\u306e\u65c5\u8def", "range": "P101-105", "desc": "\u30ec\u30df\u3068\u306e\u5bfe\u8a71\u3002\u304a\u91d1\u306f\u624b\u6bb5\u3067\u3042\u308b\u3053\u3068\u3002"},
    {"no": 22, "title": "\u81ea\u5206\u81ea\u8eab\u306e\u9053", "range": "P106-110", "desc": "\u5922\u3078\u306e\u518d\u6311\u6226\u3002\u771f\u306e\u8c4a\u304b\u3055\u3002"},
    {"no": 23, "title": "\u5e0c\u671b\u306e\u6295\u8cc7", "range": "P111-115", "desc": "\u30a8\u30d4\u30ed\u30fc\u30b1\u3002\u6b21\u4e16\u4ee3\u3078\u7e4b\u3050\u30d0\u30c8\u30f3\u3002"}
]

def generate():
    for ep in episodes:
        title_escaped = ep['title'].replace('/', '_').replace(' ', '_')
        filename = f"No102_{ep['no']:02d}_{title_escaped}_{ep['range']}_\u30d7\u30ed\u30f3\u30d7\u30c8.md"
        filepath = os.path.join(BASE_DIR, filename)
        
        start_p = int(ep['range'].split('-')[0].replace('P', ''))
        end_p = int(ep['range'].split('-')[1])
        
        pages_content = ""
        for p in range(start_p, end_p + 1):
            pages_content += f"""---

## {p} \u30da\u30fc\u30b8\u76ee\u30d7\u30ed\u30f3\u30d7\u30c8 (v15.5 Edge Obliterator)

```javascript
generate_image(
  ImageName: "remi_102_ep{ep['no']}_p{p}_final",
  Prompt: "ARCHITECTURE: [v15.5 EDGE OBLITERATOR] FULL BLEED. ZERO PIXEL MARGINS. 12:17. Characters: {{Remi}}, {{Yuto}}, {{Tanaka}}, {{Villains}}. [PANEL 1 - 40% height]: FULL WIDTH FILL. {ep['desc']}. Detailed 2D anime style. [PANEL 2 - 35% height]: FULL WIDTH FILL. Interaction in {ep['title']}. Blank speech bubbles. [PANEL 3 - 25% height]: FULL WIDTH FILL. Symbolic background. Cinematic lighting."
)
```

"""

        content = f"""# No102 Episode {ep['no']}: {ep['title']} ({ep['range']})

## TIP\u60c5\u5831

| \u9805\u76ee | \u5185\u5bb9 |
| :--- | :--- |
| EP | {ep['no']} |
| \u30bf\u30a4\u30c8\u30eb | {ep['title']} |
| \u89e3\u8aac | {ep['desc']} |

---

{pages_content}

\u4f5c\u6210\u65e5: 2026-02-07
\u30b9\u30c6\u30fc\u30bf\u30b9: {ep['range']} v15.5 Edge Obliterator \u5b8c\u5099
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Generated: {filename}")

if __name__ == "__main__":
    generate()
