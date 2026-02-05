import manga_config as config

class MangaPromptBuilder:
    def __init__(self, metadata):
        self.meta = metadata
        self.no = int(metadata.get('number', 0))
        self.title = metadata.get('title', 'Unknown Title')
        self.page_count = int(metadata.get('page_count', 2))
        
        # Dialogues
        self.dialogue_intro = metadata.get('dialogue_intro', '')
        self.dialogue_desc = metadata.get('dialogue_desc', '')
        
        # Teach Dialogue Logic (Ported from apply_variations.py)
        d_teach = metadata.get('dialogue_teach', '')
        d_desc = metadata.get('description', '')
        
        generic_phrases = ["いい心がけね", "詳細を教えるわ", "いいわよ", "聞いて驚きなさい", "Description"]
        is_generic = any(phrase in d_teach for phrase in generic_phrases)

        if is_generic and d_desc and d_desc != d_teach:
            self.dialogue_teach = f"{d_teach} つまり、{d_desc}"
        else:
            self.dialogue_teach = d_teach

    def build_page1(self):
        layout_desc = "PAGE 1 LAYOUT" if self.page_count > 1 else "PAGE LAYOUT"
        
        # Decide Template
        if self.no % 2 == 0:
            template = config.P1_LAYOUT_REMI_LEAD
        else:
            template = config.P1_LAYOUT_YUTO_LEAD
            
        return f"{config.PREFIX}\n\n" + template.format(
            layout_desc=layout_desc,
            title=self.title,
            dialogue_intro=self.dialogue_intro,
            dialogue_teach=self.dialogue_teach,
            visual_bridge=config.P1_VISUAL_BRIDGE,
            reaction=config.P1_REACTION,
            art_style=config.ART_STYLE_COMMON
        )

    def build_page2(self):
        if self.page_count <= 1:
            return None
            
        return f"{config.PREFIX}\n\n" + config.P2_LAYOUT.format(
            title=self.title,
            dialogue_desc=self.dialogue_desc,
            reaction=config.P2_REACTION,
            remi_think=config.P2_THINK_REMI,
            art_style=config.ART_STYLE_P2
        )
