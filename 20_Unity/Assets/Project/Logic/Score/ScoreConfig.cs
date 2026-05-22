// ===== Design Reason =====
// Layer: Logic (Pure C#)
// Reason: Score deltas are gameplay settings, so they must be adjustable without touching score calculation code.
// Responsibilities:
//   - Hold the hit score delta.
//   - Hold the miss score delta.
// =========================
namespace UnityMcpTextbook.Logic
{
    public sealed class ScoreConfig
    {
        public ScoreConfig(int hitScoreDelta = 10, int missScoreDelta = -3, int poisonHitScoreDelta = -20)
        {
            HitScoreDelta = hitScoreDelta;
            MissScoreDelta = missScoreDelta;
            PoisonHitScoreDelta = poisonHitScoreDelta;
        }

        public int HitScoreDelta { get; }

        public int MissScoreDelta { get; }

        /// <summary>毒モグラを叩いたときの減点値（負の整数）。</summary>
        public int PoisonHitScoreDelta { get; }
    }
}
