using System;

// ===== Design Reason =====
// Layer: Logic (Pure C#)
// Reason: Game-wide tuning values should be adjustable without touching feature logic.
// Responsibilities:
//   - Hold the timer limit in seconds.
// =========================
namespace UnityMcpTextbook.Logic
{
    public sealed class GameConfig
    {
        public GameConfig(double timeLimitSeconds = 60d)
        {
            if (timeLimitSeconds <= 0d)
            {
                throw new ArgumentOutOfRangeException(nameof(timeLimitSeconds), "Time limit must be greater than zero.");
            }

            TimeLimitSeconds = timeLimitSeconds;
        }

        public double TimeLimitSeconds { get; }
    }
}
