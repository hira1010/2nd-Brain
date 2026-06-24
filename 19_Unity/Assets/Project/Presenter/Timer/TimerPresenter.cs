using System;
using System.Threading;
using Cysharp.Threading.Tasks;
using UnityMcpTextbook.Logic;
using UnityMcpTextbook.View;

// ===== Design Reason =====
// Layer: Presenter (Pure C#)
// Reason: TimerPresenter bridges TimerLogic notifications to TimerView display commands without owning timer rules.
// Responsibilities:
//   - Push initial remaining seconds to TimerView.
//   - Subscribe to TimerLogic.OnRemainingSecondsChanged.
//   - Relay time-up notification for later screen transitions.
//   - Unsubscribe on Dispose.
// =========================
namespace UnityMcpTextbook.Presenter
{
    public sealed class TimerPresenter : IDisposable
    {
        private readonly TimerLogic logic;
        private readonly TimerView view;

        public TimerPresenter(TimerLogic logic, TimerView view)
        {
            this.logic = logic ?? throw new ArgumentNullException(nameof(logic));
            this.view = view ?? throw new ArgumentNullException(nameof(view));
            this.logic.OnRemainingSecondsChanged += OnRemainingSecondsChanged;
            this.logic.OnTimeUp += OnTimeUpReceived;
        }

        public event Action OnTimeUp;

        public void Initialize()
        {
            view.SetRemainingSeconds(logic.RemainingSeconds);
        }

        public UniTask StartAsync(CancellationToken cancellationToken)
        {
            return logic.RunAsync(cancellationToken);
        }

        public void Dispose()
        {
            logic.OnRemainingSecondsChanged -= OnRemainingSecondsChanged;
            logic.OnTimeUp -= OnTimeUpReceived;
        }

        private void OnRemainingSecondsChanged(int remainingSeconds)
        {
            view.SetRemainingSeconds(remainingSeconds);
        }

        private void OnTimeUpReceived()
        {
            OnTimeUp?.Invoke();
        }
    }
}
