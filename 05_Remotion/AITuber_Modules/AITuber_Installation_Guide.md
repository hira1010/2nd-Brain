# AITuber Kit モジュール導入ガイド

作成したモジュールをUnityプロジェクトに導入する手順です。

## ファイル構成

以下の4つのスクリプトをUnityプロジェクトの `Assets/Scripts` などの任意のフォルダにコピーしてください。

1. `AITuberManager.cs`
2. `AIAvatarController.cs`
3. `LLMService.cs`
4. `MemoryDatabase.cs`

## セットアップ手順

### 1. マネージャーの配置

1. Unityのシーン上に空のGameObjectを作成し、名前を `AITuberSystem` などにします。
2. このオブジェクトに `AITuberManager` コンポーネントをアタッチします。
    * **Note**: `MemoryDatabase`, `LLMService` は `AITuberManager` が自動的に追加しますが、個別の設定を行いたい場合は手動でアタッチしても構いません。

### 2. アバターの作成 (PNGTuber)

1. Canvasを作成します（既に存在する場合はその中へ）。
2. Canvas内に `Image` オブジェクトを作成し、キャラクターの立ち絵を表示させます。
3. このImageオブジェクトに `AIAvatarController` コンポーネントをアタッチします。
4. Inspectorで以下の設定を行います：
    * **Avatar Image**: Imageコンポーネント自身をドラッグ＆ドロップ。
    * **Idle Sprite**: 待機中の画像。
    * **Thinking Sprite**: 思考中（Thinking）の画像。
    * **Talking Sprite Open/Closed**: 口パク用の上記画像。

### 3. マネージャーとのリンク

1. `AITuberManager` コンポーネントのInspectorを確認します。
2. 実行時（Awake）に自動的に `AIAvatarController` を探しますが、確実に行うためにInspectorの該当フィールドに、先ほど作成したアバターのオブジェクトを手動でセットしておくと安全です。

## 動作確認

適当なテスト用スクリプトから以下を呼び出してテストできます。

```csharp
void Start()
{
    // ユーザーからのメッセージを入力としてAI処理を開始
    AITuberManager.Instance.ProcessUserMessage("こんにちは！調子はどう？");
}
```

## 注意点

* **LLMService**: 現状はモック（偽の応答）です。`GenerateReply` メソッド内のAPIコール部分を実際のサーバー通信（OpenAI APIなど）に置き換えてください。
* **MemoryDatabase**: 現状はメモリ内リストです。永続化する場合は `OnDisable` でJSON保存するなどの処理を追加してください。
