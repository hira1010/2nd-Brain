# Update-AllPrompts.ps1
$ErrorActionPreference = "Stop"

$TargetDir = "c:\Users\hirak\Desktop\2nd-Brain\18_繝ｬ繝滓兜雉・ｼｫ逕ｻ"
Write-Host "Searching in: $TargetDir" -ForegroundColor Cyan

$Files = Get-ChildItem -Path $TargetDir -Recurse -Filter "No*_繝励Ο繝ｳ繝励ヨ.md"
Write-Host "Found $($Files.Count) files." -ForegroundColor Cyan

# 繝偵い繝峨く繝･繝｡繝ｳ繝医ｒ菴ｿ繧上★縲∫｢ｺ螳溘↓譁・ｭ怜・繧貞ｮ夂ｾｩ
$AnatomyBlock = "CRITICAL ANATOMICAL REQUIREMENTS:`n" +
"- Each character has EXACTLY TWO HANDS`n" +
"- Each hand has EXACTLY FIVE FINGERS`n" +
"- Remi wears NO GLOVES - bare hands only`n" +
"- Yuto wears NO GLOVES - bare hands only`n" +
"- Anatomically correct human proportions"

$Prefix = "逕ｻ蜒冗函謌舌ｒ陦後▲縺ｦ縺上□縺輔＞縲ゆｻ･荳九・繝励Ο繝ｳ繝励ヨ縺ｫ蝓ｺ縺･縺・※縲∫ｸｦ髟ｷ縺ｮ繝槭Φ繧ｬ逕ｻ蜒上ｒ逕滓・縺励※縺上□縺輔＞縲・

foreach ($File in $Files) {
    Write-Host "Processing $($File.Name)..." -NoNewline
    
    try {
        $Content = Get-Content $File.FullName -Raw -Encoding UTF8
        $OriginalContent = $Content
        
        # 1. 隗｣蜑門ｭｦ逧・ｦ∽ｻｶ
        if ($Content -notmatch "CRITICAL ANATOMICAL REQUIREMENTS") {
            $Content = $Content.Replace("Resolution: High quality manga illustration", "Resolution: High quality manga illustration`n`n$AnatomyBlock")
        }
        
        # 2. 繧ｭ繝｣繝ｩ繧ｯ繧ｿ繝ｼ螳夂ｾｩ (蜊倡ｴ皮ｽｮ謠・
        $RemiOld = "Remi (Woman): Silky SILVER hair, Vibrant RED eyes, Red blazer, Black lace top, Cool & Intelligent. BARE HANDS (no gloves)."
        $RemiNew = "Remi (Woman): (Silky SILVER hair:1.5), (Vibrant RED eyes:1.4), (Sharp almond-shaped eyes:1.2). Wearing (Tailored RED blazer:1.3) over black lace top. Cool, intelligent, and authoritative. BARE HANDS (no gloves)."
        
        if ($Content.Contains($RemiOld)) {
            $Content = $Content.Replace($RemiOld, $RemiNew)
        }
        
        $YutoOld = "Yuto (Boy): Short Black hair, Black GAKURAN school uniform, Energetic & Learner. BARE HANDS (no gloves)."
        $YutoNew = "Yuto (Boy): Short Black hair, (Traditional Black GAKURAN school uniform:1.4), Gold buttons. Energetic learner. BARE HANDS (no gloves)."
        
        if ($Content.Contains($YutoOld)) {
            $Content = $Content.Replace($YutoOld, $YutoNew)
        }

        # 2.5 隍・茜繧ｿ繧､繝医Ν縺ｮ隱ｿ謨ｴ (繧ｳ繝ｳ繝代け繝亥喧)
        $TitleOld = "In Panel 1, BOTTOM-RIGHT corner: Draw a BLACK rectangular box with WHITE border containing WHITE TEXT:`n隍・茜`nFont: Bold, Clear Japanese Gothic font."
        $TitleNew = "In Panel 1, BOTTOM-RIGHT corner: Draw a COMPACT BLACK rectangular box with tight white border containing WHITE TEXT:`n隍・茜`nFont: Bold, Clear Japanese Gothic font. Layout: Single line, minimal vertical padding."
        
        if ($Content.Contains($TitleOld)) {
            $Content = $Content.Replace($TitleOld, $TitleNew)
        }
        
        # 3. 蜻ｽ莉､譁・(Prefix)縺ｮ霑ｽ蜉
        # 蜈磯ｭ縺ｮ ```text 縺ｫ繝槭ャ繝√＆縺帙ｋ
        if ($Content -notmatch "逕ｻ蜒冗函謌舌ｒ陦後▲縺ｦ縺上□縺輔＞") {
            # 豁｣隕剰｡ｨ迴ｾ縺ｧ鄂ｮ謠・
            $Content = $Content -replace "(?m)^```text\s*$", "```text`n$Prefix`n"
        }

        if ($Content -ne $OriginalContent) {
            $Content | Set-Content $File.FullName -Encoding UTF8
            Write-Host " DONE" -ForegroundColor Green
        }
        else {
            Write-Host " SKIP" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host " ERROR: $_" -ForegroundColor Red
    }
}
