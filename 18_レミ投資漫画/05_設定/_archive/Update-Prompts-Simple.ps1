# Update-Prompts-Simple.ps1
[CmdletBinding()]
param()
$ErrorActionPreference = "Stop"
$TargetDir = "c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画"

# ファイルリスト取得
$Files = Get-ChildItem -Path $TargetDir -Recurse | Where-Object { $_.Name -like "No*_プロンプト.md" }

if ($Files.Count -eq 0) {
    Write-Host "No files found."
    exit
}

# 挿入するテキスト（改行はあとで置換）
$AnatomyText = "CRITICAL ANATOMICAL REQUIREMENTS:|MAX|- Each character has EXACTLY TWO HANDS|MAX|- Each hand has EXACTLY FIVE FINGERS|MAX|- Remi wears NO GLOVES - bare hands only|MAX|- Yuto wears NO GLOVES - bare hands only|MAX|- Anatomically correct human proportions"
$AnatomyText = $AnatomyText.Replace("|MAX|", [Environment]::NewLine)

$PrefixText = "画像生成を行ってください。以下のプロンプトに基づいて、縦長のマンガ画像を生成してください。"

foreach ($File in $Files) {
    try {
        $RawContent = [System.IO.File]::ReadAllText($File.FullName)
        $NewContent = $RawContent

        # 1. Anatomy Block
        if (-not $NewContent.Contains("CRITICAL ANATOMICAL REQUIREMENTS")) {
            $TargetStr = "Resolution: High quality manga illustration"
            $NewContent = $NewContent.Replace($TargetStr, $TargetStr + [Environment]::NewLine + [Environment]::NewLine + $AnatomyText)
        }

        # 2. Hands (Remi)
        $RemiTarget = "Remi (Woman): Silky SILVER hair, Vibrant RED eyes, Red blazer, Black lace top, Cool & Intelligent."
        if ($NewContent.Contains($RemiTarget) -and -not $NewContent.Contains("BARE HANDS")) {
            $NewContent = $NewContent.Replace($RemiTarget, $RemiTarget + " BARE HANDS (no gloves).")
        }

        # 3. Hands (Yuto)
        $YutoTarget = "Yuto (Boy): Short Black hair, Black GAKURAN school uniform, Energetic & Learner."
        if ($NewContent.Contains($YutoTarget) -and -not $NewContent.Contains("BARE HANDS")) {
            $NewContent = $NewContent.Replace($YutoTarget, $YutoTarget + " BARE HANDS (no gloves).")
        }

        # 4. Prefix
        if (-not $NewContent.Contains($PrefixText)) {
            $CodeBlockStart = "```text"
            # 最初の出現のみ置換したいがReplaceは全部置換する。しかしテキストブロック以外の ```text はないはず
            # 念のため単純置換
            $NewContent = $NewContent.Replace($CodeBlockStart, $CodeBlockStart + [Environment]::NewLine + $PrefixText + [Environment]::NewLine)
        }

        if ($NewContent -ne $RawContent) {
            [System.IO.File]::WriteAllText($File.FullName, $NewContent)
            Write-Host "Updated: $($File.Name)"
        }
    }
    catch {
        Write-Host "Error processing $($File.Name): $_"
    }
}
Write-Host "All done."
