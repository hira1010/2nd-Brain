@echo off
chcp 65001 > nul
set PYTHONUTF8=1

echo ==========================================
echo  配当金データ同期システム (v1.0)
echo ==========================================

echo.
echo [1/3] 環境を確認中...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Pythonが見つかりません。インストールしてください。
    pause
    exit /b
)

echo.
echo [2/3] 必要なライブラリを準備中...
pip install --disable-pip-version-check --quiet gspread oauth2client pandas requests > nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] ライブラリのインストールに失敗した可能性があります。
    echo 手動で以下のコマンドを実行することを推奨します:
    echo pip install gspread oauth2client pandas requests
)

echo.
echo [3/3] 同期を実行中...
if not exist "%~dp0..\credentials.json" (
    echo [ERROR] 'credentials.json' が見つかりません。
    echo 以下のフォルダ（Desktop\2nd-Brain）に配置してください:
    echo %~dp0..
    pause
    exit /b
)

python "%~dp0sync_dividend.py"

echo.
echo ==========================================
echo  処理が完了しました。
echo ==========================================
pause
