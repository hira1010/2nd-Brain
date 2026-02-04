# Update-MangaPrompts.ps1 - 全プロンプトの一括更新（統合・強化版）
[CmdletBinding()]
param(
    [Parameter()]
    [switch]$Force,

    [Parameter()]
    [switch]$DryRun
)

# 1. 環境準備
. (Join-Path $PSScriptRoot "Settings.ps1")

Write-Host "🚀 統合プロンプト更新開始..." -ForegroundColor Cyan
if ($DryRun) { Write-Host "🔍 ドライラン・モード (ファイルは書き換えられません)" -ForegroundColor Yellow }

$Files = Get-ChildItem -Path $Config.Paths.BaseDir -Recurse -Filter "No*_プロンプト.md"
if ($null -eq $Files -or $Files.Count -eq 0) {
    Write-Warning "対象ファイルが見つかりませんでした。"
    return
}

$count = 0
$totalFiles = $Files.Count

foreach ($File in $Files) {
    Write-Host "[$($count+1)/$totalFiles] Processing: $($File.Name)... " -NoNewline
    try {
        $RawContent = [System.IO.File]::ReadAllText($File.FullName)
        $CurrentContent = $RawContent
        
        # 2. データ抽出
        $No = 1; if ($CurrentContent -match '\| No \| (\d+) \|') { $No = [int]$Matches[1] }
        $Title = "投資"; if ($CurrentContent -match '\| タイトル \| (.*?) \|') { $Title = $Matches[1].Trim() }
        $IntroDialog = "教えてください！"; if ($CurrentContent -match '\| DIALOGUE_INTRO \| (.*?) \|') { $IntroDialog = $Matches[1].Trim() }
        $TeachDialog = "いいわよ。"; if ($CurrentContent -match '\| DIALOGUE_TEACH \| (.*?) \|') { $TeachDialog = $Matches[1].Trim() }
        $DescDialog = "これが本質よ。"; if ($CurrentContent -match '\| DIALOGUE_DESC \| (.*?) \|') { $DescDialog = $Matches[1].Trim() }
        $ActionDialog = "やってみます！"; if ($CurrentContent -match '\| DIALOGUE_ACTION \| (.*?) \|') { $ActionDialog = $Matches[1].Trim() }

        # 3. テンプレート適用 (1P目/2P目)
        $TemplateP1 = if ($No % 2 -eq 0) { $Config.Prompts.TemplateP1_Remi } else { $Config.Prompts.TemplateP1_Yuto }
        
        $RemiDef = $Config.Characters.Remi.Current
        $YutoDef = $Config.Characters.Yuto.Current

        $NL = [Environment]::NewLine
        $NewP1 = $Config.Prompts.Prefix + $NL + $NL + $TemplateP1.Replace("{Title}", $Title).Replace("{IntroDialog}", $IntroDialog).Replace("{TeachDialog}", $TeachDialog).Replace("{Remi_Full}", $RemiDef).Replace("{Yuto_Full}", $YutoDef)
        $NewP2 = $Config.Prompts.Prefix + $NL + $NL + $Config.Prompts.TemplateP2.Replace("{Title}", $Title).Replace("{DescDialog}", $DescDialog).Replace("{ActionDialog}", $ActionDialog).Replace("{Remi_Full}", $RemiDef).Replace("{Yuto_Full}", $YutoDef)

        # 4. キャラクター定義の更新 (旧形式の全置換)
        foreach ($Char in $Config.Characters.Values) {
            foreach ($OldDef in $Char.Old) {
                # 文字列として置換
                $CurrentContent = $CurrentContent.Replace($OldDef, $Char.Current)
            }
        }

        # 5. スリム化と共通置換 (Settings.ps1 から取得)
        foreach ($Entry in $Config.Prompts.SlimmingReplacements.GetEnumerator()) {
            $CurrentContent = $CurrentContent.Replace($Entry.Key, $Entry.Value)
        }

        # 6. プロンプトセクションの置換 (正規表現)
        $opt = [System.Text.RegularExpressions.RegexOptions]::Singleline
        
        # 見出しも含めて再構成（置換ミスを防ぐ）
        $P1Pattern = "(## 1ページ目プロンプト\s*\n\s*```text\s*\n).*?(\n```)"
        $P2Pattern = "(## 2ページ目プロンプト\s*\n\s*```text\s*\n).*?(\n```)"
        
        # $ を $$ にエスケープ（Replaceメソッド用）
        $SafeP1 = $NewP1.Replace('$', '$$')
        $SafeP2 = $NewP2.Replace('$', '$$')
        
        $CurrentContent = [regex]::Replace($CurrentContent, $P1Pattern, ('$1' + $SafeP1 + '$2'), $opt)
        $CurrentContent = [regex]::Replace($CurrentContent, $P2Pattern, ('$1' + $SafeP2 + '$2'), $opt)

        # 7. 変更の保存
        if ($CurrentContent -ne $RawContent) {
            if (-not $DryRun) {
                [System.IO.File]::WriteAllText($File.FullName, $CurrentContent, [System.Text.Encoding]::UTF8)
            }
            Write-Host "DONE" -ForegroundColor Green
            $count++
        }
        else {
            Write-Host "SKIP" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
    }
}

$Msg = if ($DryRun) { "確認完了" } else { "更新完了" }
Write-Host "`n✅ $Msg : $count 個のファイルを修正(予定)しました。" -ForegroundColor Cyan
