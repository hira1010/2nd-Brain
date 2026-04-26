# 2nd-Brain 環境構築ガイド (環境コピー用)

このプロジェクトを別のPCで動かすための手順です。

## 1. 必要なソフトウェアのインストール
- **Python 3.12**: [python.org](https://www.python.org/) からダウンロード。
  - インストール時、必ず **"Add Python to PATH"** にチェックを入れてください。
- **Node.js (LTS)**: [nodejs.org](https://nodejs.org/) からダウンロード。
- **Git**: [git-scm.com](https://git-scm.com/) からダウンロード。
- **Google Drive for Desktop**: Gドライブをマウントするために必要です。

## 2. ライブラリのセットアップ
ターミナル（PowerShell等）でプロジェクトのルートに移動し、以下を実行してください。

```powershell
# Pythonライブラリのインストール
pip install -r requirements.txt

# 各プロジェクトの依存関係インストール
cd 04_Remotion/my-video
npm install
```

## 3. ゲームエンジンのパス設定
`scripts/antigravity_check.py` 内の `RENPY_SDK` など、絶対パスが記述されている箇所を、新しいPCの場所に合わせて書き換えてください。

## 4. 日常の運用
このPCでもショートカット「5」を実行できるように、Pythonへのパスが通っていることを確認してください。
迷ったときは、このフォルダの AI アシスタントに「環境構築を手伝って」と伝えてください。
