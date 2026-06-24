Step 1 は MVP のフォルダと asmdef 境界だけを固定する。
Logic と View は相互参照せず、Presenter だけが橋渡しする。
GameLauncher は初期化と破棄の配線だけを持ち、ゲーム規則を書かない。
Tests.Editor は Logic の検証専用にし、Presenter / View は必要になるまでテストしない。
Score は Logic の ScoreLogic/ScoreConfig に閉じ、加減算値は設定値として外出しする。
ScoreView は Unity UI Text への表示命令だけを受け取り、計算や入力処理を持たない。
ScorePresenter は ScoreLogic の通知を ScoreView に渡すだけにし、購読解除を Dispose に集約する。
GameLauncher はテスト用ボタンを作らず、起動時に初期スコア 0 の表示だけを配線する。
Timer は UniTask と CancellationToken を使う TimerLogic に閉じ、View には時間計算を置かない。
制限時間は GameConfig.TimeLimitSeconds として設定値化し、テストでは極小秒数に差し替える。
TimerPresenter は残り秒通知と時間切れ通知を橋渡しし、GameLauncher は起動とキャンセルだけを担当する。
TimerView は整数秒の表示命令だけを受け取り、小数の扱いは Logic 側で済ませる。

MoleHoleView は View 層に置き、穴の2層表示・入力通知・見た目のアニメだけを担当する。
Step 4 では Logic / Presenter を作らず、GameLauncher の一時テストで出現アニメとヒットアニメだけを確認する。
モグラ画像は上層、空の穴画像は下層に固定し、後続のスポーン Logic から操作できる public メソッドを用意する。



MoleSpawnLogic handles index management for 9 holes, max 3 active, and hit/miss notifications in Logic.
MoleSpawnPresenter connects indices to MoleHoleView, handles score callbacks, and triggers View animations.
Step 5 spawns 9 holes via GameLauncher and starts spawn logic without screen transitions.

App 層は GameLauncher / GameFlowController / GameplaySession / GameScreenFactory に分ける。
GameLauncher はブートストラップと全体寿命管理だけを担当する。
GameFlowController は画面遷移、GameplaySession は Logic / Presenter の生成と破棄を担当する。
音声再生は現状機能維持を優先し、RandomAudioPlayer を残して View 側演出として扱う。
