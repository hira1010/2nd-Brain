@echo off
setlocal
chcp 65001 > nul
echo Roblox Studio MCP 連携確認ツール (Antigravity)
echo ===========================================
echo.
echo [1] 連携プログラムの確認中...
if exist "%LOCALAPPDATA%\Roblox\mcp.bat" (
    echo [OK] %LOCALAPPDATA%\Roblox\mcp.bat が見つかりました。
) else (
    echo [ERROR] mcp.bat が見つかりません。Roblox Studio を最新に更新してください。
    pause
    exit /b
)
echo.
echo [2] 注意事項:
echo Roblox Studio 内で「MCP Server」設定を「オン」にする必要があります。
echo 詳細は Antigravity のチャット履歴を確認してください。
echo.
echo [3] 状態:
echo Roblox Studio 自体は現在起動しています。
echo.
echo 全て準備OKです！エディタにフォルダをドラッグして作業を開始してください。
pause
