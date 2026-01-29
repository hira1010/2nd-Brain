@echo off
cd /d %~dp0
echo 3秒後に解析を開始します。Kindleの画面を最前面にしてください...
python kindle_ocr.py
pause
