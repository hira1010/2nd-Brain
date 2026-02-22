
# GitHubへの初期デプロイ補助スクリプト

param(
    [string]$RepoUrl = ""
)

Write-Host "=== GitHub Deployment Helper ===" -ForegroundColor Cyan

# Check for Git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "Gitがインストールされていません。"
    exit 1
}

# git init
if (-not (Test-Path ".git")) {
    Write-Host "Initializing Git..." -ForegroundColor Green
    git init
}

# Add & Commit
Write-Host "Staging files..." -ForegroundColor Green
git add .
git commit -m "Initial commit from Antigravity"

# Remote setup
if ($RepoUrl) {
    Write-Host "Linking to remote: $RepoUrl" -ForegroundColor Green
    git remote add origin $RepoUrl
    git branch -M main
    git push -u origin main
    Write-Host "✅ Pushed to GitHub!" -ForegroundColor Cyan
}
else {
    Write-Host "リポジトリURLが指定されていません。手動で以下を実行してください：" -ForegroundColor Yellow
    Write-Host "git remote add origin <YOUR_REPO_URL>"
    Write-Host "git branch -M main"
    Write-Host "git push -u origin main"
}
