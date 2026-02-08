param(
    [string]$ProcessName = "Antigravity",
    [int]$PollSeconds = 2,
    [string]$CommitScript = "${PSScriptRoot}\commit_all.ps1",
    [string]$LogFile = "${PSScriptRoot}\watcher.log",
    [string]$EnableFlag = "${PSScriptRoot}\.autocommit-enabled"
)

# 注意: ProcessName はプロセス名（拡張子なし）、例: MyApp.exe -> "MyApp"

# ログファイルがなければ作成
if (-not (Test-Path -Path $LogFile)) {
    New-Item -Path $LogFile -ItemType File -Force | Out-Null
}

$enabled = Test-Path -Path $EnableFlag
if (-not $enabled) {
    "Watcher disabled because flag file was not found: $EnableFlag ($(Get-Date))" | Out-File -FilePath $LogFile -Encoding utf8 -Append
    exit 0
}

$running = $false
$trackedPid = $null
"Watcher started for process '$ProcessName' at $(Get-Date)" | Out-File -FilePath $LogFile -Encoding utf8 -Append

while ($true) {
    try {
        $ps = Get-Process -Name $ProcessName -ErrorAction SilentlyContinue
        if ($ps) {
            if (-not $running) {
                # 複数プロセスがある場合は最新のものを追跡
                $procToTrack = $ps | Sort-Object StartTime -Descending | Select-Object -First 1
                $trackedPid = $procToTrack.Id
                $running = $true
                "Detected start of process $($procToTrack.Name) (PID $trackedPid) at $(Get-Date)" | Out-File -FilePath $LogFile -Encoding utf8 -Append
            } else {
                # 既に追跡中の場合はその PID がまだ存在するかを確認
                if ($trackedPid -and -not (Get-Process -Id $trackedPid -ErrorAction SilentlyContinue)) {
                    "Tracked PID $trackedPid disappeared unexpectedly at $(Get-Date). Running commit script..." | Out-File -FilePath $LogFile -Encoding utf8 -Append
                    try {
                        $arg = "-NoProfile -ExecutionPolicy Bypass -File `"$CommitScript`""
                        $proc = Start-Process -FilePath "powershell.exe" -ArgumentList $arg -WindowStyle Hidden -PassThru -Wait
                        "Commit script finished at $(Get-Date) with exit code $($proc.ExitCode)" | Out-File -FilePath $LogFile -Encoding utf8 -Append
                    } catch {
                        "Error running commit script: $_" | Out-File -FilePath $LogFile -Encoding utf8 -Append
                    }
                    $running = $false
                    $trackedPid = $null
                }
            }
        } else {
            if ($running) {
                "Detected exit of process $trackedPid at $(Get-Date). Running commit script..." | Out-File -FilePath $LogFile -Encoding utf8 -Append
                try {
                    $arg = "-NoProfile -ExecutionPolicy Bypass -File `"$CommitScript`""
                    $proc = Start-Process -FilePath "powershell.exe" -ArgumentList $arg -WindowStyle Hidden -PassThru -Wait
                    "Commit script finished at $(Get-Date) with exit code $($proc.ExitCode)" | Out-File -FilePath $LogFile -Encoding utf8 -Append
                } catch {
                    "Error running commit script: $_" | Out-File -FilePath $LogFile -Encoding utf8 -Append
                }
                $running = $false
                $trackedPid = $null
            }
        }
    } catch {
        "Watcher error: $_" | Out-File -FilePath $LogFile -Encoding utf8 -Append
    }
    Start-Sleep -Seconds $PollSeconds
}
