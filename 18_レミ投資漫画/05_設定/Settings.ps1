# Settings.ps1 - レミ投資漫画 共通設定
# このファイルは UTF-8 (with BOM) で保存してください。

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
            Old = "Remi (Woman): Silky SILVER hair, Vibrant RED eyes, Red blazer, Black lace top, Cool & Intelligent. BARE HANDS (no gloves)."
            New = "Remi (Woman): (Silky SILVER hair:1.5), (Vibrant RED eyes:1.4), (Sharp almond-shaped eyes:1.2). Wearing (Tailored RED blazer:1.3) over black lace top. Cool, intelligent, and authoritative. BARE HANDS (no gloves)."
        }
        Yuto = @{
            Old = "Yuto (Boy): Short Black hair, Black GAKURAN school uniform, Energetic & Learner. BARE HANDS (no gloves)."
            New = "Yuto (Boy): Short Black hair, (Traditional Black GAKURAN school uniform:1.4), Gold buttons. Energetic learner. BARE HANDS (no gloves)."
        }
    }

    # プロンプト定数
    Prompts    = @{
        AnatomyBlock = "CRITICAL ANATOMICAL REQUIREMENTS:`n- Each character has EXACTLY TWO HANDS`n- Each hand has EXACTLY FIVE FINGERS`n- Remi wears NO GLOVES - bare hands only`n- Yuto wears NO GLOVES - bare hands only`n- Anatomically correct human proportions"
        Prefix       = "画像生成を行ってください。以下のプロンプトに基づいて、縦長のマンガ画像を生成してください。"
        
        TitleOld     = "In Panel 1, BOTTOM-RIGHT corner: Draw a BLACK rectangular box with WHITE border containing WHITE TEXT:`n複利`nFont: Bold, Clear Japanese Gothic font."
        TitleNew     = "In Panel 1, BOTTOM-RIGHT corner: Draw a COMPACT BLACK rectangular box with tight white border containing WHITE TEXT:`n複利`nFont: Bold, Clear Japanese Gothic font. Layout: Single line, minimal vertical padding."
    }

    # 画像設定
    Image      = @{
        Width  = 1200
        Height = 1700
    }
}

function Get-ProjectRoot {
    # スクリプトの場所から親ディレクトリを辿ってプロジェクトルートを特定する（将来的な相対パス化用）
    return $Config.Paths.BaseDir
}
