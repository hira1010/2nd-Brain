
# Setup Vidu AI Environment

Write-Host "=== Setting up Vidu AI Environment ===" -ForegroundColor Cyan

# Check for Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not installed."
    exit 1
}

# Install dependencies
Write-Host "Installing requests and python-dotenv..." -ForegroundColor Green
pip install requests python-dotenv

# Create .env template if not exists
$EnvFile = Join-Path $PSScriptRoot ".env"
if (-not (Test-Path $EnvFile)) {
    Write-Host "Creating .env template..." -ForegroundColor Yellow
    "VIDU_API_KEY=your_api_key_here" | Out-File $EnvFile -Encoding utf8
    Write-Host "Please edit $EnvFile and set your VIDU_API_KEY." -ForegroundColor Magenta
}

Write-Host "=== Setup Complete! ===" -ForegroundColor Cyan
