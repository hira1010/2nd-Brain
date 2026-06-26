using System;
using System.Threading;
using Cysharp.Threading.Tasks;
using DG.Tweening;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace UnityMcpTextbook.App
{
    internal sealed class GameFlowController : IDisposable
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

        private readonly GameScreenRefs screens;
        private GameplaySession currentSession;
        private Tween startButtonTween;
        private Tween resultScaleTween;
        private Tween resultColorTween;

        public GameFlowController(GameScreenRefs screens)
        {
            this.screens = screens ?? throw new ArgumentNullException(nameof(screens));
        }

        public async UniTask RunAsync(CancellationToken cancellationToken)
        {
            var state = GameState.Title;
            var lastScore = 0;

            try
            {
                while (!cancellationToken.IsCancellationRequested)
                {
                    switch (state)
                    {
                        case GameState.Title:
                            await RunTitleAsync(cancellationToken);
                            state = GameState.InGame;
                            break;

                        case GameState.InGame:
                            lastScore = await RunGameplayAsync(cancellationToken);
                            state = GameState.Result;
                            break;

                        case GameState.Result:
                            var resultAction = await RunResultAsync(lastScore, cancellationToken);
                            state = resultAction == ResultAction.Retry ? GameState.InGame : GameState.Title;
                            break;
                    }
                }
            }
            catch (OperationCanceledException) when (cancellationToken.IsCancellationRequested)
            {
            }
        }

        public void Dispose()
        {
            KillTweens();
            currentSession?.Dispose();
            currentSession = null;
        }

        private async UniTask RunTitleAsync(CancellationToken cancellationToken)
        {
            ShowTitleScreen();

            var startButtonImage = screens.StartButton.GetComponent<Image>();
            startButtonTween = startButtonImage.DOFade(0.5f, 0.8f).SetLoops(-1, LoopType.Yoyo);

            try
            {
                await WaitButtonPointDownAsync(screens.StartButton, cancellationToken);
            }
            finally
            {
                startButtonTween?.Kill();
                startButtonTween = null;
                startButtonImage.color = Color.white;
            }
        }

        private async UniTask<int> RunGameplayAsync(CancellationToken cancellationToken)
        {
            ShowGameplayScreen();
            currentSession?.Dispose();
            currentSession = new GameplaySession(screens);

            try
            {
                await currentSession.RunAsync(cancellationToken);
                return currentSession.Score;
            }
            finally
            {
                currentSession.Dispose();
                currentSession = null;
            }
        }

        private async UniTask<ResultAction> RunResultAsync(int score, CancellationToken cancellationToken)
        {
            ShowResultScreen();
            UpdateResultScore(score);
            return await WaitResultActionAsync(cancellationToken);
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
            screens.TitleCanvas.SetActive(title);
            screens.GameplayCanvas.SetActive(gameplay);
            screens.ScoreCanvas.SetActive(score);
            screens.TimerCanvas.SetActive(timer);
            screens.ResultCanvas.SetActive(result);
        }

        private void UpdateResultScore(int score)
        {
            var resultScoreText = screens.ResultScoreText;
            resultScoreText.text = $"スコア: {score}";
            resultScoreText.rectTransform.localScale = Vector3.one;

            resultScaleTween?.Kill();
            resultColorTween?.Kill();

            resultScaleTween = resultScoreText.rectTransform.DOScale(1.5f, 0.5f).SetEase(Ease.OutBack);
            var originalColor = resultScoreText.color;
            resultColorTween = resultScoreText.DOColor(Color.yellow, 0.25f)
                .SetLoops(2, LoopType.Yoyo)
                .OnComplete(() => resultColorTween = resultScoreText.DOColor(originalColor, 0.25f));
        }

        private static async UniTask WaitButtonPointDownAsync(Button button, CancellationToken cancellationToken)
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
            var tcs = new UniTaskCompletionSource<ResultAction>();
            UnityAction retryHandler = () => tcs.TrySetResult(ResultAction.Retry);
            UnityAction titleHandler = () => tcs.TrySetResult(ResultAction.GoToTitle);

            screens.RetryButton.onClick.AddListener(retryHandler);
            screens.TitleButton.onClick.AddListener(titleHandler);

            try
            {
                return await tcs.Task.AttachExternalCancellation(cancellationToken);
            }
            finally
            {
                screens.RetryButton.onClick.RemoveListener(retryHandler);
                screens.TitleButton.onClick.RemoveListener(titleHandler);
            }
        }

        private void KillTweens()
        {
            startButtonTween?.Kill();
            resultScaleTween?.Kill();
            resultColorTween?.Kill();
            startButtonTween = null;
            resultScaleTween = null;
            resultColorTween = null;
        }
    }
}
