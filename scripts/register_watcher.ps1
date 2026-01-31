param(
    [string]$TaskName = "AntigravityWatcher",
    [string]$ProcessName = "Antigravity"
)

$watcherPath = (Resolve-Path "$PSScriptRoot\watch_antigravity.ps1").Path
$action = "powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$watcherPath`" -ProcessName `"$ProcessName`""

# ユーザーログオン時に実行されるタスクを作成
schtasks /Create /SC ONLOGON /TN $TaskName /TR "$action" /F | Out-Null
Write-Host "Scheduled task created: $TaskName (will run at user logon)."
Write-Host "Task action: $action"
