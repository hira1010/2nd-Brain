# 全体的なリファクタリング計画 (overall_refactoring)

プロジェクト共通のスクリプト群（`18_システム`内）を、機能はそのままに、保守性と可読性を高めるために再構成します。

## Proposed Changes

### 1. 共通基盤の導入

重複している定数やロジックを整理し、一箇所で管理できるようにします。

#### [NEW] [manga_config.py](file:///c:/Users/hirak/Desktop/2nd-Brain/18_システム/manga_config.py)

以下の定数を集約します：

- ターゲットディレクトリ (`BASE_DIR`, `TARGET_DIRS`)
- シーン（背景）バリエーション (`SCENES`)
- キャラクター設定（レミ、優斗のビジュアルロック）
- プロンプトテンプレート

#### [NEW] [manga_utils.py](file:///c:/Users/hirak/Desktop/2nd-Brain/18_システム/manga_utils.py)

以下の共通関数を集約します：

- Markdownファイルからの情報抽出 (`extract_info`)
- セリフの抽出・フォールバック処理
- ファイル操作のラッパー
- 型ヒント付きの共通ロガー

---

### 2. 各スクリプトのリファクタリング

#### [MODIFY] [refactor_prompts.py](file:///c:/Users/hirak/Desktop/2nd-Brain/18_システム/refactor_prompts.py)

- `manga_config` と `manga_utils` を使用するように変更。
- 重複ロジックを削除し、コードを簡素化。
- 型ヒントと詳細なログ出力を追加。

#### [MODIFY] [smart_refactor.py](file:///c:/Users/hirak/Desktop/2nd-Brain/18_システム/smart_refactor.py)

- `refactor_prompts.py` とのロジック統合。
- 不要な重複を排除。

#### [MODIFY] [sync_assets.py](file:///c:/Users/hirak/Desktop/2nd-Brain/18_システム/sync_assets.py)

- `Active_Context.md` の規約に準拠したさらなるブラッシュアップ。
- パス管理の共通化。

---

### 3. ビジュアル・セットアップガイドの作成

ユーザーからのフィードバックに基づき、プレミアムなデザインのセットアップガイドを作成します。

#### [NEW] [setup_guide.html](file:///c:/Users/hirak/Desktop/2nd-Brain/18_システム/setup_guide.html)

- モダンで高品質なダークモードUI。
- ステップバイステップのセットアップ手順（CDPポート設定、スクリプト実行準備）。
- インタラクティブな「スクリプトコピー」機能（シミュレーション）。

---

### 4. 環境問題（Fatal Error）への恒久的な回避策

Python起動時の `UnicodeDecodeError` を回避し、誰でも確実にスクリプトを実行できるようにします。

#### [NEW] [run_system.ps1](file:///c:/Users/hirak/Desktop/2nd-Brain/18_システム/run_system.ps1)

- 適切なエンコーディング（UTF-8モード）とオプション（`-S` 等の必要に応じたフラグ）を自動適用してスクリプトを安全に起動するためのランチャー。

---

#### [MODIFY] [smart_refactor.py](file:///c:/Users/hirak/Desktop/2nd-Brain/18_システム/smart_refactor.py)

- `refactor_prompts.py` とのロジック統合。
- 不要な重複を排除。

#### [MODIFY] [sync_assets.py](file:///c:/Users/hirak/Desktop/2nd-Brain/18_システム/sync_assets.py)

- `Active_Context.md` の規約に準拠したさらなるブラッシュアップ。
- パス管理の共通化。

---

## Verification Plan

### Automated Tests

既存のテストコードがないため、以下の検証スクリプトを実行します：

- **Dry-run検証**: `python 18_システム/smart_refactor.py --target "test_file.md"` (テスト用ファイル) を実行し、出力結果が意図通りか確認。
- **Importチェック**: 全リファクタリング済みスクリプトが正常にインポート可能か確認。

### Manual Verification

- リファクタリング前後の生成物（Markdownファイル）を比較し、機能内容（プロンプトの内容、変数、セリフ）に差分がないことを確認します。
- ログ出力が読みやすく、エラー時に適切なメッセージが出ることを確認します。
