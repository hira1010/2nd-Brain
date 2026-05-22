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
    "監視が無効化されています。フラグファイルが見つかりません: $EnableFlag ($(Get-Date))" | Out-File -FilePath $LogFile -Encoding utf8 -Append
    exit 0
}

$running = $false
$trackedPid = $null
"プロセス '$ProcessName' の監視を開始しました。時刻: $(Get-Date)" | Out-File -FilePath $LogFile -Encoding utf8 -Append

while ($true) {
    try {
        $ps = Get-Process -Name $ProcessName -ErrorAction SilentlyContinue
        if ($ps) {
            if (-not $running) {
                # 複数プロセスがある場合は最新のものを追跡
                $procToTrack = $ps | Sort-Object StartTime -Descending | Select-Object -First 1
                $trackedPid = $procToTrack.Id
                $running = $true
                "プロセス $($procToTrack.Name) の起動を検出しました (PID $trackedPid)。時刻: $(Get-Date)" | Out-File -FilePath $LogFile -Encoding utf8 -Append
            } else {
                # 既に追跡中の場合はその PID がまだ存在するかを確認
                if ($trackedPid -and -not (Get-Process -Id $trackedPid -ErrorAction SilentlyContinue)) {
                    "追跡中の PID $trackedPid が予期せず終了しました。時刻: $(Get-Date)。コミットスクリプトを実行します..." | Out-File -FilePath $LogFile -Encoding utf8 -Append
                    try {
                        $arg = "-NoProfile -ExecutionPolicy Bypass -File `"$CommitScript`""
                        $proc = Start-Process -FilePath "powershell.exe" -ArgumentList $arg -WindowStyle Hidden -PassThru -Wait
                        "コミットスクリプトが正常終了しました。時刻: $(Get-Date)、終了コード: $($proc.ExitCode)" | Out-File -FilePath $LogFile -Encoding utf8 -Append
                    } catch {
                        "コミットスクリプトの実行中にエラーが発生しました: $_" | Out-File -FilePath $LogFile -Encoding utf8 -Append
                    }
                    $running = $false
                    $trackedPid = $null
                }
            }
        } else {
            if ($running) {
                "プロセス $trackedPid の終了を検出しました。時刻: $(Get-Date)。コミットスクリプトを実行します..." | Out-File -FilePath $LogFile -Encoding utf8 -Append
                try {
                    $arg = "-NoProfile -ExecutionPolicy Bypass -File `"$CommitScript`""
                    $proc = Start-Process -FilePath "powershell.exe" -ArgumentList $arg -WindowStyle Hidden -PassThru -Wait
                    "コミットスクリプトが正常終了しました。時刻: $(Get-Date)、終了コード: $($proc.ExitCode)" | Out-File -FilePath $LogFile -Encoding utf8 -Append
                } catch {
                    "コミットスクリプトの実行中にエラーが発生しました: $_" | Out-File -FilePath $LogFile -Encoding utf8 -Append
                }
                $running = $false
                $trackedPid = $null
            }
        }
    } catch {
        "監視中にエラーが発生しました: $_" | Out-File -FilePath $LogFile -Encoding utf8 -Append
    }
    Start-Sleep -Seconds $PollSeconds
}
