# Update-AllPrompts.ps1 - プロンプト一括更新スクリプト
# このファイルは UTF-8 (with BOM) で保存してください。
$ErrorActionPreference = "Stop"

# 共通設定を読み込む
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $ScriptDir "Settings.ps1")

$TargetDir = $Config.Paths.BaseDir
Write-Host "Searching in: $TargetDir" -ForegroundColor Cyan

# 対象ファイルの取得 (再帰的)
$Files = Get-ChildItem -Path $TargetDir -Recurse -Filter "No*_プロンプト.md"
Write-Host "Found $($Files.Count) files." -ForegroundColor Cyan

foreach ($File in $Files) {
    Write-Host "Processing $($File.Name)..." -NoNewline
    
    try {
        $Content = Get-Content $File.FullName -Raw -Encoding UTF8
        $OriginalContent = $Content
        
        # 1. 解剖学的要件 (Anatomy Block) の追加
        if ($Content -notmatch "CRITICAL ANATOMICAL REQUIREMENTS") {
            $Content = $Content.Replace("Resolution: High quality manga illustration", "Resolution: High quality manga illustration`n`n$($Config.Prompts.AnatomyBlock)")
        }
        
        # 2. キャラクター定義の更新 (Remi, Yuto)
        $Content = $Content.Replace($Config.Characters.Remi.Old, $Config.Characters.Remi.New)
        $Content = $Content.Replace($Config.Characters.Yuto.Old, $Config.Characters.Yuto.New)

        # 3. 複利タイトルの調整
        $Content = $Content.Replace($Config.Prompts.TitleOld, $Config.Prompts.TitleNew)
        
        # 4. 命令文 (Prefix) の追加
        # 先頭の ```text にマッチさせて、直後に Prefix を挿入する
        if ($Content -notmatch [regex]::Escape($Config.Prompts.Prefix)) {
            $PrefixLine = "```text`n$($Config.Prompts.Prefix)`n"
            $Content = $Content -replace "(?m)^```text\s*$", $PrefixLine
        }

        # 変更があれば保存
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

Write-Host "`n一括更新が完了しました。" -ForegroundColor Cyan
