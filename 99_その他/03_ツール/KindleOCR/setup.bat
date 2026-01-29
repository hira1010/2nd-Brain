@echo off
cd /d %~dp0
echo --- Kindle OCR セットアップを開始します ---
python -m pip install -r requirements.txt
echo.
echo インストールが完了しました。
pause
