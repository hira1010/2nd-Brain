param(
    [string]$FlagPath = "${PSScriptRoot}\.autocommit-enabled"
)

if (Test-Path -Path $FlagPath) {
    Remove-Item -Path $FlagPath -Force
    Write-Host "Autocommit disabled: removed $FlagPath"
} else {
    Write-Host "Autocommit already disabled: $FlagPath"
}
