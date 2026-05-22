using System;
using System.Collections.Generic;
using System.Threading;
using Cysharp.Threading.Tasks;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.Events;
using UnityEngine.UI;
using UnityMcpTextbook.Logic;
using UnityMcpTextbook.Presenter;
using UnityMcpTextbook.View;
using DG.Tweening;

// ===== 設計理由 =====
// 層: Composition Root (MonoBehaviour)
// 理由: GameLauncher は、ゲーム全体の進行（タイトル→ゲーム→結果）と、各画面の切り替え、非同期処理のライフサイクルを管理します。
// 責務:
//   - 3つの画面（Title, InGame, Result）の表示切り替え（パネル切替）。
//   - ゲーム開始時に Logic と Presenter をリセット（再生成）します。
//   - UIの具体的な生成は UIFactory に委譲します。
// =========================
namespace UnityMcpTextbook.App
{
    [DisallowMultipleComponent]
    public sealed class GameLauncher : MonoBehaviour
    {
        private enum GameState
        {
            Title,
            InGame,
            Result
        }

        private enum ResultAction
        {
            Retry,
            GoToTitle
        }

        private static GameLauncher current;
        private static readonly Vector2[] HolePositions =
        {
            new(-250f, 150f),
            new(0f, 150f),
            new(250f, 150f),
            new(-250f, -130f),
            new(0f, -130f),
            new(250f, -130f),
            new(-250f, -410f),
            new(0f, -410f),
            new(250f, -410f),
        };

        private readonly List<IDisposable> presenters = new();
        private CancellationTokenSource flowCancellationTokenSource;
        private CancellationTokenSource timerCancellationTokenSource;
        private CancellationTokenSource moleSpawnCancellationTokenSource;
        private TimerPresenter timerPresenter;
        private ScoreLogic scoreLogic;
        
        // 画面パネル（Canvas）を保持
        private GameObject titleCanvas;
        private GameObject gameplayCanvas;
        private GameObject scoreCanvas;
        private GameObject timerCanvas;
        private GameObject resultCanvas;

        private bool initialized;
        private Text resultScoreText;

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
        private static void Bootstrap()
        {
            EnsureInstance().Initialize();
        }

        private static GameLauncher EnsureInstance()
        {
            if (current != null) return current;

            current = FindFirstObjectByType<GameLauncher>();
            if (current != null) return current;

            var launcherObject = new GameObject(nameof(GameLauncher));
            DontDestroyOnLoad(launcherObject);
            current = launcherObject.AddComponent<GameLauncher>();
            
            var audioPlayer = launcherObject.AddComponent<RandomAudioPlayer>();
            audioPlayer.Initialize();

            return current;
        }

        public void Initialize()
        {
            if (initialized) return;

            Application.runInBackground = true;
            ConfigureMainCamera();
            EnsureEventSystem();

            // 最初にすべての画面（パネル）を作ってしまう
            CreateAllScreens();

            // ゲームのメインフローを開始
            initialized = true;
            flowCancellationTokenSource = new CancellationTokenSource();
            RunFlowAsync(flowCancellationTokenSource.Token).Forget();
        }

        private void Awake()
        {
            if (current != null && current != this)
            {
                Destroy(gameObject);
                return;
            }

            current = this;
            DontDestroyOnLoad(gameObject);
            Initialize();
        }

        private void OnDestroy()
        {
            CleanupAll();
            if (current == this) current = null;
        }

        /// <summary>
        /// 全ての画面パネルを事前に生成し、非表示にしておきます。
        /// </summary>
        private void CreateAllScreens()
        {
            // 1. タイトル画面
            titleCanvas = UIFactory.CreateOverlayCanvas(transform, "TitleCanvas", 5);
            var titleBg = UIFactory.CreateChildImage(titleCanvas.transform, "Background", new Vector2(1080, 1920), Vector2.zero, false);
            titleBg.sprite = UIFactory.LoadEditorSprite("Assets/Project/Images/Textures/title_background.png");
            
            var startBtnGo = UIFactory.CreateChildImage(titleCanvas.transform, "StartButton", new Vector2(300, 100), new Vector2(0, -500), true);
            startBtnGo.sprite = UIFactory.LoadEditorSprite("Assets/Project/Images/Atlas/btn_start.png");
            startBtnGo.gameObject.AddComponent<Button>(); // ボタン機能を追加
            var startText = UIFactory.CreateOverlayText(startBtnGo.transform, "Text", Vector2.zero, 40, Color.white, "START");
            UIFactory.MakeCenter(startText.rectTransform);

            // 2. ゲーム画面（背景と穴）
            gameplayCanvas = UIFactory.CreateGameplayCanvas(transform);
            UIFactory.CreateStageBackground(gameplayCanvas.transform);
            for (var i = 0; i < HolePositions.Length; i++)
            {
                UIFactory.CreateDefaultMoleHoleView(gameplayCanvas.transform, i, HolePositions[i]);
            }

            // 3. スコア画面
            scoreCanvas = UIFactory.CreateOverlayCanvas(transform, "ScoreCanvas", 10);
            Destroy(scoreCanvas.GetComponent<GraphicRaycaster>()); // クリックを透過させる
            // スコアを下に配置（Y: -220f, サイズ: 64）
            var scoreText = UIFactory.CreateOverlayText(scoreCanvas.transform, "ScoreText", new Vector2(0f, -220f), 64, Color.white, "スコア: 0");
            var scoreView = scoreCanvas.AddComponent<ScoreView>();
            scoreView.SetTextTarget(scoreText);

            // 4. タイマー画面
            timerCanvas = UIFactory.CreateOverlayCanvas(transform, "TimerCanvas", 10);
            Destroy(timerCanvas.GetComponent<GraphicRaycaster>()); // クリックを透過させる
            // タイマーを上に配置（Y: -96f, サイズ: 72）
            var timerText = UIFactory.CreateOverlayText(timerCanvas.transform, "TimerText", new Vector2(0f, -96f), 72, new Color(1f, 0.92f, 0.35f), "のこりじかん: 60");
            var timerView = timerCanvas.AddComponent<TimerView>();
            timerView.SetTextTarget(timerText);

            // 5. 結果画面
            resultCanvas = UIFactory.CreateOverlayCanvas(transform, "ResultCanvas", 20);
            var resultBg = UIFactory.CreateChildImage(resultCanvas.transform, "Background", new Vector2(1080, 1920), Vector2.zero, true);
            resultBg.GetComponent<Image>().color = new Color(0, 0, 0, 0.75f);
            resultBg.GetComponent<Image>().sprite = null;

            UIFactory.CreateOverlayText(resultCanvas.transform, "Title", new Vector2(0, -300), 80, Color.white, "RESULT");
            // スコア表記を日本語に変更
            resultScoreText = UIFactory.CreateOverlayText(resultCanvas.transform, "Score", new Vector2(0, -500), 100, Color.yellow, "スコア: 0");

            var retryBtnGo = UIFactory.CreateChildImage(resultCanvas.transform, "RetryButton", new Vector2(300, 100), new Vector2(0, -800), true);
            retryBtnGo.sprite = UIFactory.LoadEditorSprite("Assets/Project/Images/Atlas/btn_retry.png");
            retryBtnGo.gameObject.AddComponent<Button>(); // ボタン機能を追加
            var retryText = UIFactory.CreateOverlayText(retryBtnGo.transform, "Text", Vector2.zero, 30, Color.white, "もう一度");
            UIFactory.MakeCenter(retryText.rectTransform);

            var titleBtnGo = UIFactory.CreateChildImage(resultCanvas.transform, "TitleButton", new Vector2(300, 100), new Vector2(0, -950), true);
            titleBtnGo.sprite = UIFactory.LoadEditorSprite("Assets/Project/Images/Atlas/btn_title.png");
            titleBtnGo.gameObject.AddComponent<Button>(); // ボタン機能を追加
            var titleText = UIFactory.CreateOverlayText(titleBtnGo.transform, "Text", Vector2.zero, 30, Color.white, "タイトルへ");
            UIFactory.MakeCenter(titleText.rectTransform);
        }

        /// <summary>
        /// ゲームのメインループ（SetActive でパネルを切り替えます）。
        /// </summary>
        private async UniTask RunFlowAsync(CancellationToken cancellationToken)
        {
            var state = GameState.Title;

            while (!cancellationToken.IsCancellationRequested)
            {
                switch (state)
                {
                    case GameState.Title:
                        ShowTitleScreen();

                        // ボタンの点滅
                        var startBtn = titleCanvas.transform.Find("StartButton").GetComponent<Image>();
                        var tween = startBtn.DOFade(0.5f, 0.8f).SetLoops(-1, LoopType.Yoyo);

                        try
                        {
                            await WaitButtonPointDown(titleCanvas.transform.Find("StartButton").GetComponent<Button>(), cancellationToken);
                        }
                        finally
                        {
                            tween.Kill();
                            startBtn.color = Color.white; // 元に戻す
                        }
                        
                        state = GameState.InGame;
                        break;

                    case GameState.InGame:
                        ShowGameplayScreen();

                        await RunGameplayLoopAsync(cancellationToken);
                        
                        state = GameState.Result;
                        break;

                    case GameState.Result:
                        ShowResultScreen();

                        // スコアの反映と演出
                        if (resultScoreText != null && scoreLogic != null)
                        {
                            resultScoreText.text = $"スコア: {scoreLogic.Score}";
                            // 演出: スケール拡大＋黄色光 (1.5倍, 0.5秒)
                            resultScoreText.rectTransform.localScale = Vector3.one;
                            _ = resultScoreText.rectTransform.DOScale(1.5f, 0.5f).SetEase(Ease.OutBack);
                            var originalColor = resultScoreText.color;
                            _ = resultScoreText.DOColor(Color.yellow, 0.25f)
                                .SetLoops(2, LoopType.Yoyo)
                                .OnComplete(() => _ = resultScoreText.DOColor(originalColor, 0.25f));
                        }

                        var resultAction = await WaitResultActionAsync(cancellationToken);
                        state = resultAction == ResultAction.Retry ? GameState.InGame : GameState.Title;
                        break;
                }
            }
        }

        private void ShowTitleScreen()
        {
            SetScreenActive(title: true, gameplay: false, score: false, timer: false, result: false);
        }

        private void ShowGameplayScreen()
        {
            SetScreenActive(title: false, gameplay: true, score: true, timer: true, result: false);
        }

        private void ShowResultScreen()
        {
            SetScreenActive(title: false, gameplay: true, score: false, timer: false, result: true);
        }

        private void SetScreenActive(bool title, bool gameplay, bool score, bool timer, bool result)
        {
            titleCanvas.SetActive(title);
            gameplayCanvas.SetActive(gameplay);
            scoreCanvas.SetActive(score);
            timerCanvas.SetActive(timer);
            resultCanvas.SetActive(result);
        }

        private static async UniTask WaitButtonPointDown(Button button, CancellationToken cancellationToken)
        {
            var tcs = new UniTaskCompletionSource();
            UnityAction handler = () => tcs.TrySetResult();
            button.onClick.AddListener(handler);
            try
            {
                await tcs.Task.AttachExternalCancellation(cancellationToken);
            }
            finally
            {
                button.onClick.RemoveListener(handler);
            }
        }

        private async UniTask<ResultAction> WaitResultActionAsync(CancellationToken cancellationToken)
        {
            var retryBtn = resultCanvas.transform.Find("RetryButton").GetComponent<Button>();
            var titleBtn = resultCanvas.transform.Find("TitleButton").GetComponent<Button>();
            var tcs = new UniTaskCompletionSource<ResultAction>();
            UnityAction retryHandler = () => tcs.TrySetResult(ResultAction.Retry);
            UnityAction titleHandler = () => tcs.TrySetResult(ResultAction.GoToTitle);

            retryBtn.onClick.AddListener(retryHandler);
            titleBtn.onClick.AddListener(titleHandler);

            try
            {
                return await tcs.Task.AttachExternalCancellation(cancellationToken);
            }
            finally
            {
                retryBtn.onClick.RemoveListener(retryHandler);
                titleBtn.onClick.RemoveListener(titleHandler);
            }
        }

        private async UniTask RunGameplayLoopAsync(CancellationToken cancellationToken)
        {
            DisposePresenters(); // 前回のPresenterを破棄

            var gameConfig = new GameConfig();
            
            // Viewの取得
            var scoreView = scoreCanvas.GetComponent<ScoreView>();
            var timerView = timerCanvas.GetComponent<TimerView>();
            var holeViews = gameplayCanvas.GetComponentsInChildren<MoleHoleView>();

            // モグラの初期化（引っ込める）
            foreach (var hole in holeViews) hole.HideMole();

            // Logic と Presenter の再生成（これでリセットされます）
            scoreLogic = new ScoreLogic(new ScoreConfig());
            var scorePresenter = new ScorePresenter(scoreLogic, scoreView);
            scorePresenter.Initialize();
            presenters.Add(scorePresenter);

            var timerLogic = new TimerLogic(gameConfig);
            timerPresenter = new TimerPresenter(timerLogic, timerView);
            timerPresenter.Initialize();
            presenters.Add(timerPresenter);

            var moleSpawnLogic = new MoleSpawnLogic(new MoleSpawnConfig());
            var moleSpawnPresenter = new MoleSpawnPresenter(
                moleSpawnLogic,
                holeViews,
                scoreLogic.ApplyHit,
                scoreLogic.ApplyBossHit,
                scoreLogic.ApplyPoisonHit,
                scoreLogic.ApplyMiss);
            moleSpawnPresenter.Initialize();
            presenters.Add(moleSpawnPresenter);

            // 開始
            timerCancellationTokenSource = CancellationTokenSource.CreateLinkedTokenSource(cancellationToken);
            moleSpawnCancellationTokenSource = CancellationTokenSource.CreateLinkedTokenSource(cancellationToken);

            var timeUpTcs = new UniTaskCompletionSource();
            Action onTimeUp = () => timeUpTcs.TrySetResult();
            timerPresenter.OnTimeUp += onTimeUp;

            timerPresenter.StartAsync(timerCancellationTokenSource.Token).Forget();
            moleSpawnPresenter.StartAsync(moleSpawnCancellationTokenSource.Token).Forget();

            try
            {
                // 時間切れまで待つ
                await timeUpTcs.Task.AttachExternalCancellation(cancellationToken);
            }
            finally
            {
                timerPresenter.OnTimeUp -= onTimeUp;
                CancelTimer();
                CancelMoleSpawn();
            }
        }

        #region Cleanup
        private void CleanupAll()
        {
            CancelFlow();
            CancelTimer();
            CancelMoleSpawn();
            DisposePresenters();
            if (RandomAudioPlayer.Instance != null)
            {
                RandomAudioPlayer.Instance.Dispose();
            }
        }

        private void CancelFlow()
        {
            flowCancellationTokenSource?.Cancel();
            flowCancellationTokenSource?.Dispose();
            flowCancellationTokenSource = null;
        }

        private void CancelTimer()
        {
            timerCancellationTokenSource?.Cancel();
            timerCancellationTokenSource?.Dispose();
            timerCancellationTokenSource = null;
        }

        private void CancelMoleSpawn()
        {
            moleSpawnCancellationTokenSource?.Cancel();
            moleSpawnCancellationTokenSource?.Dispose();
            moleSpawnCancellationTokenSource = null;
        }

        private void DisposePresenters()
        {
            foreach (var presenter in presenters)
            {
                presenter.Dispose();
            }
            presenters.Clear();
        }
        #endregion

        #region Private Helpers
        private static void EnsureEventSystem()
        {
            if (FindFirstObjectByType<EventSystem>() != null) return;

            var eventSystemObject = new GameObject("EventSystem", typeof(EventSystem), typeof(StandaloneInputModule));
            DontDestroyOnLoad(eventSystemObject);
        }

        private static void ConfigureMainCamera()
        {
            var mainCamera = Camera.main;
            if (mainCamera == null) return;

            mainCamera.clearFlags = CameraClearFlags.SolidColor;
            mainCamera.backgroundColor = Color.black;
        }
        #endregion
    }
}
