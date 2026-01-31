# Test commit script called by watcher. Calls the real commit script with Push disabled to avoid pushing.
& "$PSScriptRoot\commit_all.ps1" -Message "Test commit from watcher" -Push:$false
