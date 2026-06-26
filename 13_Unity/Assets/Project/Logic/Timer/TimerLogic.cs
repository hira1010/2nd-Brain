using System;
using System.Diagnostics;
using System.Threading;
using Cysharp.Threading.Tasks;

// ===== Design Reason =====
// Layer: Logic (Pure C#)
// Reason: Countdown state and time-up detection are game rules, so they must not live in View.
// Responsibilities:
//   - Count down from GameConfig.TimeLimitSeconds.
//   - Notify integer remaining seconds.
//   - Notify when time reaches zero.
//   - Stop cooperatively through CancellationToken.
// =========================
namespace UnityMcpTextbook.Logic
{
    public sealed class TimerLogic
    {
        private readonly GameConfig config;
        private readonly TimeSpan tickInterval;

        public TimerLogic(GameConfig config, TimeSpan? tickInterval = null)
        {
            this.config = config ?? throw new ArgumentNullException(nameof(config));
            this.tickInterval = tickInterval ?? TimeSpan.FromMilliseconds(100);
            if (this.tickInterval <= TimeSpan.Zero)
            {
                throw new ArgumentOutOfRangeException(nameof(tickInterval), "Tick interval must be greater than zero.");
            }

            RemainingSeconds = ToDisplaySeconds(this.config.TimeLimitSeconds);
        }

        public event Action<int> OnRemainingSecondsChanged;

        public event Action OnTimeUp;

        public int RemainingSeconds { get; private set; }

        public bool IsRunning { get; private set; }

        public async UniTask RunAsync(CancellationToken cancellationToken)
        {
            if (IsRunning)
            {
                return;
            }

            IsRunning = true;
            var stopwatch = Stopwatch.StartNew();
            SetRemainingSeconds(ToDisplaySeconds(config.TimeLimitSeconds), force: true);

            try
            {
                while (RemainingSeconds > 0)
                {
                    await UniTask.Delay(tickInterval, DelayType.Realtime, cancellationToken: cancellationToken);
                    var remaining = Math.Max(0d, config.TimeLimitSeconds - stopwatch.Elapsed.TotalSeconds);
                    SetRemainingSeconds(ToDisplaySeconds(remaining));
                }

                OnTimeUp?.Invoke();
            }
            catch (OperationCanceledException) when (cancellationToken.IsCancellationRequested)
            {
            }
            finally
            {
                stopwatch.Stop();
                IsRunning = false;
            }
        }

        private static int ToDisplaySeconds(double remainingSeconds)
        {
            return Math.Max(0, (int)Math.Ceiling(remainingSeconds));
        }

        private void SetRemainingSeconds(int remainingSeconds, bool force = false)
        {
            if (!force && remainingSeconds == RemainingSeconds)
            {
                return;
            }

            RemainingSeconds = remainingSeconds;
            OnRemainingSecondsChanged?.Invoke(RemainingSeconds);
        }
    }
}
