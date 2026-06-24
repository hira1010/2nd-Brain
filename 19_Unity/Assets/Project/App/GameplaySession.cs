using System;
using System.Threading;
using Cysharp.Threading.Tasks;
using UnityMcpTextbook.Logic;
using UnityMcpTextbook.Presenter;

namespace UnityMcpTextbook.App
{
    internal sealed class GameplaySession : IDisposable
    {
        private readonly GameScreenRefs screens;
        private CancellationTokenSource timerCancellationTokenSource;
        private CancellationTokenSource moleSpawnCancellationTokenSource;
        private ScorePresenter scorePresenter;
        private TimerPresenter timerPresenter;
        private MoleSpawnPresenter moleSpawnPresenter;
        private ScoreLogic scoreLogic;

        public GameplaySession(GameScreenRefs screens)
        {
            this.screens = screens ?? throw new ArgumentNullException(nameof(screens));
        }

        public int Score => scoreLogic?.Score ?? 0;

        public async UniTask RunAsync(CancellationToken cancellationToken)
        {
            ResetViews();
            CreatePresenters();
            await RunUntilTimeUpAsync(cancellationToken);
        }

        public void Dispose()
        {
            CancelTimer();
            CancelMoleSpawn();
            DisposePresenters();
        }

        private void ResetViews()
        {
            foreach (var hole in screens.HoleViews)
            {
                hole.HideMole();
            }
        }

        private void CreatePresenters()
        {
            scoreLogic = new ScoreLogic(new ScoreConfig());
            scorePresenter = new ScorePresenter(scoreLogic, screens.ScoreView);
            scorePresenter.Initialize();

            var timerLogic = new TimerLogic(new GameConfig());
            timerPresenter = new TimerPresenter(timerLogic, screens.TimerView);
            timerPresenter.Initialize();

            var moleSpawnLogic = new MoleSpawnLogic(new MoleSpawnConfig());
            moleSpawnPresenter = new MoleSpawnPresenter(
                moleSpawnLogic,
                screens.HoleViews,
                scoreLogic.ApplyHit,
                scoreLogic.ApplyBossHit,
                scoreLogic.ApplyPoisonHit,
                scoreLogic.ApplyMiss);
            moleSpawnPresenter.Initialize();
        }

        private async UniTask RunUntilTimeUpAsync(CancellationToken cancellationToken)
        {
            timerCancellationTokenSource = CancellationTokenSource.CreateLinkedTokenSource(cancellationToken);
            moleSpawnCancellationTokenSource = CancellationTokenSource.CreateLinkedTokenSource(cancellationToken);

            var timeUpTcs = new UniTaskCompletionSource();
            Action onTimeUp = () => timeUpTcs.TrySetResult();
            timerPresenter.OnTimeUp += onTimeUp;

            timerPresenter.StartAsync(timerCancellationTokenSource.Token).Forget();
            moleSpawnPresenter.StartAsync(moleSpawnCancellationTokenSource.Token).Forget();

            try
            {
                await timeUpTcs.Task.AttachExternalCancellation(cancellationToken);
            }
            finally
            {
                timerPresenter.OnTimeUp -= onTimeUp;
                CancelTimer();
                CancelMoleSpawn();
            }
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
            scorePresenter?.Dispose();
            timerPresenter?.Dispose();
            moleSpawnPresenter?.Dispose();
            scorePresenter = null;
            timerPresenter = null;
            moleSpawnPresenter = null;
        }
    }
}
