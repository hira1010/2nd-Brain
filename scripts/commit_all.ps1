param(
    [string]$Message = ""
)

# デフォルトメッセージ（引数が空の場合）
if (-not $Message -or $Message -eq "") {
    $date = Get-Date -Format "yyyy-MM-dd"
    $Message = "Finish Antigravity - $date"
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
if (-not $porcelain) {
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
Write-Host "Committed with message: $Message"
Send-Notification -Title "Git: Committed" -Body "$Message"
exit 0
