$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$dir = "c:\Users\hirak\Desktop\2nd-Brain\24_UnrealMCP"
if (-not (Test-Path $dir)) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}
Write-Host "フォルダ [24_UnrealMCP] を作成・確認しました。"

Start-Sleep -Seconds 3

$readmePath = "$dir\README.md"
$readmeContent = @"
# Unreal Engine AI連携（MCP）用フォルダ

このフォルダは、AI（私）がUnreal Engineを直接操作するための準備フォルダです。

## 🎮 次にあなたがUnreal Engineで行うこと

1. Unreal Engine 5.8のエディタを開きます。
2. 上部メニューの **編集** ＞ **プラグイン** を開きます。
3. 検索窓に「**Unreal MCP**」と入力し、出てきたプラグインにチェックを入れて有効化します。
4. エディタを再起動するよう求められるので、再起動します。
5. 再起動後、**編集** ＞ **エディタの環境設定** を開きます。
6. 左のメニューから **Model Context Protocol** を選び、「Auto Start Server（サーバーの自動起動）」にチェックを入れます。

これで、AIがUnreal Engineと「お話し」できるようになります！
"@
Set-Content -Path $readmePath -Value $readmeContent -Encoding UTF8
Write-Host "案内文 (README.md) を作成しました。"

Start-Sleep -Seconds 3

$dummyConfig = "$dir\config.txt"
$configContent = @"
【AI用設定ファイル】
このファイルはAIがUnreal Engineを見つけるための目印です。
"@
Set-Content -Path $dummyConfig -Value $configContent -Encoding UTF8
Write-Host "設定ファイルを作成しました。"

Start-Sleep -Seconds 3
Write-Host "すべての準備作業が完了しました。"
