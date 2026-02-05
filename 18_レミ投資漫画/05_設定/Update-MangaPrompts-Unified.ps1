# Update-MangaPrompts-Unified.ps1
# 3つのPowerShellスクリプトを統合した統一版
# UTF-8 (with BOM) で保存してください

[CmdletBinding()]
param(
    [Parameter()]
    [ValidateSet('Full', 'Slim', 'Safe', 'Standard')]
    [string]$Mode = 'Standard',
    
    [Parameter()]
    [switch]$DryRun,
    
    [Parameter()]
    [switch]$Force,
    
    [Parameter()]
    [string[]]$Skip = @()
)

$ErrorActionPreference = "Stop"

# 共通設定を読み込む
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $ScriptDir "Settings.ps1")

$TargetDir = $Config.Paths.BaseDir
$ModeNameJp = @{
    'Full'     = '完全更新'
    'Slim'     = 'スリム化'
    'Safe'     = '安全更新'
    'Standard' = '標準更新'
}[$Mode]

Write-Host "🚀 漫画プロンプト統合更新スクリプト - モード: $ModeNameJp" -ForegroundColor Cyan
if ($DryRun) { 
    Write-Host "🔍 ドライラン・モード (ファイルは書き換えられません)" -ForegroundColor Yellow 
}
Write-Host ("=" * 70)
Write-Host ""

# 対象ファイルの取得
$Files = Get-ChildItem -Path $TargetDir -Recurse -Filter "No*_プロンプト.md"

if ($null -eq $Files -or $Files.Count -eq 0) {
    Write-Warning "対象ファイルが見つかりませんでした。"
    return
}

$count = 0
$totalFiles = $Files.Count

foreach ($File in $Files) {
    $FileNum = $count + 1
    $FileName = $File.Name
    
    # スキップ処理
    $ShouldSkip = $false
    foreach ($SkipNum in $Skip) {
        if ($FileName -match "No$SkipNum`_") {
            $ShouldSkip = $true
            break
        }
    }
    
    if ($ShouldSkip) {
        Write-Host "⊘ SKIP (指定): $FileName" -ForegroundColor Gray
        continue
    }
    
    Write-Host "[$FileNum/$totalFiles] Processing: $FileName... " -NoNewline
    
    try {
        $RawContent = [System.IO.File]::ReadAllText($File.FullName)
        $CurrentContent = $RawContent
        
        # ========== モード別処理 ==========
        
        switch ($Mode) {
            'Full' {
                # 完全更新: テンプレート適用 + キャラ定義 + スリム化
                
                # データ抽出
                $No = 1
                if ($CurrentContent -match '\| No \| (\d+) \|') { $No = [int]$Matches[1] }
                
                $Title = "投資"
                if ($CurrentContent -match '\| タイトル \| (.*?) \|') { $Title = $Matches[1].Trim() }
                
                $IntroDialog = "教えてください！"
                if ($CurrentContent -match '\| DIALOGUE_INTRO \| (.*?) \|') { $IntroDialog = $Matches[1].Trim() }
                
                $TeachDialog = "いいわよ。"
                if ($CurrentContent -match '\| DIALOGUE_TEACH \| (.*?) \|') { $TeachDialog = $Matches[1].Trim() }
                
                $DescDialog = "これが本質よ。"
                if ($CurrentContent -match '\| DIALOGUE_DESC \| (.*?) \|') { $DescDialog = $Matches[1].Trim() }
                
                $ActionDialog = "やってみます！"
                if ($CurrentContent -match '\| DIALOGUE_ACTION \| (.*?) \|') { $ActionDialog = $Matches[1].Trim() }
                
                # テンプレート適用
                $TemplateP1 = if ($No % 2 -eq 0) { $Config.Prompts.TemplateP1_Remi } else { $Config.Prompts.TemplateP1_Yuto }
                
                $RemiDef = $Config.Characters.Remi.Current
                $YutoDef = $Config.Characters.Yuto.Current
                
                $NL = [Environment]::NewLine
                $NewP1 = $Config.Prompts.Prefix + $NL + $NL + $TemplateP1.Replace("{Title}", $Title).Replace("{IntroDialog}", $IntroDialog).Replace("{TeachDialog}", $TeachDialog).Replace("{Remi_Full}", $RemiDef).Replace("{Yuto_Full}", $YutoDef)
                $NewP2 = $Config.Prompts.Prefix + $NL + $NL + $Config.Prompts.TemplateP2.Replace("{Title}", $Title).Replace("{DescDialog}", $DescDialog).Replace("{ActionDialog}", $ActionDialog).Replace("{Remi_Full}", $RemiDef).Replace("{Yuto_Full}", $YutoDef)
                
                # プロンプトセクションの置換
                $opt = [System.Text.RegularExpressions.RegexOptions]::Singleline
                
                $P1Pattern = "(## 1ページ目プロンプト\s*\n\s*``````text\s*\n).*?(\n``````)"
                $P2Pattern = "(## 2ページ目プロンプト\s*\n\s*``````text\s*\n).*?(\n``````)"
                
                $SafeP1 = $NewP1.Replace('$', '$$')
                $SafeP2 = $NewP2.Replace('$', '$$')
                
                $CurrentContent = [regex]::Replace($CurrentContent, $P1Pattern, ('$1' + $SafeP1 + '$2'), $opt)
                $CurrentContent = [regex]::Replace($CurrentContent, $P2Pattern, ('$1' + $SafeP2 + '$2'), $opt)
            }
            
            'Slim' {
                # スリム化: サイズ修正 + キャラ定義更新 + 見出し簡略化
                
                # サイズと比率
                $CurrentContent = $CurrentContent.Replace("1200x1700", "1200x1697")
                $CurrentContent = $CurrentContent.Replace("1700 pixels height", "1697 pixels height")
                $CurrentContent = $CurrentContent.Replace("aspect ratio 12:17", "aspect ratio 1200:1697")
                $CurrentContent = $CurrentContent.Replace("Aspect Ratio: 12:17", "Aspect Ratio: 1200:1697")
                $CurrentContent = $CurrentContent.Replace("ratio (9:16)", "ratio (1200:1697)")
                
                # キャラクター定義
                $RemiOldPatterns = @(
                    "Remi (Woman): Silky SILVER hair, Vibrant RED eyes, Red blazer, Black lace top, Cool & Intelligent. BARE HANDS (no gloves).",
                    "Remi (Woman): Silky SILVER hair, Red eyes, Red blazer.",
                    "Remi: Silky SILVER hair, Red eyes, Red blazer.",
                    "(Silky SILVER hair:1.5), (Vibrant RED eyes:1.4), (Tailored RED blazer:1.3)",
                    "Remi: (Silky SILVER hair:1.5), (Vibrant RED eyes:1.4), (Tailored RED blazer:1.3)."
                )
                foreach ($Pattern in $RemiOldPatterns) {
                    $CurrentContent = $CurrentContent.Replace($Pattern, $Config.Characters.Remi.Current)
                }
                
                $YutoOldPatterns = @(
                    "Yuto (Boy): Short Black hair, Black GAKURAN school uniform, Energetic & Learner. BARE HANDS (no gloves).",
                    "Yuto (Boy): Short Black hair, Black GAKURAN uniform.",
                    "Yuto: Short Black hair, Black GAKURAN uniform.",
                    "Short Black hair, (Traditional Black GAKURAN school uniform:1.4)",
                    "Yuto: Short Black hair, (Traditional Black GAKURAN school uniform:1.4)."
                )
                foreach ($Pattern in $YutoOldPatterns) {
                    $CurrentContent = $CurrentContent.Replace($Pattern, $Config.Characters.Yuto.Current)
                }
                
                # 見出しの簡略化
                $CurrentContent = $CurrentContent.Replace("MANDATORY IMAGE SPECIFICATIONS:", "Technical Setup:")
                $CurrentContent = $CurrentContent.Replace("CRITICAL ANATOMICAL REQUIREMENTS:", "Character Anatomy:")
                $CurrentContent = $CurrentContent.Replace("PANEL LAYOUT - PAGE 1:", "Page 1 Layout:")
                $CurrentContent = $CurrentContent.Replace("PANEL LAYOUT - PAGE 2:", "Page 2 Layout:")
                $CurrentContent = $CurrentContent.Replace("STYLE SPECIFICATIONS:", "Art Style:")
                $CurrentContent = $CurrentContent.Replace("TEXT BOX REQUIREMENT:", "Title Box Design:")
            }
            
            'Safe' {
                # 安全更新: 解剖学的要件追加 + BARE HANDS追加のみ
                
                # 解剖学的要件
                if ($CurrentContent -notmatch "CRITICAL ANATOMICAL REQUIREMENTS") {
                    $CurrentContent = $CurrentContent.Replace("Resolution: High quality manga illustration", "Resolution: High quality manga illustration`n`n$($Config.Prompts.AnatomyBlock)")
                }
                
                # キャラクター定義（BARE HANDSがない場合のみ追加）
                $RemiOld = "Remi (Woman): Silky SILVER hair, Vibrant RED eyes, Red blazer, Black lace top, Cool & Intelligent."
                if ($CurrentContent -match [regex]::Escape($RemiOld) -and $CurrentContent -notmatch "BARE HANDS") {
                    $CurrentContent = $CurrentContent.Replace($RemiOld, $Config.Characters.Remi.Current)
                }
                
                $YutoOld = "Yuto (Boy): Short Black hair, Black GAKURAN school uniform, Energetic & Learner."
                if ($CurrentContent -match [regex]::Escape($YutoOld) -and $CurrentContent -notmatch "BARE HANDS") {
                    $CurrentContent = $CurrentContent.Replace($YutoOld, $Config.Characters.Yuto.Current)
                }
                
                # Prefix追加
                if ($CurrentContent -notmatch [regex]::Escape($Config.Prompts.Prefix)) {
                    $PrefixLine = "``````text`n$($Config.Prompts.Prefix)`n"
                    $CurrentContent = $CurrentContent -replace "(?m)^``````text\s*$", $PrefixLine
                }
            }
            
            'Standard' {
                # 標準更新: 解剖学的要件 + キャラ定義 + タイトル + Prefix
                
                # 解剖学的要件
                if ($CurrentContent -notmatch "CRITICAL ANATOMICAL REQUIREMENTS") {
                    $CurrentContent = $CurrentContent.Replace("Resolution: High quality manga illustration", "Resolution: High quality manga illustration`n`n$($Config.Prompts.AnatomyBlock)")
                }
                
                # キャラクター定義
                $CurrentContent = $CurrentContent.Replace($Config.Characters.Remi.Old, $Config.Characters.Remi.Current)
                $CurrentContent = $CurrentContent.Replace($Config.Characters.Yuto.Old, $Config.Characters.Yuto.Current)
                
                # タイトル調整
                $CurrentContent = $CurrentContent.Replace($Config.Prompts.TitleOld, $Config.Prompts.TitleNew)
                
                # Prefix追加
                if ($CurrentContent -notmatch [regex]::Escape($Config.Prompts.Prefix)) {
                    $PrefixLine = "``````text`n$($Config.Prompts.Prefix)`n"
                    $CurrentContent = $CurrentContent -replace "(?m)^``````text\s*$", $PrefixLine
                }
            }
        }
        
        # ========== 共通スリム化処理（全モード共通）==========
        foreach ($Entry in $Config.Prompts.SlimmingReplacements.GetEnumerator()) {
            $CurrentContent = $CurrentContent.Replace($Entry.Key, $Entry.Value)
        }
        
        # 変更があれば保存
        if ($CurrentContent -ne $RawContent) {
            if (-not $DryRun) {
                [System.IO.File]::WriteAllText($File.FullName, $CurrentContent, [System.Text.Encoding]::UTF8)
            }
            Write-Host "✓ DONE" -ForegroundColor Green
            $count++
        }
        else {
            Write-Host "⊘ NO CHANGE" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "✗ ERROR: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host ("=" * 70)
$Action = if ($DryRun) { "更新予定" } else { "更新" }
Write-Host "✅ 完了: $count/$totalFiles ファイルを$Action" -ForegroundColor Cyan
Write-Host ("=" * 70)
