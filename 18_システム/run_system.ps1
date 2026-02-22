# Antigravity System Launcher
# このスクリプトは、Windows環境での Python エンコーディング問題を回避して
# システムスクリプトを安全に実行するためのランチャーです。

param(
    [string]$Script = "smart_refactor.py",
    [string]$Args = "--dry-run"
)

Write-Host "=== Antigravity System Launcher ===" -ForegroundColor Cyan

# UTF-8 モードの強制
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

# スクリプトのフルパスを取得
$ScriptPath = Join-Path $PSScriptRoot $Script

if (-not (Test-Path $ScriptPath)) {
    Write-Host "Error: Script not found at $ScriptPath" -ForegroundColor Red
    exit 1
}

Write-Host "Running: $Script $Args" -ForegroundColor Yellow

# Python の実行
# -X utf8: UTF-8 モードを有効化
# -S: site-packages を原因とする Fatal Error 回避が必要な場合に備え、
#     問題が深刻な場合は追加を検討（現在は環境変数での解決を優先）
& python -X utf8 $ScriptPath $Args.Split(" ")

if ($LASTEXITCODE -ne 0) {
    Write-Host "`nWarning: Script exited with code $LASTEXITCODE" -ForegroundColor Yellow
}
else {
    Write-Host "`nSuccess: Script completed." -ForegroundColor Green
}
