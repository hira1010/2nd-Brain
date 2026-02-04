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
            Current = "Remi (Woman): (Silky SILVER hair:1.5), (Vibrant RED eyes:1.4), (Sharp almond-shaped eyes:1.2). Wearing (Tailored RED blazer:1.3) over black lace top. Cool, intelligent, and authoritative. BARE HANDS (no gloves)."
            Old     = @(
                "Remi (Woman): Silky SILVER hair, Vibrant RED eyes, Red blazer, Black lace top, Cool & Intelligent. BARE HANDS (no gloves).",
                "Remi (Woman): Silky SILVER hair, Red eyes, Red blazer.",
                "Remi: Silky SILVER hair, Red eyes, Red blazer.",
                "Remi: (Silky SILVER hair:1.5), (Vibrant RED eyes:1.4), (Tailored RED blazer:1.3)."
            )
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
        TemplateP1_Yuto      = "PAGE 1 LAYOUT: 1200x1697 pixels portrait. Vertical dynamic layout.`nPanel 1 (Top 40%): Bright meeting room. Yuto (Black hair, Gakuran) approaches Remi with a question. Remi (Silver hair, Red eyes, Red blazer) arms crossed, listening. Yuto says `"{IntroDialog}`" (In a speech bubble). Title box: BLACK SLENDER box at bottom-left offset (15% from right) with white text `"{Title}`".`nPanel 2 (Middle 30%): Close-up of Remi's face, explaining the core truth. {TeachDialog}`nPanel 3 (Bottom-Right 30%): Yuto's shock/realization face with shock lines.`nPanel 4 (Bottom-Left 30%): Remi's small cool smile.`nArt style: Japanese manga style, cel shading, professional quality. Characters: Remi has Silver hair, Red eyes, Red blazer. Yuto has Black Gakuran. NO GLOVES."

        # 1ページ目：レミ主導（偶数No）
        TemplateP1_Remi      = "PAGE 1 LAYOUT: 1200x1697 pixels portrait. Vertical dynamic layout.`nPanel 1 (Top 40%): Bright meeting room. Remi (Silver hair, Red eyes, Red blazer) stands confidently, pointing at a whiteboard to start a surprise lecture. Yuto (Black hair, Gakuran) looks surprised but eager. Remi says `"優斗君、今日は『{Title}』について教えるわよ。しっかり聞きなさい。`" (In a speech bubble). Title box: BLACK SLENDER box at bottom-left offset (15% from right) with white text `"{Title}`".`nPanel 2 (Middle 30%): Close-up of Remi's face, explaining authoritative yet kindly. {TeachDialog}`nPanel 3 (Bottom-Right 30%): Yuto looking impressed and nodding. `"はい、レミさん！`" `nPanel 4 (Bottom-Left 30%): Remi's mysterious side profile.`nArt style: Japanese manga style, cel shading, professional quality. Characters: Remi has Silver hair, Red eyes, Red blazer. Yuto has Black Gakuran. NO GLOVES."

        # 2ページ目共通
        TemplateP2           = "PAGE 2 LAYOUT: 1200x1697 pixels portrait. Lecture style.`nPanel 1 (Top 50%): Remi in front of a monitor showing '{Title}'. Charts and symbolic icons.`nPanel 2 (Middle-Right 25%): Vertical panel. Remi emphasizing key points. Speech: `"{DescDialog}`"`nPanel 3 (Middle-Left 25%): Vertical panel. Yuto understanding with visuals.`nPanel 4 (Bottom 25%): Wide shot. Yuto determined, Remi proud. Yuto says `"{ActionDialog}`".`nColors: GOLD and ROYAL PURPLE theme. Remi: SILVER hair, RED blazer. Yuto: BLACK Gakuran. Cinematic lighting."
        
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
