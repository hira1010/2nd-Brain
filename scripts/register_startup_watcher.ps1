param(
    [string]$ProcessName = "Antigravity",
    [string]$WatcherScript = "$PSScriptRoot\watch_antigravity.ps1"
)

$startup = [Environment]::GetFolderPath('Startup')
$lnkPath = Join-Path $startup "AntigravityWatcher.lnk"
$target = "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
$arguments = "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$WatcherScript`" -ProcessName `"$ProcessName`""

try {
    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut($lnkPath)
    $shortcut.TargetPath = $target
    $shortcut.Arguments = $arguments
    $shortcut.WorkingDirectory = Split-Path -Parent $WatcherScript
    $shortcut.WindowStyle = 7
    $shortcut.Save()
    Write-Host "Startup shortcut created: $lnkPath"
} catch {
    Write-Host "Failed to create startup shortcut: $_"
    exit 1
}

# Also write a small marker file so user can see that registration happened
"Registered startup watcher for process '$ProcessName' at $([datetime]::Now)" | Out-File -FilePath "$PSScriptRoot\startup_registration.log" -Append -Encoding utf8
