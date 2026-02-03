# MangaTool.ps1 - レミ投資漫画 統合ツール
# 使い方:
#   .\MangaTool.ps1                (メニュー表示)
#   .\MangaTool.ps1 -Mode Prompt -Number 15
#   .\MangaTool.ps1 -Mode Resize -Path "image.png"
#   .\MangaTool.ps1 -Mode Preview -Number 15
# このファイルは UTF-8 (with BOM) で保存してください。

param(
    [string]$Mode,
    [string]$Path,
    [int]$Number
)

# 共通設定を読み込む
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $ScriptDir "Settings.ps1")

# --- 関数定義 ---

function Show-Header {
    Clear-Host
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "   🎨 レミ投資漫画 制作アシスタント" -ForegroundColor White
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
}

function Get-Prompt {
    param([int]$Num)
    $baseDir = $Config.Paths.BaseDir
    # 数値を2桁のNo00形式に整形
    $numStr = $Num.ToString("00")
    $files = Get-ChildItem -Path $baseDir -Recurse | Where-Object { $_.Name -like "No${numStr}_*_プロンプト.md" }

    if ($files.Count -eq 0) { 
        Write-Host "❌ No.$Num のファイルが見つかりません" -ForegroundColor Red
        return 
    }

    $lines = Get-Content $files[0].FullName -Encoding UTF8
    $inCode = $false; $section = ''; $p1 = @(); $p2 = @()

    foreach ($line in $lines) {
        if ($line -match '^## 1ページ') { $section = '1'; continue }
        if ($line -match '^## 2ページ') { $section = '2'; continue }
        if ($line -match '^## ') { $section = ''; $inCode = $false; continue }
        if ($line -match '^```text') { $inCode = $true; continue }
        if ($line -match '^```$') { $inCode = $false; continue }
        if ($inCode -and $section -eq '1') { $p1 += $line }
        if ($inCode -and $section -eq '2') { $p2 += $line }
    }

    Write-Host "📜 No.$Num のプロンプトを抽出しました: $($files[0].Name)" -ForegroundColor Green
    Write-Host ""
    
    $prefix = $Config.Prompts.Prefix + "`n`n"

    if ($p1) { 
        $text1 = $p1 -join "`n"
        # すでに命令文が含まれているか確認
        if ($text1 -notmatch [regex]::Escape($Config.Prompts.Prefix)) {
            $text1 = $prefix + $text1
        }
        Write-Host '=== 1ページ目 (AIスタジオにコピペ) ===' -ForegroundColor Yellow
        Write-Host $text1
        Write-Host "" 
    }
    if ($p2) { 
        $text2 = $p2 -join "`n"
        if ($text2 -notmatch [regex]::Escape($Config.Prompts.Prefix)) {
            $text2 = $prefix + $text2
        }
        Write-Host '=== 2ページ目 (AIスタジオにコピペ) ===' -ForegroundColor Yellow
        Write-Host $text2
        Write-Host "" 
    }
    
    # クリップボードにコピー
    $choice = Read-Host "📋 1ページ目をクリップボードにコピーしますか？ (y/n)"
    if ($choice -eq 'y') { 
        Set-Clipboard -Value $text1
        Write-Host "✅ 1ページ目をコピーしました！" -ForegroundColor Green 
    }
    
    $choice2 = Read-Host "📋 2ページ目をクリップボードにコピーしますか？ (y/n)"
    if ($choice2 -eq 'y') { 
        Set-Clipboard -Value $text2
        Write-Host "✅ 2ページ目をコピーしました！" -ForegroundColor Green 
    }
}

function Resize-Image {
    param([string]$FilePath)
    Add-Type -AssemblyName System.Drawing
    
    # パスが引用符で囲まれている場合のトリム
    $FilePath = $FilePath.Trim('"').Trim("'")
    if (-not (Test-Path $FilePath)) { Write-Host "❌ ファイルが見つかりません: $FilePath" -ForegroundColor Red; return }
    
    try {
        $img = [System.Drawing.Image]::FromFile($FilePath)
        $targetW = $Config.Image.Width
        $targetH = $Config.Image.Height

        if ($img.Width -eq $targetW -and $img.Height -eq $targetH) {
            Write-Host "✅ サイズは既に ${targetW}x${targetH} です。リサイズ不要。" -ForegroundColor Green
            $img.Dispose()
            return
        }

        Write-Host "リサイズ中: $($img.Width)x$($img.Height) -> ${targetW}x${targetH}..." -ForegroundColor Cyan
        $resized = New-Object System.Drawing.Bitmap($targetW, $targetH)
        $graphics = [System.Drawing.Graphics]::FromImage($resized)
        $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $graphics.DrawImage($img, 0, 0, $targetW, $targetH)
        
        $outputPath = $FilePath -replace '\.png$', '_fixed.png'
        $resized.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)
        
        $img.Dispose(); $resized.Dispose(); $graphics.Dispose()
        Write-Host "✅ リサイズ完了: $outputPath" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ エラー: $_" -ForegroundColor Red
    }
}

function Create-Preview {
    param([int]$Num)
    Add-Type -AssemblyName System.Drawing
    
    # カレントディレクトリまたはBaseDirから画像を探す
    $searchDir = Get-Location
    $files = Get-ChildItem -Path $searchDir -Filter "*.png" | Where-Object { $_.Name -match "No0?$Num" }
    
    $p1 = $files | Where-Object { $_.Name -match "p1" -and $_.Name -notmatch "preview|見開き" } | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    $p2 = $files | Where-Object { $_.Name -match "p2" -and $_.Name -notmatch "preview|見開き" } | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    
    if (-not $p1 -or -not $p2) { 
        Write-Host "❌ No.$Num の画像ペアが見つかりません (p1, p2)" -ForegroundColor Red
        Write-Host "   現在のディレクトリにある PNG ファイルを確認してください。"
        return 
    }

    Write-Host "画像結合中..."
    Write-Host "  Left: $($p1.Name)"
    Write-Host "  Right: $($p2.Name)"

    try {
        $img1 = [System.Drawing.Image]::FromFile($p1.FullName)
        $img2 = [System.Drawing.Image]::FromFile($p2.FullName)
        
        $width = $img1.Width + $img2.Width
        $height = [Math]::Max($img1.Height, $img2.Height)
        
        $combined = New-Object System.Drawing.Bitmap($width, $height)
        $graphics = [System.Drawing.Graphics]::FromImage($combined)
        $graphics.FillRectangle([System.Drawing.Brushes]::White, 0, 0, $width, $height)
        
        # 漫画の並び (通常は p1, p2 の順で左から右に配置)
        $graphics.DrawImage($img1, 0, 0)
        $graphics.DrawImage($img2, $img1.Width, 0)
        
        $outputPath = Join-Path $searchDir "No${Num}_見開きプレビュー.png"
        $combined.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)
        
        $img1.Dispose(); $img2.Dispose(); $combined.Dispose(); $graphics.Dispose()
        Write-Host "✅ 見開きプレビュー作成完了: $outputPath" -ForegroundColor Green
        
        # プレビュー表示
        Start-Process $outputPath
    }
    catch {
        Write-Host "❌ エラー: $_" -ForegroundColor Red
    }
}

# --- メイン処理 ---

if ($Mode) {
    switch ($Mode) {
        "Prompt" { Get-Prompt $Number }
        "Resize" { Resize-Image $Path }
        "Preview" { Create-Preview $Number }
    }
    exit
}

# メニューモード
while ($true) {
    Show-Header
    Write-Host "1. 📜 プロンプトを表示・コピー (Get-Prompt)"
    Write-Host "2. 🖼️ 画像をリサイズ (Resize 1200x1700)"
    Write-Host "3. 📖 見開きプレビュー作成 (Create-Preview)"
    Write-Host "u. 🔄 プロンプトを一括更新 (Update-AllPrompts)"
    Write-Host "q. 終了"
    Write-Host ""
    
    $selection = Read-Host "選択してください"
    
    switch ($selection) {
        "1" {
            $n = Read-Host "Noを入力 (例: 15)"
            if ($n -match '^\d+$') { Get-Prompt ([int]$n) }
            Pause
        }
        "2" {
            $p = Read-Host "画像パスを入力 (ドラッグ&ドロップ可)"
            Resize-Image $p
            Pause
        }
        "3" {
            $n = Read-Host "Noを入力 (例: 15)"
            if ($n -match '^\d+$') { Create-Preview ([int]$n) }
            Pause
        }
        "u" {
            & (Join-Path $ScriptDir "Update-AllPrompts.ps1")
            Pause
        }
        "q" { exit }
    }
}
