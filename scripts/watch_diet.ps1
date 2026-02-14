# Watcher for Diet Screenshots
# Monitors the Desktop for new images and runs the python extractor

$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = "C:\Users\hirak\Desktop"
$watcher.Filter = "*.*" # Watch all, filter extensions in event
$watcher.IncludeSubdirectories = $false
$watcher.EnableRaisingEvents = $true

$action = {
    $path = $Event.SourceEventArgs.FullPath
    $ext = [System.IO.Path]::GetExtension($path).ToLower()
    
    # Filter for images
    if ($ext -in @(".png", ".jpg", ".jpeg", ".bmp")) {
        Write-Host "New image detected: $path"
        
        # Wait a bit for the file handle to be released (screenshot tools might still be writing)
        Start-Sleep -Seconds 2
        
        # Call the Python script
        $pythonScript = "C:\Users\hirak\Desktop\2nd-Brain\scripts\auto_diet_screenshot.py"
        $pythonPath = "python" # Assuming python is in PATH
        
        Write-Host "Running analysis..."
        Start-Process -FilePath $pythonPath -ArgumentList "`"$pythonScript`"", "`"$path`"" -WindowStyle Hidden
    }
}

Register-ObjectEvent $watcher "Created" -Action $action

Write-Host "Monitoring Desktop for screenshots..."
while ($true) {
    Start-Sleep -Seconds 5
}
