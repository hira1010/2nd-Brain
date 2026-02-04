# Settings.ps1 - レミ投資漫画 共通設定
# このファイルは UTF-8 (with BOM) で保存ください。

$Config = @{
    # ディレクトリパス
    Paths      = @{
        BaseDir    = "c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画"
        ConfigDir  = "c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画\05_設定"
        ContentDir = "c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画\01_投資の基礎知識"
    }

    # キャラクター定義
    Characters = @{
        Remi = @{
            Name    = "Remi"
            Current = "Remi (SIGNATURE OUTFIT: Always wearing a Tailored RED blazer over a Black lace top, no variations allowed). (Silky SILVER hair:1.5), (Vibrant RED eyes:1.4). NO GLOVES."
        }
        Yuto = @{
            Name    = "Yuto"
            Current = "Yuto (Boy): Short Black hair, (Traditional Black GAKURAN school uniform:1.4), Gold buttons. Energetic learner. BARE HANDS (no gloves)."
            Old     = @(
                "Yuto (Boy): Short Black hair, Black GAKURAN school uniform, Energetic & Learner. BARE HANDS (no gloves).",
                "Yuto (Boy): Short Black hair, Black GAKURAN uniform.",
                "Yuto: Short Black hair, Black GAKURAN uniform.",
                "Yuto: Short Black hair, (Traditional Black GAKURAN school uniform:1.4)."
            )
        }
    }

    # プロンプトテンプレート
    Prompts    = @{
        Prefix               = "【IMAGE_GENERATION_TASK】Generate a high-quality manga illustration BASE ON THE FOLLOWING VISUAL DESCRIPTION. DO NOT OUTPUT ANY TEXT OR CODE. ONLY OUTPUT THE IMAGE."
        
        # 1ページ目：優斗主導（奇数No）
        TemplateP1_Yuto      = "### INSTRUCTION: DO NOT DRAW ANY ENGLISH TEXT. ONLY JAPANESE IN SPEECH BUBBLES.`n### CHARACTER SETTING`n- Remi: {Remi_Full}`n- Yuto: {Yuto_Full}`n### PAGE LAYOUT (Portrait 1200x1697)`nPanel 1: Yuto and Remi in a meeting room. Yuto says `"{IntroDialog}`" in a Japanese speech bubble. Title box: Black slender box with white Japanese text `"{Title}`".`nPanel 2: Extreme Close-up of Remi's red eyes. She says `"{TeachDialog}`" in a Japanese speech bubble.`nPanel 3: Yuto with manga shock lines.`nPanel 4: Remi smiling coolly.`n### STYLE: Japanese manga, cel shaded. NO GLOVES."

        # 1ページ目：レミ主導（偶数No）
        TemplateP1_Remi      = "### INSTRUCTION: DO NOT DRAW ANY ENGLISH TEXT. ONLY JAPANESE IN SPEECH BUBBLES.`n### CHARACTER SETTING`n- Remi: {Remi_Full}`n- Yuto: {Yuto_Full}`n### PAGE LAYOUT (Portrait 1200x1697)`nPanel 1: Remi pointing at whiteboard, Yuto taking notes. Remi says `"優斗君、今日は『{Title}』について教えるわよ。`" in a Japanese speech bubble. Title box: Black box with white Japanese text `"{Title}`".`nPanel 2: Remi explaining concepts. She says `"{TeachDialog}`" in a Japanese speech bubble.`nPanel 3: Yuto nodding. `"はい、レミさん！`" in a bubble.`nPanel 4: Remi's side profile.`n### STYLE: Japanese manga, cel shaded. NO GLOVES."

        # 2ページ目共通
        TemplateP2           = "### INSTRUCTION: DO NOT DRAW ANY ENGLISH TEXT. ONLY JAPANESE IN SPEECH BUBBLES.`n### CHARACTER SETTING`n- Remi: {Remi_Full}`n- Yuto: {Yuto_Full}`n### PAGE LAYOUT (Portrait 1200x1697)`nPanel 1: EPIC METAPHOR SCENE. Remi navigating a symbolic world of '{Title}' (e.g. cosmic/oceanic). Digital charts in background. Remi has absolute authority.`nPanel 2: Remi making a sharp gesture. She says `"{DescDialog}`" in a Japanese speech bubble.`nPanel 3: Yuto visualizing profit with golden icons.`nPanel 4: Yuto determined, Remi proud. Yuto says `"{ActionDialog}`" in a bubble. Remi thinks `"期待しているわよ。`" in a small thoughts bubble.`n### STYLE: Cinematic lighting, Gold/Purple theme. NO GLOVES."
        
        # スリム化用置換パターン
        SlimmingReplacements = @{
            "1200x1700"                         = "1200x1697"
            "1700 pixels height"                = "1697 pixels height"
            "aspect ratio 12:17"                = "aspect ratio 1200:1697"
            "MANDATORY IMAGE SPECIFICATIONS:"   = "Technical Setup:"
            "CRITICAL ANATOMICAL REQUIREMENTS:" = "Character Anatomy:"
            "PANEL LAYOUT - PAGE 1:"            = "Page 1 Layout:"
            "PANEL LAYOUT - PAGE 2:"            = "Page 2 Layout:"
            "STYLE SPECIFICATIONS:"             = "Art Style:"
            "TEXT BOX REQUIREMENT:"             = "Title Box Design:"
        }
    }

    # 画像設定
    Image      = @{
        Width       = 1200
        Height      = 1697
        AspectRatio = "1200:1697"
    }
}
