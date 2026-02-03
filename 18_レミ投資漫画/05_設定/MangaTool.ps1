# MangaTool.ps1 - レミ投資漫画 統合ツール
# 使い方:
#   .\MangaTool.ps1                (メニュー表示)
#   .\MangaTool.ps1 -Mode Prompt -Number 15
#   .\MangaTool.ps1 -Mode Resize -Path "image.png"
#   .\MangaTool.ps1 -Mode Preview -Number 15

param(
    [string]$Mode,
    [string]$Path,
    [int]$Number
)

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
    $baseDir = "c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画\01_投資の基礎知識"
    $files = Get-ChildItem -Path $baseDir | Where-Object { $_.Name -like "No*${Num}*_プロンプト.md" }

    if ($files.Count -eq 0) { Write-Host "❌ No.$Num のファイルが見つかりません" -ForegroundColor Red; return }

    $lines = Get-Content $files[0].FullName -Encoding UTF8
    $inCode = $false; $section = ''; $p1 = @(); $p2 = @()

    foreach ($line in $lines) {
        if ($line -match '^## 1ページ') { $section = '1'; continue }
        if ($line -match '^## 2ページ') { $section = '2'; continue }
        if ($line -match '^## ') { $section = ''; $inCode = $false; continue }
        if ($line -match '^``````text') { $inCode = $true; continue }
        if ($line -match '^``````$') { $inCode = $false; continue }
        if ($inCode -and $section -eq '1') { $p1 += $line }
        if ($inCode -and $section -eq '2') { $p2 += $line }
    }

    Write-Host "📜 No.$Num のプロンプトを抽出しました" -ForegroundColor Green
    Write-Host ""
    
    $prefix = "画像生成を行ってください。以下のプロンプトに基づいて、縦長のマンガ画像を生成してください。`n`n"

    if ($p1) { 
        Write-Host '=== 1ページ目 (AIスタジオにコピペ) ===' -ForegroundColor Yellow
        $text1 = $prefix + ($p1 -join "`n")
        Write-Host $text1
        Write-Host "" 
    }
    if ($p2) { 
        Write-Host '=== 2ページ目 (AIスタジオにコピペ) ===' -ForegroundColor Yellow
        $text2 = $prefix + ($p2 -join "`n")
        Write-Host $text2
        Write-Host "" 
    }
    
    # クリップボードにコピー
    $choice = Read-Host "📋 1ページ目をクリップボードにコピーしますか？ (y/n)"
    if ($choice -eq 'y') { Set-Clipboard -Value $text1; Write-Host "✅ コピーしました！（命令文付き）" -ForegroundColor Green }
}

function Resize-Image {
    param([string]$FilePath)
    Add-Type -AssemblyName System.Drawing
    
    if (-not (Test-Path $FilePath)) { Write-Host "❌ ファイルが見つかりません: $FilePath" -ForegroundColor Red; return }
    
    try {
        $img = [System.Drawing.Image]::FromFile($FilePath)
        if ($img.Width -eq 1200 -and $img.Height -eq 1700) {
            Write-Host "✅ サイズは既に 1200x1700 です。リサイズ不要。" -ForegroundColor Green
            $img.Dispose()
            return
        }

        $resized = New-Object System.Drawing.Bitmap(1200, 1700)
        $graphics = [System.Drawing.Graphics]::FromImage($resized)
        $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $graphics.DrawImage($img, 0, 0, 1200, 1700)
        
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
    
    # 画像を探す
    $files = Get-ChildItem -Path . -Filter "*.png" | Where-Object { $_.Name -match "No0?$Num" }
    $p1 = $files | Where-Object { $_.Name -match "p1" -and $_.Name -notmatch "preview" } | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    $p2 = $files | Where-Object { $_.Name -match "p2" -and $_.Name -notmatch "preview" } | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    
    if (-not $p1 -or -not $p2) { 
        Write-Host "❌ No.$Num の画像ペアが見つかりません (p1, p2)" -ForegroundColor Red
        return 
    }

    Write-Host "画像結合中..."
    Write-Host "  Left: $($p1.Name)"
    Write-Host "  Right: $($p2.Name)"

    $img1 = [System.Drawing.Image]::FromFile($p1.FullName)
    $img2 = [System.Drawing.Image]::FromFile($p2.FullName)
    
    $width = $img1.Width + $img2.Width
    $height = [Math]::Max($img1.Height, $img2.Height)
    
    $combined = New-Object System.Drawing.Bitmap($width, $height)
    $graphics = [System.Drawing.Graphics]::FromImage($combined)
    $graphics.FillRectangle([System.Drawing.Brushes]::White, 0, 0, $width, $height)
    
    # 漫画は右から左なので、p1を右、p2を左にするか？
    # 通常のプレビューなら p1(左) p2(右) で良いが、漫画の見開き（右綴じ）なら p2(左) p1(右)
    # ここでは単純に p1(左) p2(右) とする（ウェブ表示順）
    $graphics.DrawImage($img1, 0, 0)
    $graphics.DrawImage($img2, $img1.Width, 0)
    
    $outputPath = "No${Num}_見開きプレビュー.png"
    $combined.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)
    
    $img1.Dispose(); $img2.Dispose(); $combined.Dispose(); $graphics.Dispose()
    Write-Host "✅ 見開きプレビュー作成完了: $outputPath" -ForegroundColor Green
    
    # HTMLで表示
    Start-Process $outputPath
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
    Write-Host "1. 📜 プロンプトを表示 (Get-Prompt)"
    Write-Host "2. 🖼️ 画像をリサイズ (Resize 1200x1700)"
    Write-Host "3. 📖 見開きプレビュー作成 (Create-Preview)"
    Write-Host "q. 終了"
    Write-Host ""
    
    $selection = Read-Host "選択してください"
    
    switch ($selection) {
        "1" {
            $n = Read-Host "Noを入力 (例: 15)"
            Get-Prompt ([int]$n)
            Pause
        }
        "2" {
            $p = Read-Host "画像パスを入力 (ドラッグ&ドロップ)"
            Resize-Image $p.Trim('"')
            Pause
        }
        "3" {
            $n = Read-Host "Noを入力 (例: 15)"
            Create-Preview ([int]$n)
            Pause
        }
        "q" { exit }
    }
}
