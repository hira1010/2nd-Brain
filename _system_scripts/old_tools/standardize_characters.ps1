$root = "c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画"
$files = Get-ChildItem -Path $root -Recurse -Filter "*プロンプト.md"

$newBlock = @"
### Characters:
- Remi: (Crimson RED blazer, Black lace top). (Silky SILVER hair), (RED eyes). NO GLOVES. (ONLY ONE Remi per panel).
- Yuto: (Traditional SOLID BLACK Gakuran school uniform, gold buttons). (Short Black hair). BARE HANDS. (ONLY ONE Yuto per panel).
"@

# Regex to remove existing Character blocks.
# Matches "### Characters:" followed by Remi and Yuto lines.
# (?m) ensures ^ matches start of line.
$removePattern = "(?m)^\s*### Characters:(\r?\n)+^\s*- Remi:.*(\r?\n)+^\s*- Yuto:.*(\r?\n)+"

# Regex to find ARCHITECTURE line
$archPattern = "(?m)^(ARCHITECTURE:.*)$"

$count = 0
foreach ($file in $files) {
    try {
        $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
        
        # Step 1: Remove existing character blocks (to avoid duplication/inconsistency)
        $cleanContent = $content -replace $removePattern, ""
        
        # Step 2: Insert the unified character block after every ARCHITECTURE line
        # We add newlines ensuring separation
        $newContent = $cleanContent -replace $archPattern, ('$1' + "`r`n`r`n" + $newBlock + "`r`n")
        
        # Only write if changes occurred (Step 1 or Step 2 changed something)
        if ($newContent -ne $content) {
            Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8 -NoNewline
            Write-Host "Updated: $($file.Name)"
            $count++
        }
    }
    catch {
        Write-Error "Failed to process $($file.Name): $_"
    }
}

Write-Host "Total files updated: $count"
