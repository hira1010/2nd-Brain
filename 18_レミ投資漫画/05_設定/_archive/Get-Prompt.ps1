# Prompt Extractor
# Usage: .\Get-Prompt.ps1 4

param([int]$Number)

$baseDir = 'c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画\01_投資の基礎知識'
$files = Get-ChildItem -Path $baseDir | Where-Object { $_.Name -like "No*$Number*_プロンプト.md" }

if ($files.Count -eq 0) { Write-Host "Not found"; exit 1 }

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

if ($p1) { Write-Host '=== PAGE 1 ===' -ForegroundColor Green; $p1 -join "`n" }
if ($p2) { Write-Host '=== PAGE 2 ===' -ForegroundColor Cyan; $p2 -join "`n" }
