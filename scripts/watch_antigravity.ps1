param(
    [string]$ProcessName = "Antigravity",
    [int]$PollSeconds = 2,
    [string]$CommitScript = "${PSScriptRoot}\commit_all.ps1",
    [string]$LogFile = "${PSScriptRoot}\watcher.log"
)

# 注意: ProcessName はプロセス名（拡張子なし）、例: MyApp.exe -> "MyApp"

$running = $false
"Watcher started for process '$ProcessName' at $(Get-Date)" | Out-File -FilePath $LogFile -Encoding utf8 -Append

while ($true) {
    $p = Get-Process -Name $ProcessName -ErrorAction SilentlyContinue
    if ($p) {
        if (-not $running) {
            $running = $true
            "Detected start of process at $(Get-Date)" | Out-File -FilePath $LogFile -Encoding utf8 -Append
        }
    } else {
        if ($running) {
            "Detected exit of process at $(Get-Date). Running commit script..." | Out-File -FilePath $LogFile -Encoding utf8 -Append
            # 実行は別の PowerShell を呼び出して確実に動くようにする
            & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $CommitScript
            "Commit script finished at $(Get-Date)" | Out-File -FilePath $LogFile -Encoding utf8 -Append
            $running = $false
        }
    }
    Start-Sleep -Seconds $PollSeconds
}
