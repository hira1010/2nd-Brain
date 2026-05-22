using System;

// ===== Design Reason =====
// Layer: Logic (Pure C#)
// Reason: Score is game state and calculation. It has no dependency on Unity display APIs.
// Responsibilities:
//   - Apply hit and miss score changes.
//   - Clamp score to zero or higher.
//   - Notify listeners only when the score value changes.
// =========================
namespace UnityMcpTextbook.Logic
{
    public sealed class ScoreLogic
    {
        private readonly ScoreConfig config;

        public ScoreLogic(ScoreConfig config)
        {
            this.config = config ?? throw new ArgumentNullException(nameof(config));
        }

        public event Action<int> OnScoreChanged;

        public int Score { get; private set; }

        public void ApplyHit()
        {
            Add(config.HitScoreDelta);
        }

        public void ApplyBossHit()
        {
            Add(config.HitScoreDelta * 2);
        }

        /// <summary>\u6bd2\u30e2\u30b0\u30e9\u3092\u53e9\u3044\u305f\u3068\u304d\u306b\u547c\u3073\u51fa\u3057\u307e\u3059\u3002\u8a2d\u5b9a\u5024\u306e\u5206\u3060\u3051\u6e1b\u70b9\u3057\u307e\u3059\u3002</summary>
        public void ApplyPoisonHit()
        {
            Add(config.PoisonHitScoreDelta);
        }

        public void ApplyMiss()
        {
            Add(config.MissScoreDelta);
        }

        private void Add(int delta)
        {
            var nextScore = Math.Max(0, Score + delta);
            if (nextScore == Score)
            {
                return;
            }

            Score = nextScore;
            OnScoreChanged?.Invoke(Score);
        }
    }
}
