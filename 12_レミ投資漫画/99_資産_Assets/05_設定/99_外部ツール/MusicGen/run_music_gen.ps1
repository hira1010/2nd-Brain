
# Wrapper script to run generate_music.py using the correct uv environment

param(
    [string]$Prompt = "upbeat pop music",
    [string]$Lyrics = "",
    [int]$Duration = 30,
    [string]$Out = ""
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RepoDir = Join-Path $ScriptDir "ACE-Step-1.5"
$GenScript = Join-Path $ScriptDir "generate_music.py"

if (-not (Test-Path $RepoDir)) {
    Write-Error "ACE-Step-1.5 directory not found. Please run setup_music_gen.ps1 first."
    exit 1
}

# Change to the repo directory so 'uv run' finds the correct project context/virtualenv
Push-Location $RepoDir

Write-Host ">>> Running Music Generation in UV Environment..." -ForegroundColor Cyan
Write-Host "Prompt: $Prompt"
Write-Host "Duration: $Duration"

# Fix encoding issues on Windows
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 > $null
$Env:PYTHONUTF8 = "1"

$CmdArgs = @(
    "run",
    "python", 
    $GenScript, 
    "--prompt", "`"$Prompt`"", 
    "--duration", $Duration
)

if ($Lyrics) {
    $CmdArgs += "--lyrics"
    $CmdArgs += "`"$Lyrics`""
}

if ($Out) {
    $CmdArgs += "--out"
    $CmdArgs += "`"$Out`""
}

# Execute using direct venv python to bypass uv encoding issues
$VenvPython = Join-Path $RepoDir ".venv\Scripts\python.exe"

if (-not (Test-Path $VenvPython)) {
    Write-Error "Virtual environment python found at $VenvPython. Please run setup_music_gen.ps1."
    exit 1
}

# Construct command arguments manually for Start-Process or direct invocation
# Using & operator for direct invocation
& $VenvPython $GenScript --prompt "$Prompt" --duration $Duration --lyrics "$Lyrics" --out "$Out"

Pop-Location
