# Unified Shortcut Consolidation Plan

作業効率を最大化するため、すべての主要アクション（同期・リファクタリング・コミット）をショートカット「5」に集約し、他の冗長なショートカットを削除します。

## Proposed Changes

### [Component] 自動化・同期システム

#### [MODIFY] [commit_all.ps1](file:///c:/Users/hirak/Desktop/2nd-Brain/scripts/commit_all.ps1)

- 同期処理の後に `smart_refactor.py` を実行するロジックを追加します。
- これにより、「データ同期 -> プロンプト等のリファクタリング -> Gitコミット & Drive保存」が一連の流れとして実行されます。

#### [MODIFY] [GEMINI.md](file:///c:/Users/hirak/Desktop/2nd-Brain/GEMINI.md)

- ショートカットリストを「5」のみに整理します。
- 「5: 全部入り (Sync, Refactor, Commit)」のような分かりやすい表記に変更します。

## Verification Plan

### Automated Tests

- `scripts/commit_all.ps1` を実行し、以下の順序で処理が行われることを確認します：
  1. `sync_assets.py` (資産同期)
  2. `sync_weight.py` (体重同期)
  3. `smart_refactor.py` (リファクタリング)
  4. `git commit` & `push`

### Manual Verification

- `GEMINI.md` の表示がシンプルになり、ショートカット 5 だけで完結することを確認します。
