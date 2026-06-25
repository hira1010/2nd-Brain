$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("C:\Users\hirak\Desktop\Start_MyProject.lnk")
$Shortcut.TargetPath = "C:\Users\hirak\Documents\Unreal Projects\MyProject\MyProject.uproject"
$Shortcut.Save()
Write-Host "Shortcut created"
