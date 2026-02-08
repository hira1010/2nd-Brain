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
# 繝・ヵ繧ｩ繝ｫ繝医Γ繝・そ繝ｼ繧ｸ・亥ｼ墓焚縺檎ｩｺ縺ｮ蝣ｴ蜷茨ｼ・
if (-not $Message -or $Message -eq "") {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $Message = "Antigravity finished [$Mode] - $timestamp"
}

# 繝ｪ繝昴ず繝医Μ繝ｫ繝ｼ繝医ｒ豎ｺ螳壹＠縺ｦ遘ｻ蜍包ｼ医ち繧ｹ繧ｯ迺ｰ蠅・〒繧ら｢ｺ螳溘↓蜍輔￥繧医≧縺ｫ・・
try {
    $repoRoot = git rev-parse --show-toplevel 2>&1
    if ($LASTEXITCODE -ne 0 -or -not $repoRoot) { throw "git rev-parse failed" }
    $repoRoot = $repoRoot.Trim()
} catch {
    # 繝輔か繝ｼ繝ｫ繝舌ャ繧ｯ縺ｯ繧ｹ繧ｯ繝ｪ繝励ヨ縺ｮ隕ｪ繝・ぅ繝ｬ繧ｯ繝医Μ
    $repoRoot = Split-Path -Path $PSScriptRoot -Parent
}
Set-Location -Path $repoRoot

# 縺吶∋縺ｦ繧ｹ繝・・繧ｸ・・it -C 繧剃ｽｿ縺｣縺ｦ遒ｺ螳溘↓蟇ｾ雎｡繝ｪ繝昴ず繝医Μ繧呈欠螳夲ｼ・
git -C "$repoRoot" add -A

function Send-Notification {
    param(
        [string]$Title,
        [string]$Body
    )
    try {
        # BurntToast 縺檎┌縺代ｌ縺ｰ繝ｭ繝ｼ繧ｫ繝ｫ繝ｦ繝ｼ繧ｶ繝ｼ縺ｫ繧､繝ｳ繧ｹ繝医・繝ｫ繧定ｩｦ縺ｿ繧・
        if (-not (Get-Module -ListAvailable -Name BurntToast)) {
            Install-Module -Name BurntToast -Scope CurrentUser -Force -AllowClobber -ErrorAction Stop
        }
        Import-Module BurntToast -ErrorAction Stop
        New-BurntToastNotification -Text $Title, $Body
    } catch {
        # 繝輔か繝ｼ繝ｫ繝舌ャ繧ｯ・壹さ繝ｳ繧ｽ繝ｼ繝ｫ蜃ｺ蜉帙→繝ｭ繧ｰ
        Write-Host "$Title - $Body"
        "$([datetime]::Now) - $Title - $Body" | Out-File -FilePath "$PSScriptRoot\notify_fallback.log" -Append -Encoding utf8
    }
}

# 螟画峩縺後≠繧九°遒ｺ隱・
$porcelain = git -C "$repoRoot" status --porcelain
$changeCount = ($porcelain | Where-Object { $_ -ne '' } | Measure-Object).Count
if ($changeCount -eq 0) {
    Write-Host "No changes to commit."
    Send-Notification -Title "Git: No changes" -Body "Nothing to commit."
    exit 0
}

# 繧ｳ繝溘ャ繝亥ｮ溯｡・
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

