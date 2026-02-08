param(
    [string]$FlagPath = "${PSScriptRoot}\.autocommit-enabled"
)

if (-not (Test-Path -Path $FlagPath)) {
    New-Item -Path $FlagPath -ItemType File -Force | Out-Null
}

Write-Host "Autocommit enabled: $FlagPath"
