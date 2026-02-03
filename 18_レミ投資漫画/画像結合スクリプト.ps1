# レミ投資漫画 2ページ結合スクリプト
# 使い方: .\画像結合スクリプト.ps1 -Page1 "No35_株の始まり_p1.png" -Page2 "No35_株の始まり_p2.png" -Output "No35_株の始まり_見開き.png"

param(
    [Parameter(Mandatory = $true)]
    [string]$Page1,  # 1ページ目のファイル名
    
    [Parameter(Mandatory = $true)]
    [string]$Page2,  # 2ページ目のファイル名
    
    [Parameter(Mandatory = $true)]
    [string]$Output  # 出力ファイル名
)

# スクリプトのディレクトリを取得
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# フルパスを構築
$Page1Path = Join-Path $ScriptDir $Page1
$Page2Path = Join-Path $ScriptDir $Page2
$OutputPath = Join-Path $ScriptDir $Output

Write-Host "=== レミ投資漫画 2ページ結合スクリプト ===" -ForegroundColor Cyan
Write-Host ""

# ファイルの存在確認
if (-not (Test-Path $Page1Path)) {
    Write-Host "エラー: 1ページ目が見つかりません: $Page1Path" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $Page2Path)) {
    Write-Host "エラー: 2ページ目が見つかりません: $Page2Path" -ForegroundColor Red
    exit 1
}

Write-Host "✓ 1ページ目: $Page1" -ForegroundColor Green
Write-Host "✓ 2ページ目: $Page2" -ForegroundColor Green
Write-Host ""

# .NET の System.Drawing を使用して画像を結合
Add-Type -AssemblyName System.Drawing

try {
    # 画像を読み込み
    $img1 = [System.Drawing.Image]::FromFile($Page1Path)
    $img2 = [System.Drawing.Image]::FromFile($Page2Path)
    
    # 新しい画像のサイズを計算（横並び）
    $totalWidth = $img1.Width + $img2.Width
    $maxHeight = [Math]::Max($img1.Height, $img2.Height)
    
    Write-Host "見開き画像サイズ: ${totalWidth}px × ${maxHeight}px" -ForegroundColor Yellow
    
    # 新しいビットマップを作成
    $combined = New-Object System.Drawing.Bitmap($totalWidth, $maxHeight)
    $graphics = [System.Drawing.Graphics]::FromImage($combined)
    
    # 背景を白で塗りつぶし
    $graphics.Clear([System.Drawing.Color]::White)
    
    # 1ページ目を左側に描画
    $graphics.DrawImage($img1, 0, 0, $img1.Width, $img1.Height)
    
    # 2ページ目を右側に描画
    $graphics.DrawImage($img2, $img1.Width, 0, $img2.Width, $img2.Height)
    
    # 保存
    $combined.Save($OutputPath, [System.Drawing.Imaging.ImageFormat]::Png)
    Write-Host "✓ 見開き画像を保存しました: $Output" -ForegroundColor Green
    
    # クリーンアップ
    $graphics.Dispose()
    $img1.Dispose()
    $img2.Dispose()
    $combined.Dispose()
    
    Write-Host ""
    Write-Host "=== 完了！ ===" -ForegroundColor Cyan
    Write-Host "見開き版: $Output (${totalWidth}×${maxHeight}px)" -ForegroundColor White
    
}
catch {
    Write-Host "エラー: 画像の結合に失敗しました" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
