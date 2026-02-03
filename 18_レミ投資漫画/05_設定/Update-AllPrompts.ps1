# Update-AllPrompts.ps1
$ErrorActionPreference = "Stop"

$TargetDir = "c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画"
Write-Host "Searching in: $TargetDir" -ForegroundColor Cyan

$Files = Get-ChildItem -Path $TargetDir -Recurse -Filter "No*_プロンプト.md"
Write-Host "Found $($Files.Count) files." -ForegroundColor Cyan

# ヒアドキュメントを使わず、確実に文字列を定義
$AnatomyBlock = "CRITICAL ANATOMICAL REQUIREMENTS:`n" +
"- Each character has EXACTLY TWO HANDS`n" +
"- Each hand has EXACTLY FIVE FINGERS`n" +
"- Remi wears NO GLOVES - bare hands only`n" +
"- Yuto wears NO GLOVES - bare hands only`n" +
"- Anatomically correct human proportions"

$Prefix = "画像生成を行ってください。以下のプロンプトに基づいて、縦長のマンガ画像を生成してください。"

foreach ($File in $Files) {
    Write-Host "Processing $($File.Name)..." -NoNewline
    
    try {
        $Content = Get-Content $File.FullName -Raw -Encoding UTF8
        $OriginalContent = $Content
        
        # 1. 解剖学的要件
        if ($Content -notmatch "CRITICAL ANATOMICAL REQUIREMENTS") {
            $Content = $Content.Replace("Resolution: High quality manga illustration", "Resolution: High quality manga illustration`n`n$AnatomyBlock")
        }
        
        # 2. キャラクター定義 (単純置換)
        $RemiOld = "Remi (Woman): Silky SILVER hair, Vibrant RED eyes, Red blazer, Black lace top, Cool & Intelligent."
        $RemiNew = "Remi (Woman): Silky SILVER hair, Vibrant RED eyes, Red blazer, Black lace top, Cool & Intelligent. BARE HANDS (no gloves)."
        
        if ($Content.Contains($RemiOld)) {
            $Content = $Content.Replace($RemiOld, $RemiNew)
        }
        
        $YutoOld = "Yuto (Boy): Short Black hair, Black GAKURAN school uniform, Energetic & Learner."
        $YutoNew = "Yuto (Boy): Short Black hair, Black GAKURAN school uniform, Energetic & Learner. BARE HANDS (no gloves)."
        
        if ($Content.Contains($YutoOld)) {
            $Content = $Content.Replace($YutoOld, $YutoNew)
        }
        
        # 3. 命令文 (Prefix)の追加
        # 先頭の ```text にマッチさせる
        if ($Content -notmatch "画像生成を行ってください") {
            # 正規表現で置換
            $Content = $Content -replace "(?m)^```text\s*$", "```text`n$Prefix`n"
        }

        if ($Content -ne $OriginalContent) {
            $Content | Set-Content $File.FullName -Encoding UTF8
            Write-Host " DONE" -ForegroundColor Green
        } else {
            Write-Host " SKIP" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host " ERROR: $_" -ForegroundColor Red
    }
}
