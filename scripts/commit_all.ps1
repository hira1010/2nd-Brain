param()

$scriptPath = Join-Path $PSScriptRoot "commit_all.py"
if (-not (Test-Path -LiteralPath $scriptPath)) {
    Write-Error "commit_all.py not found: $scriptPath"
    exit 1
}

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

python -X utf8 $scriptPath
exit $LASTEXITCODE
