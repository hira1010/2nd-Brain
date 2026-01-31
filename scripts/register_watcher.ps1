param(
    [string]$TaskName = "AntigravityWatcher",
    [string]$ProcessName = "Antigravity"
)

$watcherPath = (Resolve-Path "$PSScriptRoot\watch_antigravity.ps1").Path

try {
    # アクションとトリガーを作成（現在のユーザーのログオン時に実行、かつユーザーがログオンしているときのみ実行）
    $action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$watcherPath`" -ProcessName `"$ProcessName`""
    $trigger = New-ScheduledTaskTrigger -AtLogOn
    $settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

    Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -User $env:USERNAME -RunLevel Limited -Force

    # 明示的に "Run only when user is logged on" を保証
    $task = Get-ScheduledTask -TaskName $TaskName
    $task.Settings.RunOnlyIfLoggedOn = $true
    Set-ScheduledTask -InputObject $task

    Write-Host "Scheduled task created: $TaskName (will run at user logon, only when user is logged on)."
    Write-Host "Task action: powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$watcherPath`" -ProcessName `"$ProcessName`""
} catch {
    Write-Host "Register-ScheduledTask failed: $_"
    Write-Host "Falling back to schtasks.exe method."
    $actionString = "powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$watcherPath`" -ProcessName `"$ProcessName`""
    schtasks /Create /SC ONLOGON /TN $TaskName /TR "$actionString" /F | Out-Null
    Write-Host "Scheduled task created (schtasks fallback): $TaskName"
}
