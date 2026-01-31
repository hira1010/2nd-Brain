$ErrorActionPreference = "Stop"
# Move to repo root
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location (Join-Path $scriptDir "..")

$source = "$env:windir\System32\notepad.exe"
$dest = Join-Path $PWD "scripts\Antigravity.exe"
Copy-Item -Path $source -Destination $dest -Force

$watch = Start-Process -FilePath powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PWD\scripts\watch_antigravity.ps1`" -ProcessName Antigravity -PollSeconds 1" -WindowStyle Hidden -PassThru
Write-Host "Watcher PID: $($watch.Id)"
Start-Sleep -Seconds 1

$testfile = "scripts\auto_test_commit_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
Set-Content -Path $testfile -Value "autocommit test"

$proc = Start-Process -FilePath $dest -PassThru
Write-Host "Started Antigravity PID:$($proc.Id)"
Start-Sleep -Seconds 3

$proc.Kill()
Write-Host "Killed Antigravity"
Start-Sleep -Seconds 4

if (Test-Path scripts\watcher.log) {
    Write-Host '--- watcher.log (tail) ---'
    Get-Content scripts\watcher.log -Tail 20
} else {
    Write-Host '--- no watcher.log ---'
}

Write-Host '--- git log (recent) ---'
git log -n 5 --pretty=oneline

$watch.Kill()
Write-Host 'Stopped watcher'

Remove-Item $dest -Force
Write-Host 'Cleaned up'