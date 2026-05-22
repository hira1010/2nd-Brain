using System;
using UnityMcpTextbook.Logic;
using UnityMcpTextbook.View;

// ===== Design Reason =====
// Layer: Presenter (Pure C#)
// Reason: ScorePresenter is the bridge from ScoreLogic state changes to ScoreView display commands.
// Responsibilities:
//   - Subscribe to ScoreLogic.OnScoreChanged.
//   - Push the initial score to ScoreView.
//   - Unsubscribe on Dispose.
// =========================
namespace UnityMcpTextbook.Presenter
{
    public sealed class ScorePresenter : IDisposable
    {
        private readonly ScoreLogic logic;
        private readonly ScoreView view;

        public ScorePresenter(ScoreLogic logic, ScoreView view)
        {
            this.logic = logic ?? throw new ArgumentNullException(nameof(logic));
            this.view = view ?? throw new ArgumentNullException(nameof(view));
            this.logic.OnScoreChanged += OnScoreChanged;
        }

        public void Initialize()
        {
            view.SetScore(logic.Score);
        }

        public void Dispose()
        {
            logic.OnScoreChanged -= OnScoreChanged;
        }

        private void OnScoreChanged(int score)
        {
            view.SetScore(score);
        }
    }
}
