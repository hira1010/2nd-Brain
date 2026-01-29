# Kindle OCR Tool セットアップガイド

このツールは、Kindle Cloud Reader のページを自動でめくり、スクリーンショットを撮影してテキスト化（OCR）するためのものです。
日本の著作権法第30条の4（情報解析のための複製）に準拠した設計となっています。

## 1. 事前準備 (Windows)

### Tesseract OCR のインストール
1. [Tesseract OCR Windows Installer](https://github.com/UB-Mannheim/tesseract/wiki) からインストーラーをダウンロードして実行します。
2. インストール中、**「Additional script data」から「Japanese」** を、**「Additional language data」から「Japanese / Japanese (vertical)」** にチェックを入れてインストールしてください。
3. デフォルトのインストール先は `C:\Program Files\Tesseract-OCR` です。

### ライブラリのインストール
ターミナルで以下のコマンドを実行します：
```bash
pip install -r requirements.txt
```

## 2. 設定 (`kindle_ocr.py`)

スクリプト内の以下の項目を自分の環境に合わせて調整してください。

- `pytesseract.pytesseract.tesseract_cmd`: Tesseract のインストールパス
- `CAPTURE_REGION`: 撮影範囲 (x, y, width, height)
- `lang='jpn'`: 縦書きの本を解析する場合は `'jpn_vert'` に変更してください。

## 3. 使い方

1. ブラウザで [Kindle Cloud Reader](https://read.amazon.co.jp/) を開き、解析したい本を表示します。
2. コマンドプロンプト等でスクリプトを実行します。
   ```bash
   python kindle_ocr.py
   ```
3. 実行後、**3秒以内にブラウザの Kindle 画面を最前面**にしてください。
4. 自動でページめくりと解析が始まります。マウスやキーボードには触れずに待機してください。

## ⚖️ 法的・倫理的運用ルール

- **解析目的限定**: 本ツールは「AIによるテキスト解析・要約」を目的としています。
- **個人利用限定**: 生成されたテキストファイルは、あなたの「第2の脳」内でのみ利用し、他人へ渡したり公開したりしないでください。
- **享受の禁止**: ツールで取得した内容を、通常の読書目的（享受目的）で利用し続けることは法律の趣旨から外れる可能性があるため、解析が終わったら適宜活用してください。
