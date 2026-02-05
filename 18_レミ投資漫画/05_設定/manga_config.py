import os

# Base Directory for the 2nd Brain Manga Project
# Using relative path from this script location (18_レミ投資漫画/05_設定/manga_config.py -> 18_レミ投資漫画)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Image Generation Task Prefix
PREFIX = "【IMAGE_GENERATION_TASK】Generate a high-quality manga illustration BASE ON THE FOLLOWING VISUAL DESCRIPTION. DO NOT OUTPUT ANY TEXT OR CODE. ONLY OUTPUT THE IMAGE."

# Layout Instructions
NEW_TITLE_BOX_INSTRUCTION = "In Panel 1, at the BOTTOM, positioned slightly to the LEFT of the bottom-right corner (approx. 15% away from the right edge): Draw a SLENDER BLACK rectangular box with a thin WHITE border. The box should be THINNER and vertical-compact with tight padding around the WHITE TEXT:"

# Character Definitions (Source of Truth)
# Based on apply_slim_prompts.py and apply_variations.py
REMI_DEF = "Remi (Woman): (Silky SILVER hair:1.5), (Vibrant RED eyes:1.4), (Sharp almond-shaped eyes:1.2). Wearing (Tailored RED blazer:1.3) over black lace top. Cool, intelligent, and authoritative. BARE HANDS (no gloves)."
YUTO_DEF = "Yuto (Boy): Short Black hair, (Traditional Black GAKURAN school uniform:1.4), Gold buttons. Energetic learner. BARE HANDS (no gloves)."

# Anatomy Block (for reference if needed)
ANATOMY_BLOCK = """Character Anatomy:
- Each character has EXACTLY TWO HANDS
- Each hand has EXACTLY FIVE FINGERS
- Remi wears NO GLOVES - bare hands only
- Yuto wears NO GLOVES - bare hands only
- Anatomically correct human proportions"""

# Page 1 Constants
P1_REACTION = "なるほど…！\\nイメージできました！"
P1_VISUAL_BRIDGE = "イメージで捉えるとこういうことよ。"

# Page 2 Constants
P2_REACTION = "深く胸に刻みます…！"
P2_THINK_REMI = "期待しているわよ。"

# Art Style
ART_STYLE_COMMON = "Art style: Japanese manga style, cel shading, bright colors. Characters: Remi has Silver hair, Red eyes, Red blazer. Yuto has Black Gakuran. NO GLOVES."
ART_STYLE_P2 = "Art style: Cinematic lighting, Gold/Purple theme. NO GLOVES."

# Layout Templates
# Note: These are format strings expecting {title}, {dialogue_teach}, etc.
P1_LAYOUT_REMI_LEAD = """{layout_desc}: 1200x1697 pixels portrait. Flow: Theme -> Explain -> Visual -> Understand.
Panel 1 (Top 25%): THEME INTRO. Bright office. Remi (Silver hair, Red blazer) introduces the topic "{title}". Yuto (Black hair, Gakuran) listens. Remi says "優斗君、今日は『{title}』について教えるわよ。" Title box: BLACK SLENDER box with "{title}".
Panel 2 (Middle-Top 25%): EXPLANATION. Close-up of Remi teaching. She gives the verbal definition. She says "{dialogue_teach}" (In a speech bubble).
Panel 3 (Middle-Bottom 35%): VISUAL EXPLANATION. A clear conceptual illustration/metaphor of '{title}'. Remi is present, pointing at the visual. She says "{visual_bridge}"
Panel 4 (Bottom 15%): UNDERSTANDING. Yuto nodding with a "Eureka" expression, looking at the visual. "{reaction}"
{art_style}"""

P1_LAYOUT_YUTO_LEAD = """{layout_desc}: 1200x1697 pixels portrait. Flow: Theme -> Explain -> Visual -> Understand.
Panel 1 (Top 25%): THEME INTRO. Yuto asks about "{title}". Remi listens. Yuto says "{dialogue_intro}". Title box: BLACK SLENDER box with "{title}".
Panel 2 (Middle-Top 25%): EXPLANATION. Remi explains the answer verbally. She says "{dialogue_teach}" (In a speech bubble).
Panel 3 (Middle-Bottom 35%): VISUAL EXPLANATION. A large visual metaphor of '{title}' appears. Remi points to it. She says "{visual_bridge}"
Panel 4 (Bottom 15%): UNDERSTANDING. Yuto looks enlightened by the image. "{reaction}"
{art_style}"""

P2_LAYOUT = """PAGE 2 LAYOUT: 1200x1697 pixels portrait.
Panel 1 (Top 40%): EPIC METAPHOR SCENE. Remi (in RED blazer) navigating a symbolic world representing '{title}'. Digital charts or abstract visuals completely surround her. She has absolute authority here.
Panel 2 (Middle 30%): VISUAL MANIFESTATION of the dialogue. The background vividly illustrates the concept: "{dialogue_desc}". Remi explains it within this visualized world. She says "{dialogue_desc}" (In a speech bubble).
Panel 3 (Bottom-Right 15%): Yuto visualizing his own future success based on this advice. Golden icons or happy future self imagery.
Panel 4 (Bottom-Left 15%): Yuto determined, Remi proud. Yuto says "{reaction}" (In a speech bubble). Remi thinks "{remi_think}" (In a thought bubble).
{art_style}"""
