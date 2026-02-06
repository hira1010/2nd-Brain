
# Setup ACE-Step 1.5 Music Generation Environment

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$TargetDir = Join-Path $ScriptDir "ACE-Step-1.5"

Write-Host "=== Setting up ACE-Step 1.5 Music Generator ===" -ForegroundColor Cyan

# 1. Check Git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "Git is not installed. Please install Git to proceed."
    exit 1
}

# 2. Clone Repository
if (-not (Test-Path $TargetDir)) {
    Write-Host "Cloning ACE-Step-1.5 repository..." -ForegroundColor Green
    git clone https://github.com/ace-step/ACE-Step-1.5.git $TargetDir
}
else {
    Write-Host "Repository already exists at $TargetDir" -ForegroundColor Yellow
}

# 3. Change Directory
Set-Location $TargetDir

# 4. Create Virtual Environment (Standard)
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Green
    python -m venv .venv
}

# 5. Install Dependencies (using uv into venv)
Write-Host "Installing dependencies..." -ForegroundColor Green
# Activate venv for the session
. .\.venv\Scripts\Activate.ps1

# Install uv inside venv or use global, targeting this venv
python -m pip install uv
uv pip install -e .

# 6. Download Models
Write-Host "Downloading Default Models (This may take a while)..." -ForegroundColor Green
try {
    # Ensure acestep-download is run from the venv
    & .\.venv\Scripts\acestep-download.exe --model acestep-v15-turbo
    & .\.venv\Scripts\acestep-download.exe --model acestep-5Hz-lm-1.7B
    Write-Host "Model download complete." -ForegroundColor Green
}
catch {
    Write-Host "Manual download might be required if this step fails." -ForegroundColor Yellow
    Write-Error $_
}

Write-Host "=== Setup Complete! ===" -ForegroundColor Cyan
Write-Host "You can now generate music using run_music_gen.ps1"
