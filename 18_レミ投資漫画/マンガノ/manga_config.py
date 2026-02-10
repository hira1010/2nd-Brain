# -*- coding: utf-8 -*-
import os

# Base paths
BASE_DIR = os.path.join(os.getcwd(), "01_髟ｷ邱ｨ_蟶梧悍縺ｮ謚戊ｳ・)

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
    {"no": 1, "title": "邨ｶ譛帙・迴ｾ莉｣遉ｾ莨・, "range": "P1-5", "desc": "蠅礼ｨ弱・繝ｳ繝ｻ迚ｩ萓｡鬮倥・繝ｳ縺ｮ隘ｲ譚･縺ｨ縲∝━譁励・邨梧ｸ亥峅遯ｮ縲・},
    {"no": 2, "title": "謳ｾ蜿悶・騾｣骼・, "range": "P6-10", "desc": "謇句叙繧翫∈縺ｮ謾ｻ謦・→縲∝酔蜒夂伐荳ｭ縺ｮFX閾ｪ諷｢縲・},
    {"no": 3, "title": "逕倥＞隱俶ヱ", "range": "P11-15", "desc": "逕ｰ荳ｭ縺ｮ雎ｪ驕翫→蜆ｪ譁励・辟ｦ繧翫ゅΞ繝舌Ξ繝・ず縺ｮ隱俶ヱ縲・},
    {"no": 4, "title": "謨台ｸ紋ｸｻ繝ｬ繝・, "range": "P16-20", "desc": "蜈ｬ蝨偵〒縺ｮ驕句多縺ｮ蜃ｺ莨壹＞縲よｳ｢蜍輔・荵ｱ繧後・謖・遭縲・},
    {"no": 5, "title": "繧ｫ繝｡縺ｮ豁ｩ縺ｿ", "range": "P21-25", "desc": "繝ｬ繝溘↓繧医ｋ謚戊ｳ・蕗閧ｲ髢句ｧ九よ兜讖溘→謚戊ｳ・・驕輔＞縲・},
    {"no": 6, "title": "隍・茜縺ｮ鬲疲ｳ・, "range": "P26-30", "desc": "螳・ｮ呎怙蠑ｷ縺ｮ蜉帙∬､・茜縺ｮ隕冶ｦ壼喧縲・},
    {"no": 7, "title": "闍玲惠繧呈､阪∴繧・, "range": "P31-35", "desc": "驥代・縺ｪ繧区惠縺ｮ闍玲惠繧呈､阪∴繧狗ｲｾ逾樒噪蜆蠑上・},
    {"no": 8, "title": "遨咲ｫ九・髢句ｧ・, "range": "P36-40", "desc": "S&P500縺ｸ縺ｮ蜈･驥代ら伐荳ｭ縺ｮ蜀ｷ隨代・},
    {"no": 9, "title": "蠏舌・莠亥・", "range": "P41-45", "desc": "謨ｰ蟷ｴ蠕後る・ｪｿ縺ｪ謌宣聞縺ｨ逕ｰ荳ｭ縺ｮ逡ｰ蟶ｸ縺ｪ閹ｨ蠑ｵ縲・},
    {"no": 10, "title": "繝悶Λ繝・け繝ｻ繧ｹ繝ｯ繝ｳ", "range": "P46-50", "desc": "證ｴ關ｽ縺ｮ逋ｺ逕溘ゅヮ繧､繧ｺ縺御ｸ也阜繧定ｦ・≧縲・},
    {"no": 11, "title": "逕ｰ荳ｭ縺ｮ騾蝣ｴ", "range": "P51-55", "desc": "繝ｭ繧ｹ繧ｫ繝・ヨ縺ｫ豕｣縺冗伐荳ｭ縲よ兜讖溘・谿矩・縺輔・},
    {"no": 12, "title": "謠｡蜉帙・隧ｦ邱ｴ", "range": "P56-60", "desc": "闍玲惠繧貞ｼ輔″謚懊％縺・→縺吶ｋ蜆ｪ譁励ｒ繝ｬ繝溘′蛻ｶ豁｢縲・},
    {"no": 13, "title": "髱吶°縺ｪ繧句ｿ崎・, "range": "P61-65", "desc": "繝ｬ繝溘・邨千阜縺ｮ荳ｭ縺ｧ縺ｮ豐磯ｻ吶ょ・荳頑・縺ｮ蜈・＠縲・},
    {"no": 14, "title": "蜀咲函縺ｮ邱・, "range": "P66-70", "desc": "譬ｪ萓｡蝗槫ｾｩ縲り距譛ｨ縺御ｻ･蜑阪ｈ繧雁､ｪ縺上↑繧九・},
    {"no": 15, "title": "譛蛻昴・譫懷ｮ・, "range": "P71-75", "desc": "蛻昴ａ縺ｦ縺ｮ驟榊ｽ薙ょ・謚戊ｳ・・蝟懊・縲・},
    {"no": 16, "title": "關ｽ蟾ｮ縺ｮ迴ｾ莉｣", "range": "P76-80", "desc": "繝ｪ繝吶Φ繧ｸFX縺ｧ縺輔ｉ縺ｫ豐医・逕ｰ荳ｭ縺ｨ縺ｮ蟇ｾ豈斐・},
    {"no": 17, "title": "雉・肇縺ｮ逶ｾ", "range": "P81-85", "desc": "雉・肇縺ｨ縺・≧蜷阪・繧ｷ繝ｼ繝ｫ繝峨らｵ梧ｸ医＞髦ｲ蠕｡縺ｮ螳梧・縲・},
    {"no": 18, "title": "鮟・≡縺ｮ豕｢蜍・, "range": "P86-90", "desc": "邊ｾ逾樒噪閾ｪ遶九ゅΞ繝溘′蜆ｪ譁励・謌宣聞繧定ｪ阪ａ繧九・},
    {"no": 19, "title": "20蟷ｴ蠕後・譛・, "range": "P91-95", "desc": "螟ｧ讓ｹ縺ｨ縺ｪ縺｣縺溯ｳ・肇縲り・逕ｱ縺ｪ譎る俣縺ｮ迯ｲ蠕励・},
    {"no": 20, "title": "F-U Money", "range": "P96-100", "desc": "雖後↑縺薙→縺ｫNO縺ｨ險縺医ｋ蜉帙ょｾ瑚ｼｩ縺ｸ縺ｮ莨晄価縲・},
    {"no": 21, "title": "縺企≡縺ｮ譌・ｷｯ", "range": "P101-105", "desc": "繝ｬ繝溘→縺ｮ蟇ｾ隧ｱ縲ゅ♀驥代・謇区ｮｵ縺ｧ縺ゅｋ縺薙→縲・},
    {"no": 22, "title": "閾ｪ蛻・・霄ｫ縺ｮ驕・, "range": "P106-110", "desc": "螟｢縺ｸ縺ｮ蜀肴倦謌ｦ縲ら悄縺ｮ雎翫°縺輔・},
    {"no": 23, "title": "蟶梧悍縺ｮ謚戊ｳ・, "range": "P111-115", "desc": "繧ｨ繝斐Ο繝ｼ繧ｱ縲よｬ｡荳紋ｻ｣縺ｸ郢九＄繝舌ヨ繝ｳ縲・}
]

# Email Settings
EMAIL_SENDER = "hirakura10@gmail.com"
EMAIL_PASSWORD = "Teruki1982@@"
EMAIL_RECEIVER = "hirakura10@mail.com"
EMAIL_SUBJECT = "縲舌Ξ繝滓兜雉・ｼｫ逕ｻ縲代・繝ｳ繧ｬ繝朱聞邱ｨ讒区・繝励Ο繝ｳ繝励ヨ 蜈ｨ23繝輔ぃ繧､繝ｫ"
EMAIL_BODY = "縺顔夢繧梧ｧ倥〒縺吶ゅ＃萓晞ｼ縺・◆縺縺・◆蜈ｨ23繝輔ぃ繧､繝ｫ縺ｮMarkdown繝励Ο繝ｳ繝励ヨ繧呈ｷｻ莉倥↓縺ｦ縺企√ｊ縺励∪縺吶・

# Prompt formatting settings
PROMPT_VERSION = "v15.5 Edge Obliterator"

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
