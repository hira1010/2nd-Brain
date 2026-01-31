$ErrorActionPreference = "Stop"
# Move to repo root
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location (Join-Path $scriptDir "..")

$pw = "$env:windir\System32\WindowsPowerShell\v1.0\powershell.exe"
$dest = Join-Path $PWD "scripts\Antigravity.exe"
Copy-Item -Path $pw -Destination $dest -Force

$watch = Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PWD\scripts\watch_antigravity.ps1`" -ProcessName Antigravity -PollSeconds 1" -WindowStyle Hidden -PassThru
Write-Host "Watcher PID: $($watch.Id)"
Start-Sleep -Seconds 1

$proc = Start-Process -FilePath $dest -ArgumentList "-NoProfile -WindowStyle Hidden -Command `"Start-Sleep -Seconds 5`"" -PassThru
Write-Host "Started Antigravity: $($proc.Id)"
Start-Sleep -Seconds 7

if (Test-Path scripts\watcher.log) {
    Write-Host '--- watcher.log (tail) ---'
    Get-Content scripts\watcher.log -Tail 40
} else {
    Write-Host 'no watcher.log'
}

Write-Host '--- git log recent ---'
git log -n 5 --pretty=oneline

$watch.Kill()
Remove-Item $dest -Force
Write-Host 'cleaned'