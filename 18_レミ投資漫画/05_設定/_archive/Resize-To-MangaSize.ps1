# 画像を1200x1700にリサイズするスクリプト
param(
    [string]$InputImage
)

Add-Type -AssemblyName System.Drawing

$img = [System.Drawing.Image]::FromFile($InputImage)
$resized = New-Object System.Drawing.Bitmap(1200, 1700)
$graphics = [System.Drawing.Graphics]::FromImage($resized)
$graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$graphics.DrawImage($img, 0, 0, 1200, 1700)

$outputPath = $InputImage -replace '\.png$', '_1200x1700.png'
$resized.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)

$img.Dispose()
$resized.Dispose()
$graphics.Dispose()

Write-Host "✅ リサイズ完了: $outputPath" -ForegroundColor Green
