param(
    [string]$Message = "",
    [string]$Mode = "Auto",
    [bool]$Push = $true
)
$EnableFlag = Join-Path $PSScriptRoot '.autocommit-enabled'
if (-not (Test-Path -Path $EnableFlag)) {
    Write-Host "Autocommit is disabled (missing flag file): $EnableFlag"
    exit 0
}
# デフォルトメッセージ（引数が空の場合）
if (-not $Message -or $Message -eq "") {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $Message = "Antigravity finished [$Mode] - $timestamp"
}

# リポジトリルートを決定して移動
try {
    $repoRoot = git rev-parse --show-toplevel 2>&1
    if ($LASTEXITCODE -ne 0 -or -not $repoRoot) { throw "git rev-parse failed" }
    $repoRoot = $repoRoot.Trim()
}
catch {
    $repoRoot = Split-Path -Path $PSScriptRoot -Parent
}
Set-Location -Path $repoRoot

function Send-Notification {
    param(
        [string]$Title,
        [string]$Body
    )
    try {
        if (-not (Get-Module -ListAvailable -Name BurntToast)) {
            Install-Module -Name BurntToast -Scope CurrentUser -Force -AllowClobber -ErrorAction Stop
        }
        Import-Module BurntToast -ErrorAction Stop
        New-BurntToastNotification -Text $Title, $Body
    }
    catch {
        Write-Host "$Title - $Body"
        "$([datetime]::Now) - $Title - $Body" | Out-File -FilePath "$PSScriptRoot\notify_fallback.log" -Append -Encoding utf8
    }
}

# ---------------------------------------------------------
# Google Drive (Sheets) からのデータ同期
# ---------------------------------------------------------
Write-Host "Syncing data from Google Drive..." -ForegroundColor Cyan
$env:PYTHONUTF8 = "1"

# 1. 資産同期 (配当・資産推移)
$syncAssetsPath = Join-Path $repoRoot "18_システム\sync_assets.py"
Write-Host "Running Asset Sync..." -ForegroundColor Yellow
python -X utf8 "$syncAssetsPath"
$assetExit = $LASTEXITCODE

# 2. 体重同期
$syncWeightPath = Join-Path $repoRoot "18_システム\sync_weight.py"
Write-Host "Running Weight Sync..." -ForegroundColor Yellow
python -X utf8 "$syncWeightPath"
$weightExit = $LASTEXITCODE

if ($assetExit -ne 0 -or $weightExit -ne 0) {
    Write-Host "Warning: Some sync processes failed (Assets: $assetExit, Weight: $weightExit)" -ForegroundColor Yellow
}

# 同期による変更を再度ステージング
git -C "$repoRoot" add -A

# 変更があるか確認
$porcelain = git -C "$repoRoot" status --porcelain
$changeCount = ($porcelain | Where-Object { $_ -ne '' } | Measure-Object).Count
if ($changeCount -eq 0) {
    Write-Host "No changes to commit (Everything is up-to-date)."
    Send-Notification -Title "Git: No changes" -Body "Everything is up-to-date."
    exit 0
}

# コミット実行
$commitResult = git -C "$repoRoot" commit -m $Message 2>&1
$commitExit = $LASTEXITCODE
if ($commitExit -ne 0) {
    Write-Host "Commit failed: $commitResult"
    Send-Notification -Title "Git: Commit failed" -Body "Check the terminal for details."
    "$([datetime]::Now) - Commit failed - $commitResult" | Out-File -FilePath "$PSScriptRoot\notify_fallback.log" -Append -Encoding utf8
    exit $commitExit
}
Write-Host "Committed with message: $Message ($changeCount files changed)"

if ($Push) {
    Write-Host "Pushing to remote..."
    try {
        $pushOutput = git -C "$repoRoot" push 2>&1
        $pushExit = $LASTEXITCODE
        if ($pushExit -ne 0) {
            Write-Host "Push failed: $pushOutput"
            Send-Notification -Title "Git: Push failed" -Body "Push failed. Check terminal for details."
            "$([datetime]::Now) - Push failed - $pushOutput" | Out-File -FilePath "$PSScriptRoot\notify_fallback.log" -Append -Encoding utf8
            exit $pushExit
        }
        else {
            Write-Host "Push succeeded."
            Send-Notification -Title "Git: Committed & Pushed" -Body "$Message - $changeCount files changed"
            exit 0
        }
    }
    catch {
        Write-Host "Push exception: $_"
        Send-Notification -Title "Git: Push failed" -Body "Exception during push. Check logs."
        "$([datetime]::Now) - Push exception - $_" | Out-File -FilePath "$PSScriptRoot\notify_fallback.log" -Append -Encoding utf8
        exit 1
    }
}
else {
    Send-Notification -Title "Git: Committed" -Body "$Message - $changeCount files changed"
    exit 0
}
