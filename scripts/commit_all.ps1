param(
    [string]$Message = "",
    [string]$Mode = "Auto",
    [bool]$Push = $true
)

# デフォルトメッセージ（引数が空の場合）
if (-not $Message -or $Message -eq "") {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $Message = "Antigravity finished [$Mode] - $timestamp"
}

# すべてステージ
git add -A

function Send-Notification {
    param(
        [string]$Title,
        [string]$Body
    )

    try {
        # BurntToast が無ければローカルユーザーにインストールを試みる
        if (-not (Get-Module -ListAvailable -Name BurntToast)) {
            Install-Module -Name BurntToast -Scope CurrentUser -Force -AllowClobber -ErrorAction Stop
        }
        Import-Module BurntToast -ErrorAction Stop
        New-BurntToastNotification -Text $Title, $Body
    } catch {
        # フォールバック：コンソール出力とログ
        Write-Host "$Title - $Body"
        "$([datetime]::Now) - $Title - $Body" | Out-File -FilePath "$PSScriptRoot\notify_fallback.log" -Append -Encoding utf8
    }
}

# 変更があるか確認
$porcelain = git status --porcelain
$changeCount = ($porcelain | Where-Object { $_ -ne '' } | Measure-Object).Count
if ($changeCount -eq 0) {
    Write-Host "No changes to commit."
    Send-Notification -Title "Git: No changes" -Body "Nothing to commit."
    exit 0
}

# コミット実行
git commit -m $Message
if ($LASTEXITCODE -ne 0) {
    Write-Host "Commit failed."
    Send-Notification -Title "Git: Commit failed" -Body "Check the terminal for details."
    exit $LASTEXITCODE
}
Write-Host "Committed with message: $Message ($changeCount files changed)"

if ($Push) {
    Write-Host "Pushing to remote..."
    try {
        $pushOutput = git push 2>&1
        $pushExit = $LASTEXITCODE
        if ($pushExit -ne 0) {
            Write-Host "Push failed: $pushOutput"
            Send-Notification -Title "Git: Push failed" -Body "Push failed. Check terminal for details."
            "$([datetime]::Now) - Push failed - $pushOutput" | Out-File -FilePath "$PSScriptRoot\notify_fallback.log" -Append -Encoding utf8
            exit $pushExit
        } else {
            Write-Host "Push succeeded."
            Send-Notification -Title "Git: Committed & Pushed" -Body "$Message - $changeCount files changed"
            exit 0
        }
    } catch {
        Write-Host "Push exception: $_"
        Send-Notification -Title "Git: Push failed" -Body "Exception during push. Check logs."
        "$([datetime]::Now) - Push exception - $_" | Out-File -FilePath "$PSScriptRoot\notify_fallback.log" -Append -Encoding utf8
        exit 1
    }
} else {
    Send-Notification -Title "Git: Committed" -Body "$Message - $changeCount files changed"
    exit 0
}
