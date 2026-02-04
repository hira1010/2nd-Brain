# Update-MangaPrompts.ps1 - 全プロンプトの一括更新（統合版）
[CmdletBinding()]
param(
    [Parameter()]
    [switch]$Force
)

# 1. 環境準備
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $ScriptDir "Settings.ps1")

Write-Host "🚀 統合更新開始..." -ForegroundColor Cyan

$Files = Get-ChildItem -Path $Config.Paths.BaseDir -Recurse -Filter "No*_プロンプト.md"
if ($null -eq $Files -or $Files.Count -eq 0) {
    Write-Warning "No files found."
    return
}

$count = 0
foreach ($File in $Files) {
    Write-Host "Processing: $($File.Name)... " -NoNewline
    try {
        $RawContent = [System.IO.File]::ReadAllText($File.FullName)
        
        $No = 1
        if ($RawContent -match '\| No \| (\d+) \|') { $No = [int]$Matches[1] }
        $Title = "投資"; if ($RawContent -match '\| タイトル \| (.*?) \|') { $Title = $Matches[1].Trim() }
        $IntroDialog = "教えてください！"; if ($RawContent -match '\| DIALOGUE_INTRO \| (.*?) \|') { $IntroDialog = $Matches[1].Trim() }
        $TeachDialog = "いいわよ。"; if ($RawContent -match '\| DIALOGUE_TEACH \| (.*?) \|') { $TeachDialog = $Matches[1].Trim() }
        $DescDialog = "これが本質よ。"; if ($RawContent -match '\| DIALOGUE_DESC \| (.*?) \|') { $DescDialog = $Matches[1].Trim() }
        $ActionDialog = "やってみます！"; if ($RawContent -match '\| DIALOGUE_ACTION \| (.*?) \|') { $ActionDialog = $Matches[1].Trim() }

        $TemplateP1 = $Config.Prompts.TemplateP1_Yuto
        if ($No % 2 -eq 0) { $TemplateP1 = $Config.Prompts.TemplateP1_Remi }
        
        $NL = [Environment]::NewLine
        $NewP1 = $Config.Prompts.Prefix + $NL + $NL + $TemplateP1.Replace("{Title}", $Title).Replace("{IntroDialog}", $IntroDialog).Replace("{TeachDialog}", $TeachDialog)
        $NewP2 = $Config.Prompts.Prefix + $NL + $NL + $Config.Prompts.TemplateP2.Replace("{Title}", $Title).Replace("{DescDialog}", $DescDialog).Replace("{ActionDialog}", $ActionDialog)

        $opt = [System.Text.RegularExpressions.RegexOptions]::Singleline
        $P1Pattern = "## 1ページ目プロンプト\s*\n\s*```text\s*\n.*?\n```"
        $P2Pattern = "## 2ページ目プロンプト\s*\n\s*```text\s*\n.*?\n```"
        $Rep1 = "## 1ページ目プロンプト" + $NL + $NL + "```text" + $NL + $NewP1 + $NL + "```"
        $Rep2 = "## 2ページ目プロンプト" + $NL + $NL + "```text" + $NL + $NewP2 + $NL + "```"

        $NewContent = [regex]::Replace($RawContent, $P1Pattern, $Rep1.Replace('$', '$$'), $opt)
        $NewContent = [regex]::Replace($NewContent, $P2Pattern, $Rep2.Replace('$', '$$'), $opt)

        $tw = $Config.Image.Width
        $th = $Config.Image.Height
        $tr = $Config.Image.AspectRatio
        $NewContent = $NewContent.Replace("1200x1700", "$tw`x$th").Replace("aspect ratio 12:17", "aspect ratio $tr")

        if ($NewContent -ne $RawContent) {
            [System.IO.File]::WriteAllText($File.FullName, $NewContent, [System.Text.Encoding]::UTF8)
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
Write-Host "`n✅ 更新完了: $count 個のファイルを修正しました。" -ForegroundColor Cyan
