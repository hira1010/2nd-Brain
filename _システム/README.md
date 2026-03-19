# 18_システム - Second Brain 自動化システム

このフォルダには、Second Brainプロジェクトの自動化スクリプトとプロンプト、設定ファイルが含まれています。

## 📁 フォルダ構成

```
18_システム/
├── 01_Prompts/           # 各種AIプロンプト集
│   ├── Workflow_Prompts/  # 日次・週次ワークフロー
│   ├── X長文ポスト作成プロンプト/
│   └── ...
├── devtools/             # 開発補助ツール
├── scripts/              # (今後) 実行スクリプト集約先
├── sync_assets.py        # 資産データ同期スクリプト
├── refactor_prompts.py   # 漫画プロンプト生成
├── smart_refactor.py     # スマートリファクタリング
├── Active_Context.md     # AI行動ルール定義
└── README.md            # このファイル
```

## 🚀 主要スクリプト

### sync_assets.py

Googleスプレッドシートから配当金・資産データを取得し、Markdownを更新。

```bash
python sync_assets.py
```

**機能**:

- スプレッドシートとの自動同期
- Markdownテーブルの動的更新
- 偶数日に自動提案（Active_Context.mdで制御）

---

### refactor_prompts.py

レミ投資漫画のプロンプトを一括生成・更新。

```bash
python refactor_prompts.py
```

**機能**:

- 統一フォーマットでプロンプト生成
- キャラクター設定の一貫性維持
- バッチ処理対応

---

### smart_refactor.py

コードやドキュメントの賢いリファクタリング補助。

```bash
python smart_refactor.py [target_file]
```

---

## ⚙️ 設定ファイル

### Active_Context.md

AIアシスタント（Antigravity）の動作ルールを定義。

**定義内容**:

- 偶数日の資産同期ルール
- プロジェクト固有の自動化ロジック

---

## 📋 プロンプト体系

`01_Prompts/` には以下のカテゴリのプロンプトがあります：

- **Workflow_Prompts**: 日次・週次のタスク管理
- **X長文ポスト作成**: SNS投稿の自動生成
- **Note記事作成**: Note記事の執筆支援
- **Brain教材執筆**: 教材コンテンツ制作

詳細は各フォルダ内のREADMEを参照。

---

## 🔧 開発者向け情報

### 依存関係

```bash
pip install pandas requests
```

### コーディング規約

1. **型ヒント**: すべての関数に型を明記
2. **エラーハンドリング**: try-exceptで適切に処理
3. **ドキュメント**: docstringで機能を説明
4. **ログ**: 進捗と結果を明確に出力

参考実装: `sync_assets.py`

---

## 📝 今後の予定

- [ ] スクリプトを`scripts/`に集約
- [ ] 各カテゴリにREADMEを追加
- [ ] テストスイートの整備
- [ ] CI/CD統合の検討

---

**最終更新**: 2026-02-05  
**メンテナ**: Antigravity AI Assistant
