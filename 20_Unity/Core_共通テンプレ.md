# Core: 共通テンプレ
AI×Unity ゲーム開発の共通規約 - どのゲームを作っても同じフォルダ構成・規約・設計分離になる土台

> このテンプレは「AIに自然言語で機能を依頼しても、Logic / Presenter / View が分離されたコードになる」ことを目的にした規約集です。
> ワンショットで完成させる用途ではなく、**段階的に機能を積み上げる開発**を前提にしています。
> ゲーム固有の仕様（素材リスト・ゲームルール・シーン構成）は本ファイルには含めません。ゲームごとに `Spec.md` を別途用意して組み合わせてください（雛形は `Spec_template.md`）。

---

## 前提環境

- Unity（URP想定。Built-in でも本テンプレの規約自体は有効）
- 導入済みパッケージ:
  - **UniTask**（非同期処理・タイマー）
  - **DOTween**（アニメーション。View層でのみ使用）
  - **uLoopMCP**（コンパイル / プレイモード制御 / テスト実行 / ログ取得）
- ゲーム素材: `Assets/Project/Images/` `Assets/Project/Fonts/` 配下に配置済み（具体的な内容はゲームごと）

## 使い方

1. 新規Unityプロジェクト（または既存プロジェクト）に対し、本ファイルをAIに投入
2. 「以降この規約で実装してください」と指示
3. 機能追加の依頼は **自然言語**で渡す（例:「スコアを加算する仕組みを作って」）
4. AI は本テンプレの「自動配置・自動命名ルール」に従って配置・命名・実装する
5. 機能追加のたびに `uloop compile` `uloop run-tests` で検証

---

## 設計方針: MVP（Model-View-Presenter）パッシブビュー（最重要）

このテンプレは **MVP のパッシブビュー** を採用します。これに反する実装は不合格です。

### 3層の責務

| 層 | 形態 | 責務 |
|---|------|------|
| **Logic（Model）** | Pure C# | 状態保持・計算・タイマー・乱択など。表示を一切知らない。状態変化を `event` で発火するだけ |
| **Presenter** | Pure C# | Logic と View を仲介する **オーケストレーション**。View のイベントを購読 → Logic を呼ぶ / Logic の event を購読 → View に表示命令を出す |
| **View** | MonoBehaviour | 表示と入力検出のみ。**Logic も Presenter も知らない**。入力は `event` で発火、表示は public メソッドで命令を受ける |

### 依存方向（一直線、循環なし）

```
Logic ←──── Presenter ────→ View
                ↑
              App ──→ Logic / Presenter / View 全部参照（配線役）
```

- Logic は **何も知らない**（純粋）
- Presenter は **Logic と View 両方を参照**（仲介役）
- View は **Logic も Presenter も知らない**（純粋に表示と入力）
- App（GameLauncher）は **全部知る**（配線役）

### なぜ MVP パッシブビューか

- View が Logic を直接いじらないので、ロジックが View 側に漏れない
- View は「イベント発火＋表示命令受信」だけの薄いクラスになり、Unity 依存を局所化できる
- Logic は Pure C# でテスト可能
- Presenter はオーケストレーション役で、ロジックを持たないため **テスト対象外**（Too much なので書かない）

### View のルール（厳格）

View はやっていいことが2つだけ:

1. **入力を `event` で発火**（例: `event Action<int> OnHoleHit;`）
2. **public メソッドで表示命令を受ける**（例: `void SetScore(int score)`, `void ShowGameOver()`）

やってはいけないこと:
- Logic / Presenter のクラスを参照する（asmdef で物理的に弾く）
- ゲームのルール判定・スコア計算・タイマーを持つ
- 自分で状態を保持する（表示用の一時バッファを除く）

### Presenter のルール

- 機能ごとに1個（例: `ScorePresenter`, `MoleSpawnPresenter`）
- **Pure C#（MonoBehaviour禁止）**
- 持つもの: Logic への参照 + View への参照（具象クラスでよい）
- やること:
  - View のイベントを **メソッドグループ**で購読 → Logic のメソッドを呼ぶ
  - Logic の event を **メソッドグループ**で購読 → View に表示命令を出す
- `IDisposable` を実装し、`Dispose()` で全ての購読を `-=` 解除する
- ロジック計算（スコア計算・タイマー判定など）は **絶対に書かない**。Presenter にロジックを書きたくなったら、その処理は Logic 側に置く

### Logic のルール

- **Pure C#**、`MonoBehaviour` 継承禁止、Unity 表示系型への直接依存禁止
- 状態変化は `event Action<T>` で通知する（`public event Action<int> OnScoreChanged;`）
- 禁止する using / 型: `UnityEngine.MonoBehaviour`, `Transform`, `GameObject`, `Component`, `UnityEngine.UI.*`, `UnityEngine.EventSystems.*`, `UnityEngine.ParticleSystem`, `TMPro.*`, `DG.Tweening.*`
- 許可する using / 型: `System.*`, `Cysharp.Threading.Tasks` (UniTask), `UnityEngine.Vector3` / `Vector2` / `Mathf` / `Time` / `Random` などの数学・時間ユーティリティ

#### Pure C# の定義（このテンプレでの解釈）

理想は「UnityEngine 一切非依存の Logic」（別プロジェクトでも動く真の Pure C#）だが、Unity ゲーム開発の現実を踏まえ、本テンプレでは **「View 表示系に依存しないこと」** を Pure C# の実用的定義としている。

- **禁止（厳格）**: MonoBehaviour / UI / TMP / DOTween / EventSystems / ParticleSystem などの **View 表示系**
- **許可（実用判断）**: `System.*`, `UniTask`（非同期処理）, UnityEngine の数学・時間ユーティリティ（`Vector3`, `Mathf`, `Time`, `Random` 等）

UniTask は厳密には UnityEngine 依存だが、View 表示系ではなく、EditMode テストで `UnityTest + UniTask.ToCoroutine` により極小タイミング検証ができる。Logic の非同期処理生産性のために許可している。

> **将来、設計純度を上げたい場合**: Logic から UniTask を外し、時間制御を Presenter 側で担う設計に移行できる。その場合 Logic は同期メソッドのみになり、Presenter が UniTask でフレームループを回す。本テンプレはスターターキット向けに実用優先で UniTask を許容しているが、設計純度を売りにする商品では再検討する余地あり。

### Composition Root（`App/GameLauncher.cs`）

- MonoBehaviour、**配線のみ**
- Logic を `new` し、View をシリアライズ参照で集めて、Presenter に両方を渡して組み立てる
- **GameLauncher 自体にスコア計算・タイマー・乱択などのロジックを書かない**
- ブートストラップは `[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]` で `Initialize()` を呼ぶ静的メソッド（これだけが唯一の Unity ライフサイクル例外）
- `Initialize()` 先頭で `Application.runInBackground = true` を設定（エディタ非フォーカス時のフレーム停止事故防止）
- 終了時は Presenter の `Dispose()` を呼ぶ責任を持つ（OnDestroy で）

### 設計理由コメント（必須）

各 `.cs` ファイルの先頭に **設計理由コメント**を必ず書く（XMLドキュメントとは別）。

書く内容:
- 層（Logic / Presenter / View / Composition Root / Editor）
- なぜこの層に置いたか（1〜2文）
- 主要な責務（箇条書き2〜4個）
- View 層の場合: 依存している Unity API（Image, ParticleSystem, DOTween 等）を列挙

例:
```csharp
// ===== 設計理由 =====
// 層: Presenter (Pure C#)
// 理由: ScoreLogic の状態変化を ScoreView に反映する仲介役。ロジックを持たず、購読と命令のみ。
// 責務:
//   - ScoreLogic.OnScoreChanged を購読 → view.SetScore() で表示更新
//   - 加点要求イベントを Logic に転送（必要なら）
// =====================
```

### DESIGN_NOTES.md（必須・追記更新）

`Assets/Project/Docs/DESIGN_NOTES.md` を生成し、以下を書く:

- Logic / Presenter / View / Composition Root の役割分担
- asmdef 4分割の意図と効果
- 機能追加のたびに「どのクラスを Logic / Presenter / View のどこに置いたか」「なぜそこに置いたか」を追記

---

## 共通フォルダ構成

**設計指針**: Prefab・Material・Sprite参照などのアセットは関連する `View` クラスと **同じフォルダに同居**させる（探索性の確保）。
Logic / Presenter は Pure C# のみなのでスクリプトだけまとめる。

```
Assets/Project/
├── Logic/                              ← MyGame.Logic.asmdef (Pure C#, ref: UniTask)
│   └── {機能名}/
│       ├── XxxLogic.cs                 ← Model: 状態保持 + event 発火
│       └── XxxConfig.cs                ← 設定値・データ構造
│
├── Presenter/                          ← MyGame.Presenter.asmdef (Pure C#, ref: Logic, View, UniTask)
│   └── {機能名}/
│       └── XxxPresenter.cs             ← Logic と View を仲介
│
├── View/                               ← MyGame.View.asmdef (ref: UniTask, UI/TMP/DOTween)
│   └── {機能名}/
│       ├── XxxView.cs                  ← MonoBehaviour: イベント発火 + 表示命令受信
│       ├── XxxView.prefab              ← Prefab を View クラスと同居
│       └── XxxView.mat                 ← Material（必要なら）
│
├── App/                                ← Composition Root
│   └── GameLauncher.cs                 ← Logic / Presenter / View を組み立てる
│
├── Editor/                             ← エディタ拡張
│
├── Tests/
│   └── Editor/                         ← MyGame.Tests.Editor.asmdef (ref: Logic, UniTask)
│       └── XxxLogicTests.cs            ← Logic だけテスト。Presenter / View はテスト対象外
│
├── Scenes/                             ← シーンファイル
├── Images/                             ← 共通素材（特定機能に紐付かないもの）
├── Fonts/                              ← フォント
└── Docs/
    └── DESIGN_NOTES.md                 ← 設計判断のドキュメント（自動生成・追記更新）
```

### アセンブリ参照関係

| アセンブリ | 配置 | 参照可能な相手 |
|-----------|------|---------------|
| `MyGame.Logic` | `Assets/Project/Logic/MyGame.Logic.asmdef` | `UniTask` のみ |
| `MyGame.View` | `Assets/Project/View/MyGame.View.asmdef` | `UniTask`, UI/TMP/DOTween/EventSystems 等 Unity 表示系 |
| `MyGame.Presenter` | `Assets/Project/Presenter/MyGame.Presenter.asmdef` | `MyGame.Logic`, `MyGame.View`, `UniTask` |
| App (GameLauncher) | `Assets/Project/App/`（asmdef 任意） | Logic / Presenter / View |
| `MyGame.Tests.Editor` | `Assets/Project/Tests/Editor/MyGame.Tests.Editor.asmdef` | `MyGame.Logic`, `UniTask` |

**重要**:
- Logic は **View も Presenter も知らない**（references が UniTask のみ）
- View は **Logic も Presenter も知らない**（references に Logic も Presenter も入れない）
- Presenter だけが両側を知る

> 「Prefab はスクリプトと同じ階層に置きたい」要望に対する解: View 層を機能単位フォルダにして View クラスと Prefab を同居させる。Logic / Presenter は Pure C# だけなのでスクリプト単位でまとめる。

### 機能名サブフォルダの揃え方

Logic / Presenter / View は **同じ機能名サブフォルダを使う**:

```
Logic/Score/ScoreLogic.cs
Presenter/Score/ScorePresenter.cs
View/Score/ScoreView.cs + ScoreView.prefab
```

これにより「あるゲーム機能の Logic / Presenter / View が一目で対応づく」。

---

## 自然言語依頼の自動配置・自動命名ルール（最重要）

依頼は **「やりたいこと」を自然言語**で来ます（例:「スコアを加算する仕組みを作って」）。
ファイル名・クラス名・パス・asmdef名・名前空間は **指示されません**。
AI は以下のルールに従って **自動で決定**してください。

### 配置先マッピング（層判定）

依頼内容から **機能名（英語）** を決め、その機能名のサブフォルダに配置する。

| 依頼の性質 | 配置先 | 形態 |
|-----------|--------|------|
| ゲームのルール / 状態管理 / タイマー / スコア計算 / スポーン制御 | `Assets/Project/Logic/{機能名}/` | Pure C# (`〇〇Logic`) |
| データ構造 / 設定値 | `Assets/Project/Logic/{機能名}/` | Pure C# (`〇〇Config` 等) |
| Logic と View の仲介役 | `Assets/Project/Presenter/{機能名}/` | Pure C# (`〇〇Presenter`) |
| 画面表示 / 入力受付 / ボタン / アニメ / パーティクル | `Assets/Project/View/{機能名}/` | MonoBehaviour (`〇〇View`) |
| Prefab / Material / View 専用素材 | `Assets/Project/View/{機能名}/` | アセット（View クラスと同居） |
| 全体配線 / Logic と View を繋ぐ | `Assets/Project/App/` | MonoBehaviour（Composition Root） |
| エディタ拡張 / メニュー追加 | `Assets/Project/Editor/` | エディタコード |
| Logic のテスト | `Assets/Project/Tests/Editor/` | NUnit テスト |

### クラス名命名ルール

依頼内容から **機能を表す英語名**を自動命名:

| 機能 | 命名規則 | 例 |
|------|---------|-----|
| 設定値の保持 | `〇〇Config` | `GameConfig`, `PlayerConfig` |
| ゲーム本体ロジック | `〇〇Logic` | `ScoreLogic`, `TimerLogic`, `MoleSpawnLogic` |
| 仲介役 | `〇〇Presenter` | `ScorePresenter`, `TimerPresenter` |
| View 実装 | `〇〇View` | `ScoreView`, `TimerView` |
| カスタムボタン | プロジェクト独自命名 | `AppButton` |
| 全体配線 | `GameLauncher` | `GameLauncher` |
| エディタ拡張 | `〇〇Menu` 等 | `BuildSceneMenu` |

### 名前空間ルール

- Logic 層: `MyGame.Logic`（プロジェクト固有なら `{ProjectName}.Logic`）
- Presenter 層: `MyGame.Presenter`
- View 層: 名前空間なし、または `MyGame.View`
- Composition Root: 名前空間なし
- Editor: `MyGame.Editor`、または名前空間なし
- Tests: `MyGame.Tests.Editor`

### asmdef 自動作成ルール

各層に最初のコードを置く時、対応する asmdef がなければ自動作成:

| asmdef ファイル | 配置先 | references | 補足 |
|----------------|-------|-----------|------|
| `MyGame.Logic.asmdef` | `Assets/Project/Logic/` | `UniTask` のみ | Pure C# 物理分離 |
| `MyGame.Presenter.asmdef` | `Assets/Project/Presenter/` | `MyGame.Logic`, `MyGame.View`, `UniTask` | 仲介役 |
| `MyGame.View.asmdef` | `Assets/Project/View/` | `UniTask`（必要に応じて UI/TMP/DOTween 関連を追加） | Logic も Presenter も参照しない |
| `MyGame.Tests.Editor.asmdef` | `Assets/Project/Tests/Editor/` | `MyGame.Logic`, `UniTask` | EditMode テスト用 |

`MyGame.Tests.Editor.asmdef` の追加設定:
- `includePlatforms`: Editor
- `overrideReferences`: true
- `precompiledReferences`: `nunit.framework.dll`
- `defineConstraints`: `UNITY_INCLUDE_TESTS`

### 依頼が曖昧な場合

仕様が不明確な箇所は **AIが合理的なデフォルトで決めて先に進める**こと。
最後にまとめて「決めた前提」を申告してください。

---

## event ベース通知ルール（重要）

Logic → Presenter の通知、および View → Presenter の入力通知はすべて **`event Action<T>`** で行う。
オオバの本テンプレでは **R3 / ReactiveProperty は使わない**（最小依存の原則）。差し替えたい場合は Logic の状態を `ReactiveProperty<T>` に置き換えるだけで Presenter 側の構造は変わらない。

### event を必ず付けるルール

```csharp
// Logic
public event Action<int> OnScoreChanged;  // ← event を必ず付ける
```

`event` を付けることで:
- 外部から `OnScoreChanged = null` で全削除する事故を防げる
- 外部から `OnScoreChanged?.Invoke(...)` で偽発火する事故を防げる
- 「Logic = 発火元 / 外部 = 購読側」という責務を **構造的に固定**できる

### クロージャ（即席ラムダ）禁止

即席ラムダで `+=` すると **解除不能**になりリークする:

```csharp
// ✗ 禁止: 即席ラムダ
logic.OnScoreChanged += s => view.SetScore(s);
logic.OnScoreChanged -= s => view.SetScore(s);  // 別インスタンスなので解除されない
```

### 安全な購読パターン

#### A. メソッドグループ（推奨）

```csharp
public class ScorePresenter : IDisposable
{
    private readonly ScoreLogic _logic;
    private readonly ScoreView _view;

    public ScorePresenter(ScoreLogic logic, ScoreView view)
    {
        _logic = logic;
        _view = view;
    }

    public void Initialize()
    {
        _logic.OnScoreChanged += HandleScoreChanged;
        _view.OnAddRequest += HandleAddRequest;
    }

    public void Dispose()
    {
        _logic.OnScoreChanged -= HandleScoreChanged;
        _view.OnAddRequest -= HandleAddRequest;
    }

    private void HandleScoreChanged(int newScore) => _view.SetScore(newScore);
    private void HandleAddRequest(int delta) => _logic.Add(delta);
}
```

#### B. ラムダをフィールド保持（メソッドグループに収まらない場合のみ）

```csharp
private Action<int> _scoreChangedHandler;

public void Initialize()
{
    _scoreChangedHandler = s => _view.SetScore(s * 2);  // ラムダで加工が必要な時など
    _logic.OnScoreChanged += _scoreChangedHandler;
}

public void Dispose()
{
    _logic.OnScoreChanged -= _scoreChangedHandler;
}
```

### 購読解除の徹底ルール

- **Presenter は `IDisposable` を実装し、`Dispose()` で購読した全 event を `-=` 解除**
- GameLauncher は子の Presenter / View の `Dispose()` をライフサイクル終了時（`OnDestroy`）に必ず呼ぶ
- Logic 自身も `Dispose()` で自分の event を null クリアして二重保険にしてよい:
  ```csharp
  public void Dispose() {
      OnScoreChanged = null;  // クラス内部からは event でも = 代入可
  }
  ```

---

## コーディング規約

### 基本方針

- **既存設計に合わせる**（勝手に思想を変えない）
- 不明点は必ず確認する（推測で進めない）
- **1クラス1責務**を徹底する
- **300行を超えたら分割を検討**する
- 関数の肥大化禁止。長くなってきたら分割を検討
- 可読性を優先し、クラス・関数・変数の名前を **省略しすぎない**（`mgr` より `manager`、`btn` より `button`）

### 命名規則

| 種別 | 規則 | 例 |
|------|------|----|
| 定数 / static readonly | PascalCase | `public const int MaxCount = 10;` |
| ローカル変数 | lowerCamelCase | `int hoge;` |
| public 変数 | lowerCamelCase | `public int hoge;` |
| private / protected 変数 | `_` + lowerCamelCase | `private int _hoge;` |
| public / protected / private 関数 | PascalCase | `public void Hoge() {}` |
| ローカル関数（メソッド内定義） | `_` + PascalCase | `void _Hoge() {}` |
| bool | `is` / `has` / `can` プレフィックス | `bool isReady;` |
| プロパティ | PascalCase | `int Id { get; }` |
| Action / event | `On` + PascalCase | `public event Action<int> OnScoreChanged;` |

> **注意**: 「ローカル関数」はC#のローカル関数構文（メソッド内に定義する関数）を指す。
> クラスの private メソッドは PascalCase（`_`なし）。混同しないこと。
>
> ```c#
> // private メソッド → PascalCase（_なし）
> private void DoSomething() {}
> 
> // ローカル関数（メソッド内定義）→ _PascalCase
> public void Execute()
> {
>  void _ValidateInput() {}  // ← これがローカル関数
> }
> ```
>
> 

### Unity ライフサイクル禁止

- `Awake` / `Start` / `OnEnable` / `OnDisable` は **使用禁止**
- `Update` の使用も控える（必要なら Updater に登録する形）
- 初期化は `Initialize()` 系メソッドを明示的に定義し、呼び出し元（GameLauncher）から実行する
- 解放処理は `Dispose()` を親側から呼ぶ
- `OnDestroy` は許可（GameLauncher が子の `Dispose()` を呼ぶため、DOTween Kill のため）
- 例外: `GameLauncher` のみ `[RuntimeInitializeOnLoadMethod(AfterSceneLoad)]` でブート

### シリアライズ

- `[SerializeField] private` を使用。`public` フィールドのシリアライズは禁止

### 非同期処理

- UniTask を使用。`async void` 禁止
- `CancellationToken` を必ず引数で受ける
- await しない UniTask は `.Forget()` を付ける
- DOTween で await しない Tween は変数で受ける（または `_ = transform.DOMoveX(...)` で破棄抑制）。すべての Tween は `OnDestroy` で `Kill()` する
- `Tween.ToUniTask()` は `UniTask.DOTween` asmdef ブリッジ未設定なら使えない。代わりに `UniTask.Delay(TimeSpan.FromSeconds(d), cancellationToken: ct)` で待機

### nullチェック方針

- **nullが不正な状態（設定漏れ・初期化忘れ等）の場合、nullチェックで握りつぶさない**
- 早期リターンで黙殺するとエラーが検知できず原因不明のバグになる
- そのまま実行して `NullReferenceException` を出して即検知する
- nullチェックが適切なケース:「nullが正当な値」として設計上許容されている場合のみ

### コメント

- クラスと public 関数には XML ドキュメントコメント（`/// <summary>`）必須
- 変数・プロパティは1行形式: `/// <summary>キャラID</summary>`
- 加えて、各 `.cs` ファイル冒頭に **設計理由コメント**（前述）

### Unity標準コンポーネント禁止

- **`UnityEngine.UI.Button` は使用禁止**
- ボタンは必ずプロジェクト独自のカスタムボタンクラス（例: `AppButton`）を使用する
- 理由: 押下フィードバック・状態管理を独自実装で揃えるため
- カスタムボタンの実装内容（点滅・拡縮アニメ等）はゲームごとに異なるので `Spec.md` 側で定義する

### UI要素・Sprite の視覚的配置（視覚的境界・中心・サイズ感の優先）

UI要素や Sprite を配置する際は、`RectTransform` の機械的中央や端、画像ファイルの矩形を盲信せず、**素材の視覚的な境界・中心・サイズ感**を確認して配置する。

#### 3つの視覚的整合性

##### 1. 視覚的境界（意味領域に収める）

背景画像内に「意味のある領域」（土エリア・パネル領域・舞台等）がある場合、子要素は **その意味領域内に収まる**よう配置する。背景画像全体の矩形ではなく、**意味のある領域の境界**を基準にする。

> 例: 背景画像が縦長で、中央に茶色い土エリアが描かれている場合、ゲームオブジェクトは土エリア内に配置する。緑の草地部分にはみ出さない。

##### 2. 視覚的中心（中心を合わせる）

2層構造（背景画像の上にキャラを重ねる、ボタン画像の上にラベルを置く等）の場合、上層の中心が **下層画像の視覚的中心**に重なるように調整する。

- ボタン画像にドロップシャドウや上下左右非対称な余白がある場合、TMP ラベルを `anchoredPosition = (0, 0)` で済ませると視覚的中央から下にずれることが多い
- 必要に応じて Y 方向に数px〜10px 程度上にオフセットする
- Sprite の Pivot 設定や RectTransform anchor も画像の見た目の中心に合わせる
- 画像ファイルの矩形中心と視覚的中心がずれている場合は **視覚的中心を優先**する

##### 3. 常識的サイズ感（周辺と揃える）

演出（パーティクル・エフェクト・Tween スケール）や UI 要素のサイズは、**周辺要素のサイズ感に揃える**。

- 特定要素1個分を大きく超えない
- 画面いっぱいに広がるような派手すぎる演出は避ける
- AI は「派手な演出」と「常識的な演出」の判別ができないため、Spec.md 側で具体的なサイズ基準を示す

#### 確認手順（必須）

- AI は画像認識で「意味領域」「視覚的中心」「常識サイズ」を自動判定できない
- ゲーム固有の具体的な境界・中心・サイズ感は **Spec.md 側で明示**すること
- 本規約は「視覚的整合性を考慮する思想」を示すもの
- 実装後は **Game ビューで目視確認**してから完了報告すること

### カメラ設定（2D / UI 主体のゲーム）

2D / UI 主体のゲームでは、Main Camera の背景設定を以下にすること:

- `clearFlags = SolidColor`（**Unity デフォルトの SkyBox は使わない**）
- `backgroundColor` = 黒、または背景画像に合う色（背景画像が画面いっぱいでない場合に隙間として見える色）

理由: Unity デフォルトの SkyBox は3D空間のための装飾であり、2Dゲームでは「画面の隙間に青空が見える」など意図しない見た目になる。リザルト画面など背景画像が無いシーンでは特に違和感が出る。

3D ゲームの場合のみ、必要に応じて SkyBox を使う。

---

## EditMode テスト

- 配置: `Assets/Project/Tests/Editor/<Feature>LogicTests.cs`
- asmdef: `MyGame.Tests.Editor.asmdef`（前述「asmdef 自動作成ルール」参照）
- テスト関数名は **日本語+連番**（例: `T1_スタミナ減少テスト`, `T2_満タンを超えない`）
- **Logic 層のみテスト対象**。Presenter / View はテスト対象外（Presenter はオーケストレーション役でテスト価値が薄い、View は MonoBehaviour で重い）
- Logic 層の機能を追加したら **テストを必ず書く**

---

## 検証コマンド（uLoopMCP）

機能追加・変更後は以下を必ず実行して検証する:

| 目的 | コマンド |
|------|---------|
| コンパイル確認 | `uloop compile --force-recompile true --wait-for-domain-reload true` |
| EditMode テスト実行 | `uloop run-tests --test-mode EditMode --filter-type assembly --filter-value MyGame.Tests.Editor` |
| プレイモード起動 | `uloop control-play-mode --action play` |
| ランタイムログ確認 | `uloop get-logs --log-type Error` |
| プレイモード終了 | `uloop control-play-mode --action stop` |

### 実コマンド実行ルール（最重要・絶対遵守）

**「コンパイル確認します」「テスト走らせます」「プレイで動作確認します」と言うだけで、実際にコマンドを実行しないことを禁止する。**

過去にAIが規約破りを起こした典型パターン:
- 「コンパイル確認しました」と言いながら実は実行していない
- 「テストは想定通り通ると思います」とコマンド未実行のまま完了報告
- 「プレイモードで動作確認できます」と言うだけで起動していない

これを防ぐため、以下を **絶対に守る**:

1. 上表のコマンドは **必ず Bash ツールで実コマンドとして実行**する（言葉で「実行する」と書くだけは NG）
2. 実行後、**標準出力・エラー件数を最後まで読み**、エラー件数・警告件数・テスト件数を **数字で申告**する
3. 出力に異常があれば修正してから次の操作に進む
4. **未実行のまま「想定通り動く」「動きました」と報告することは禁止**
5. 「コンパイル待機が効かなかったかも」と感じたら、もう一度 `uloop compile --force-recompile true --wait-for-domain-reload true` を **再実行**する。AIが内部で待機を省略しないよう、毎回明示的に再実行する

完了報告には必ず以下のフォーマットを含めること:

```
- uloop compile: 0 error / 0 warning（実行済み）
- uloop run-tests: <X件> Pass / <Y件> Fail（実行済み）
- uloop control-play-mode + uloop get-logs --log-type Error: 0 件（実行済み）
```

**実行していない項目があれば、未実行であることを明示**（嘘を書かない）。

### .meta ファイル運用

- C#ファイルを新規作成・自動生成した場合、コミット前に必ず以下を行う:
  1. `uloop compile --force-recompile true --wait-for-domain-reload true` でコンパイル
  2. `.meta` ファイルが生成されたことを `git status` で確認
  3. `.cs` と `.meta` を一緒にコミットする
- `.meta` なしでコミットすると Unity 側で GUID 参照が壊れる

### コード変更後の検証フロー

コード編集・マージ・コンフリクト解消後は、以下を必ずセットで実行:

1. `uloop compile` でコンパイルエラーがないことを確認
2. `uloop control-play-mode --action play` でプレイモードに入る
3. `uloop get-logs --log-type Error` でランタイムエラーがないことを確認
4. プレイモードを終了

> コンパイルは通るがランタイムで落ちるケース（SerializeField 未アサイン等）を検知するため。

---

## 既知の汎用 Tips

### New Input System
- 本テンプレ前提: New Input System 使用（`activeInputHandler:1`）
- EventSystem には `StandaloneInputModule` ではなく `UnityEngine.InputSystem.UI.InputSystemUIInputModule` を付ける

### TMP テキスト改行モード
- `TMP_Text.enableWordWrapping` は obsolete
- `textWrappingMode = TextWrappingModes.NoWrap` を使う

### URP使用時のParticleSystemマテリアル（必要なら）
- `Shader.Find("Universal Render Pipeline/Particles/Unlit")` でマテリアル作成
- 透明描画する場合: `_Surface=1` (transparent) / `_Blend=0` (alpha) / `_SrcBlend=SrcAlpha` / `_DstBlend=OneMinusSrcAlpha` / `_ZWrite=0`、Keyword `_SURFACE_TYPE_TRANSPARENT` を有効化、`renderQueue=3000`
- UI上面に描画したい場合: `ParticleSystemRenderer.sortingOrder = 100` 程度

---

## 段階的開発の進め方

このテンプレは **段階的開発**を前提にしています。一度にすべて実装する必要はありません。

### 推奨フロー

1. **規約投入**: このCoreファイルをAIに投入し、「以降この規約で実装してください」と指示
2. **Composition Root 雛形**: `GameLauncher.cs` を最初に作る（中身は空でいい）
3. **Logic から作る**: 機能を1つずつ Logic 層から実装し、`event` で状態通知。テストを書く
4. **Presenter を作る**: Logic と View を仲介する Presenter を実装。`IDisposable` で `Dispose()` 必須
5. **View を作る**: 表示と入力イベントだけの薄い MonoBehaviour を実装
6. **GameLauncher で配線**: Logic を `new`、View を SerializeField で参照、Presenter に両方を渡して `Initialize()`
7. **検証**: `uloop compile` → `uloop run-tests` → `uloop control-play-mode` で動作確認
8. **DESIGN_NOTES.md 追記**: 各機能追加時に「どのクラスをどの層に置いたか・なぜ」を追記

### 機能追加のたびに守ること

- Logic に MonoBehaviour・UnityEngine.UI 等が混入していないか確認（asmdef で物理的に弾かれているはず）
- View が Logic / Presenter を参照していないか確認（asmdef で物理的に弾かれているはず）
- Presenter が `IDisposable` を実装し `Dispose()` で全購読を `-=` 解除しているか確認
- GameLauncher が OnDestroy で Presenter の `Dispose()` を呼んでいるか確認
- Logic 機能のテストが追加されているか確認
- 設計理由コメントが書かれているか確認
- DESIGN_NOTES.md が追記更新されているか確認

---

## 完成判定基準（共通枠）

機能追加・変更のたびに以下を満たすこと。満たさない箇所があれば最後に正直に申告すること。

### 構造チェック
- [ ] コンパイルが通る (`uloop compile` で 0 error / 0 warning)
- [ ] EditMode テストが全件 Pass する
- [ ] プレイモードでランタイムエラーが出ない
- [ ] **`MyGame.Logic.asmdef` の references が `UniTask` のみ**（UI/TMP/DOTween/View/Presenter に物理的にアクセスできない）
- [ ] **`MyGame.View.asmdef` の references に `MyGame.Logic` / `MyGame.Presenter` が含まれていない**（View は Logic も Presenter も知らない）
- [ ] **`MyGame.Presenter.asmdef` の references が `MyGame.Logic`, `MyGame.View`, `UniTask`**

### コード規約チェック
- [ ] **Logic 配下の全クラスが MonoBehaviour を継承していない**
- [ ] **Logic 配下のファイルに `using UnityEngine.UI;` / `using TMPro;` / `using DG.Tweening;` / `using UnityEngine.EventSystems;` が含まれていない**
- [ ] **Presenter 配下の全クラスが MonoBehaviour を継承していない**（Pure C#）
- [ ] **View 配下の全クラスが Logic / Presenter のクラスを参照していない**
- [ ] **GameLauncher.cs にロジック計算（タイマー・スコア・乱択など）が書かれていない**（`new` と参照配線と Initialize/Dispose 呼び出しのみ）
- [ ] Awake/Start/OnEnable/OnDisable に処理を書いていない（`Initialize()` 経由、ブートのみ `[RuntimeInitializeOnLoadMethod]`）
- [ ] private 変数が `_` + lowerCamelCase になっている
- [ ] async void がない / `CancellationToken` が UniTask メソッドに渡っている
- [ ] `UnityEngine.UI.Button` を使っていない（カスタムボタンクラス使用）
- [ ] DOTween Tween が `OnDestroy` で Kill されている
- [ ] **ボタンラベルが画像の視覚的中心に配置されている**（ドロップシャドウ等を考慮した位置調整）
- [ ] **子要素が背景画像の意味領域からはみ出していない**（土エリア・パネル領域等の境界内に収まっている）
- [ ] **2層構造の上層が下層の視覚的中心に重なっている**（モグラと穴・キャラと足場等）
- [ ] **演出のサイズが周辺要素に対して常識的範囲**（画面いっぱいに広がる派手すぎる演出になっていない）
- [ ] **2D / UI 主体のゲームで Main Camera が SkyBox を使っていない**（`clearFlags = SolidColor`）
- [ ] **開発中の動作確認用UI（テストボタン・デバッグテキスト等）が最終ビルドに残っていない**（必要だった場合も Step 8 仕上げで削除する）

### イベント購読チェック
- [ ] **Logic の状態通知フィールドはすべて `event Action<T>` で公開されている**（生の `Action` 直書き禁止）
- [ ] **Presenter で `+=` した event は全て `Dispose()` で `-=` 解除されている**
- [ ] **即席ラムダで `+=` していない**（メソッドグループまたは保持済みラムダのみ）
- [ ] **Presenter は `IDisposable` を実装している**
- [ ] **GameLauncher が OnDestroy で Presenter の Dispose() を呼んでいる**

### ドキュメントチェック
- [ ] **各 `.cs` ファイル冒頭に「設計理由コメント」が書かれている**
- [ ] **`Assets/Project/Docs/DESIGN_NOTES.md` が追記更新されている**

> ゲーム固有の完成判定基準は `Spec.md` 側で追加すること

---

## このファイルの位置づけ

- 本ファイルは **どのUnityゲーム開発でも変えずに使える共通規約** です
- ゲーム固有の仕様（素材リスト・ゲームルール・シーン構成・カスタムボタンの具体実装など）は **`Spec.md`**（`Spec_template.md` をコピーして埋める）で管理してください
- 段階的に機能を追加していく前提なので、ワンショット完成プロンプトとは性質が異なります（ワンショット用途には別途プロンプト集を組み合わせること）
