# モグラたたき (Whack-A-Mole)

> このファイルは Codex が作業時に参照するプロジェクトルールの入口です。
> 規約本体は別ファイル（Core_共通テンプレ.md）に集約しているため、本ファイルは短く保ちます。
> 検証用Unityプロジェクトに配置して使用してください。Codexで作業する場合の入口ファイルです。

---

## プロジェクト概要

- **ジャンル**: ミニゲーム / カジュアル
- **1行説明**: 9つの穴から出てくるモグラを60秒間で何匹叩けるかを競うミニゲーム
- **想定プラットフォーム**: スマホ縦持ち（941x1672 縦長UI想定）。PC横持ちでも遊べる構成
- **画面構成**: タイトル → インゲーム → リザルト → タイトル の3画面循環（同一シーン内のパネル切替）

---

## 設計規約（必須・最重要）

このプロジェクトのコード規約は以下のファイルに集約されています。
**機能を実装する前に必ず読んでください**:

- `Core_共通テンプレ.md`（プロジェクト配置時の想定パス）

ここに以下が書かれています:
- MVP（Logic / Presenter / View）構成と依存方向
- 4アセンブリ（Logic / Presenter / View / Tests.Editor）の物理分離ルール
- フォルダ構成と機能名サブフォルダの揃え方
- 自然言語依頼の自動配置・自動命名ルール
- `event Action<T>` 必須・クロージャ即席ラムダ禁止・`Dispose()` で `-=` 徹底
- コーディング規約（命名・ライフサイクル・非同期・null方針）
- 検証コマンド（uLoopMCP）
- 完成判定基準

**本ファイルではこれらを繰り返しません**。Core を読まずに実装した結果は不合格です。

---

## ゲーム固有仕様

詳細仕様（素材リスト・ゲームルール・推奨パラメータ・特殊View構成・演出構成）は以下を参照:

- `Spec.md`（プロジェクトルート直下、AGENTS.md と並べて配置）

このゲームの素材・ルール・特殊View構成・演出のイメージはすべて Spec.md にまとまっています。実装時は Core 規約とこの仕様書の両方を参照してください。

---

## このプロジェクトの環境設定

### 素材配置（既に配置済み・パス絶対固定）
- 画像（背景）: `Assets/Project/Images/Textures/`
  - `title_background.png`, `stage_background.png`
- 画像（モグラ・演出）: `Assets/Project/Images/Atlas/`
  - モグラ: `mole_idle.png`, `mole_appear.png`, `mole_hit.png`, `mole_escape.png`
  - 演出: `hit_particle_base.png`, `hit_particle_star_00〜04.png`, `hit_particle_slash_00〜03.png`
  - その他: `hammer_cursor.png`, `icon_score.png`, `icon_time.png`
  - ボタン: `btn_start.png`, `btn_retry.png`, `btn_title.png`（文字なし背景のみ）
- フォント: `Assets/Project/Fonts/NotoSansJP-Bold.ttf`（TMP_FontAsset は AI が生成する）

> ⚠️ Atlas/ と Textures/ の PNG は textureType=Default で取り込まれている可能性がある。
> Image / Sprite として使う前に Sprite (Single) に一括再インポートすること。

### レンダーパイプライン
- **URP**

### Input System
- **New Input System**（`activeInputHandler:1`）
- EventSystem には `UnityEngine.InputSystem.UI.InputSystemUIInputModule` を付ける

### 使用パッケージ
- UniTask（非同期処理・タイマー）
- DOTween Free（アニメーション、View層のみ）
- TextMeshPro（UI標準同梱）
- uLoopMCP（コンパイル / プレイモード制御 / テスト実行）
- NUnit + Unity Test Framework（EditMode テスト用）

### 音声
- **音は実装しない**（MVP範囲外）。AudioSource / AudioClip を一切登場させない

---

## ゲーム固有の追加規約

### 素材の扱い
- **タイトル画面のタイトル文字（"もぐらたたき" 等）は背景画像 `title_background.png` にすでに含まれている**。TMP テキストで重ねて描かないこと
- ボタン画像（`btn_start.png` 等）は文字なし。TMP で「START」「もう一度」等を重ねること
- **9個の穴の表示は MoleHoleView 内で2層構造で描く**（下層=常時表示の穴 idle、上層=モグラ本体）。`stage_background.png` には穴は描かれていないため

### カスタムボタン
- クラス名: `AppButton`（プロジェクト固有命名）
- 押下フィードバック・点滅API・SetSprite API を持つ
- 詳細は Spec.md と Core_共通テンプレ.md を参照

### TMP_FontAsset 生成
- `NotoSansJP-Bold.ttf` から SDF 形式の TMP_FontAsset を AI が生成する
- `atlasTexture` と `material` を `AddObjectToAsset` でサブアセット化すること（しないと Atlas が GC されてエラー）
- 推奨設定: AtlasPopulationMode=Dynamic, RenderMode=SDFAA, サンプリングサイズ=90, padding=9, atlas=1024x1024

### ParticleSystem（ヒット演出）
- URP用マテリアル: `Shader.Find("Universal Render Pipeline/Particles/Unlit")`
- 透明描画: `_Surface=1, _Blend=0, _SrcBlend=SrcAlpha, _DstBlend=OneMinusSrcAlpha, _ZWrite=0`、Keyword `_SURFACE_TYPE_TRANSPARENT` 有効化、`renderQueue=3000`
- UI上面描画: `ParticleSystemRenderer.sortingOrder = 100`
- `SetBurst(0, ...)` の前に `emission.burstCount = 1` を必ず設定（さもないと burst 無視警告）
- `TextureSheetAnimation` でスプライトを差す前に `while (tsa.spriteCount > 0) tsa.RemoveSprite(0);` でデフォルトを掃除

詳細仕様（素材リスト・ゲームルール・特殊View構成・演出のイメージ）は Spec.md を参照。

---

## 検証コマンド（uLoopMCP）

機能追加・変更後は必ず実行:

| 目的 | コマンド |
|------|---------|
| コンパイル確認 | `uloop compile --force-recompile true --wait-for-domain-reload true` |
| EditMode テスト実行 | `uloop run-tests --test-mode EditMode --filter-type assembly --filter-value MyGame.Tests.Editor` |
| プレイモード起動 | `uloop control-play-mode --action play` |
| ランタイムログ確認 | `uloop get-logs --log-type Error` |
| プレイモード終了 | `uloop control-play-mode --action stop` |
| スクショ確認 | `uloop screenshot --capture-mode rendering` |

---

## グローバル規約との関係

もしプロジェクト外にも共通の AGENTS.md や作業ルールを設定している場合、そこにも全プロジェクト共通のルールが定義されていることがあります。
グローバル規約と本プロジェクトの規約が衝突した場合、より厳しい方（多くの場合は Core_共通テンプレ.md）を優先してください。

---

## このファイルの保守

- パッケージバージョン・素材の追加削除があったら本ファイルを更新する
- 共通規約を変更したい場合は Core_共通テンプレ.md 側を編集する（こちらには共通規約を書かない）
- ゲームルール・素材リスト・特殊View構成・演出の詳細は Spec.md 側で管理する（本ファイルでは概要のみ）
