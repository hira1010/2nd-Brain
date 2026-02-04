# MangaTool.ps1 - レミ投資漫画 制作支援統合ツール
[CmdletBinding()]
param(
    [Parameter()]
    [ValidateSet("Prompt", "Resize", "Preview", "Update")]
    [string]$Mode,

    [Parameter()]
    [string]$Path,

    [Parameter()]
    [int]$Number
)

# 1. 共通設定の読み込み
. (Join-Path $PSScriptRoot "Settings.ps1")

# --- 内部関数 ---

function Show-MangaHeader {
    [CmdletBinding()]
    param()
    Clear-Host
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "   🎨 レミ投資漫画 制作アシスタント v2" -ForegroundColor White
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
}

function Get-MangaPrompt {
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][int]$Num)
    
    $numStr = $Num.ToString("00")
    $files = Get-ChildItem -Path $Config.Paths.BaseDir -Recurse -Filter "No${numStr}_*_プロンプト.md"
    
    if (-not $files) {
        Write-Host "❌ No.$Num のファイルが見つかりません。" -ForegroundColor Red
        return
    }

    $content = [System.IO.File]::ReadAllText($files[0].FullName)
    Write-Host "📜 プロンプトを抽出しました: $($files[0].Name)" -ForegroundColor Green
    
    $opt = [System.Text.RegularExpressions.RegexOptions]::Singleline
    $p1 = ""; $match1 = [regex]::Match($content, "## 1ページ目プロンプト\s*\n\s*```text\s*\n(.*?)\n```", $opt)
    if ($match1.Success) {
        $p1 = $match1.Groups[1].Value
        Write-Host ""
        Write-Host "= == 1ページ目 (AIスタジオ用) ===" -ForegroundColor Yellow
        Write-Host $p1
    }

    $p2 = ""; $match2 = [regex]::Match($content, "## 2ページ目プロンプト\s*\n\s*```text\s*\n(.*?)\n```", $opt)
    if ($match2.Success) {
        $p2 = $match2.Groups[1].Value
        Write-Host ""
        Write-Host "=== 2ページ目 (AIスタジオ用) ===" -ForegroundColor Yellow
        Write-Host $p2
    }

    if ($p1 -or $p2) {
        Write-Host ""
        $c = Read-Host "📋 コピーしますか？ (1:1P目 / 2:2P目 / n:しない)"
        if ($c -eq '1') { Set-Clipboard -Value $p1; Write-Host "✅ 1P目コピー完了" -ForegroundColor Green }
        elseif ($c -eq '2') { Set-Clipboard -Value $p2; Write-Host "✅ 2P目コピー完了" -ForegroundColor Green }
    }
}

function Set-MangaImageSize {
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][string]$FilePath)
    Add-Type -AssemblyName System.Drawing
    $f = $FilePath.Trim('"').Trim("'")
    if (-not (Test-Path $f)) { Write-Error "File not found: $f"; return }
    try {
        $img = [System.Drawing.Image]::FromFile($f)
        $tw, $th = $Config.Image.Width, $Config.Image.Height
        if ($img.Width -eq $tw -and $img.Height -eq $th) {
            Write-Host "✅ サイズ修正済み" -ForegroundColor Green
        }
        else {
            Write-Host "Resizing..." -ForegroundColor Cyan
            $bmp = New-Object System.Drawing.Bitmap($tw, $th)
            $g = [System.Drawing.Graphics]::FromImage($bmp)
            $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
            $g.DrawImage($img, 0, 0, $tw, $th)
            $out = $f -replace '\.png$', '_fixed.png'
            $bmp.Save($out, [System.Drawing.Imaging.ImageFormat]::Png)
            $g.Dispose(); $bmp.Dispose()
            Write-Host "✅ 保存完了: $out" -ForegroundColor Green
        }
        $img.Dispose()
    }
    catch { Write-Error "Error: $_" }
}

function New-MangaPreview {
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][int]$Num)
    Add-Type -AssemblyName System.Drawing
    $files = Get-ChildItem -Path (Get-Location) -Filter "*.png" | Where-Object { $_.Name -match "No0?$Num" }
    $p1 = $files | Where-Object { $_.Name -match "p1" -and $_.Name -notmatch "preview" } | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    $p2 = $files | Where-Object { $_.Name -match "p2" -and $_.Name -notmatch "preview" } | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if (-not $p1 -or -not $p2) { Write-Error "Pair not found."; return }
    try {
        $i1 = [System.Drawing.Image]::FromFile($p1.FullName)
        $i2 = [System.Drawing.Image]::FromFile($p2.FullName)
        $bmp = New-Object System.Drawing.Bitmap(($i1.Width + $i2.Width), [Math]::Max($i1.Height, $i2.Height))
        $g = [System.Drawing.Graphics]::FromImage($bmp)
        $g.Clear([System.Drawing.Color]::White)
        $g.DrawImage($i1, 0, 0)
        $g.DrawImage($i2, $i1.Width, 0)
        $out = Join-Path (Get-Location) "No${Num}_見開きプレビュー.png"
        $bmp.Save($out, [System.Drawing.Imaging.ImageFormat]::Png)
        $i1.Dispose(); $i2.Dispose(); $bmp.Dispose(); $g.Dispose()
        Write-Host "✅ 作成完了: $out" -ForegroundColor Green
        Start-Process $out
    }
    catch { Write-Error "Error: $_" }
}

# --- メイン処理 ---
if ($Mode) {
    switch ($Mode) {
        "Prompt" { Get-MangaPrompt $Number }
        "Resize" { Set-MangaImageSize $Path }
        "Preview" { New-MangaPreview $Number }
        "Update" { & (Join-Path $PSScriptRoot "Update-MangaPrompts.ps1") }
    }
    return
}

while ($true) {
    Show-MangaHeader
    Write-Host "1. 📜 プロンプト抽出・コピー" -ForegroundColor Yellow
    Write-Host "2. 🖼️ 画像リサイズ (1200x1697)" -ForegroundColor Yellow
    Write-Host "3. 📖 見開きプレビュー作成" -ForegroundColor Yellow
    Write-Host "u. 🔄 全プロンプト一括更新" -ForegroundColor Yellow
    Write-Host "q. 終了" -ForegroundColor Gray
    Write-Host ""
    $s = Read-Host "選択"
    switch ($s) {
        "1" { $n = Read-Host "No"; if ($n -as [int]) { Get-MangaPrompt $n }; $null = Read-Host "Enter..." }
        "2" { $p = Read-Host "Path"; Set-MangaImageSize $p; $null = Read-Host "Enter..." }
        "3" { $n = Read-Host "No"; if ($n -as [int]) { New-MangaPreview $n }; $null = Read-Host "Enter..." }
        "u" { & (Join-Path $PSScriptRoot "Update-MangaPrompts.ps1"); $null = Read-Host "Enter..." }
        "q" { exit }
    }
}
