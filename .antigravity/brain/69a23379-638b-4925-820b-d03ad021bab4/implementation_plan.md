# Implementation Plan - Master Prompt Architect のワークフロー化

保存した高品質プロンプト `07_Master_Prompt_Architect.md` を、スラッシュコマンド（ワークフロー）として呼び出せるように設定します。

## 変更内容

### [.agent/workflows/](file:///c:/Users/hirak/Desktop/2nd-Brain/.agent/workflows/)

#### [NEW] [master-prompt-arch.md](file:///c:/Users/hirak/Desktop/2nd-Brain/.agent/workflows/master-prompt-arch.md)

このファイルを作成し、以下の手順を定義します：

1. `07_Master_Prompt_Architect.md` を読み込む。
2. ユーザーの要望が抽象的な場合は、ヒアリングを行う。
3. プロンプト内の「Workflow (Your Process)」に従い、最適化されたプロンプトを出力する。

## 検証計画

### 手動確認

- `/master-prompt-arch` コマンドでワークフローが起動し、正しいファイルが参照されるかを確認します。
