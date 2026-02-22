# Run this script to install NuGet provider and BurntToast with elevation (UAC will be shown)
# Usage: Right-click -> Run with PowerShell, or run from PowerShell (no admin) to trigger UAC prompt.

function Is-Admin {
    $current = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $current.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

if (-not (Is-Admin)) {
    Write-Host "Not running as admin. Relaunching with elevation..."
    Start-Process -FilePath "powershell.exe" -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit 0
}

# Now running elevated
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
Write-Host 'Installing NuGet provider...'
Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force -ErrorAction Stop
Import-PackageProvider -Name NuGet -Force -ErrorAction SilentlyContinue
Write-Host 'Trusting PSGallery...'
Set-PSRepository -Name 'PSGallery' -InstallationPolicy Trusted -ErrorAction SilentlyContinue
Write-Host 'Installing BurntToast...'
Install-Module -Name BurntToast -Scope AllUsers -Force -AllowClobber -ErrorAction Stop
Import-Module BurntToast -ErrorAction Stop
New-BurntToastNotification -Text 'Test', 'BurntToast installed (elevated)'
Write-Host 'Done'
