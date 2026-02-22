# システム全体のリファクタリング計画

現状の「第2の脳」システムの機能を維持したまま、コードの品質、保守性、およびポータビリティを向上させるためのリファクタリングを行います。

## ユーザー確認事項

> [!IMPORTANT]
>
> 1. ハードコードされた絶対パス（`c:\Users\hirak\...`）を、プロジェクトのルートディレクトリからの相対パスに置き換えます。これにより、別の環境でも動作するようになります。
> 2. `18_システム` と `_system_scripts` に点在する重複・類似機能（体重同期など）を整理し、共通ライブラリ化します。
> 3. ファイル内の日本語の文字化け（文字コードの問題）を一括修正します。
> 4. コード内のコメントを原則として日本語に統一します。

## 変更内容の概要

### 1. 共通ライブラリ (`lib/`) の新設

すべてのスクリプトから利用可能な共通基盤を作成します。

#### [NEW] [config.py](file:///c:/Users/hirak/Desktop/2nd-Brain/lib/config.py)

- プロジェクトルートの自動検知（`.git` や `SOUL.md` を目印にする）。
- スプレッドシートIDや共通パスの設定を集約。

#### [NEW] [utils.py](file:///c:/Users/hirak/Desktop/2nd-Brain/lib/utils.py)

- ログ出力のセットアップ（日本語対応）。
- 堅牢なファイル入出力（文字コード問題の回避）。
- 共通の正規表現パターン。

#### [NEW] [sheets.py](file:///c:/Users/hirak/Desktop/2nd-Brain/lib/sheets.py)

- Googleスプレッドシートからのデータ取得ロジックの共通化。

---

### 2. マンガ制作ツール (`18_システム`) の改善

#### [MODIFY] [manga_config.py](file:///c:/Users/hirak/Desktop/2nd-Brain/18_システム/manga_config.py)

- `lib/config.py` を使用するように修正し、絶対パスを排除。

#### [MODIFY] [manga_utils.py](file:///c:/Users/hirak/Desktop/2nd-Brain/18_システム/manga_utils.py)

- `lib/utils.py` の機能を利用し、コードを簡略化。
- モジュール内のコメントを日本語化。

#### [MODIFY] [smart_refactor.py](file:///c:/Users/hirak/Desktop/2nd-Brain/18_システム/smart_refactor.py)

- 新しい構成に合わせてインポート処理を整理。

---

### 3. ダイエット・ライフログツール (`scripts`, `_system_scripts`) の統合

#### [MODIFY] [sync_weight.py](file:///c:/Users/hirak/Desktop/2nd-Brain/18_システム/sync_weight.py)

- スプレッドシートからの取得と、Markdownの解析・アドバイス生成機能（`_system_scripts` 側の良さ）を統合。
- 重複する古いファイルを整理（削除はユーザー確認後に実施）。

#### [MODIFY] [auto_diet_screenshot.py](file:///c:/Users/hirak/Desktop/2nd-Brain/scripts/auto_diet_screenshot.py)

- 共通パス設定とログ機能を使用。

---

### 4. 文字化けの解消

#### [MODIFY] [verify_check.py](file:///c:/Users/hirak/Desktop/2nd-Brain/verify_check.py) 等

- ファイル内の日本語文字列が壊れているものをすべて修正。

## 検証計画

### 修正後の動作確認

以下の主要スクリプトを実行し、エラーなく完了し、期待通りに出力（Markdownの更新等）が行われることを確認します。

- `python 18_システム/smart_refactor.py --dry-run`: テンプレート適用が正しくシミュレーションされるか。
- `python 18_システム/sync_assets.py`: 資産データが正しく取得・更新されるか。
- `python 18_システム/sync_weight.py`: 体重データが取得・解析・追記されるか。

### 自動テスト（新規作成）

- `python tests/test_path_resolver.py`: ルートディレクトリの検知が正しく行われるかを確認する簡単なテスト。

---
> [!NOTE]
> 既存のスクリプトを削除する際は、必ず事前にバックアップの有無を確認し、ユーザーに同意を得てから行います。
