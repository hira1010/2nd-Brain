# Roblox Studioのインストールフォルダを指定
$robloxDir = "$env:LOCALAPPDATA\Roblox\Versions"

# フォルダ内から RobloxStudioBeta.exe を検索（最も新しいものを1つ取得）
$studioExe = Get-ChildItem -Path $robloxDir -Filter "RobloxStudioBeta.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1

if ($studioExe) {
    Write-Host "Roblox Studioが見つかりました: $($studioExe.FullName)"
    # バックグラウンドで起動
    Start-Process -FilePath $studioExe.FullName
    Write-Host "Roblox Studioを起動しました。"
} else {
    Write-Host "エラー: Roblox Studioが見つかりませんでした。インストールされているか確認してください。"
    exit 1
}
