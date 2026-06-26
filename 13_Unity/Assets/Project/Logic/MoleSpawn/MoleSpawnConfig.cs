using System;

// ===== Design Reason =====
// Layer: Logic (Pure C#)
// Reason: Spawn counts, intervals, and visible duration are game rule parameters and must be testable without View.
// Responsibilities:
//   - Hold hole count and maximum active mole count.
//   - Hold spawn interval range.
//   - Hold visible duration before a miss is reported.
// =========================
namespace UnityMcpTextbook.Logic
{
    /// <summary>
    /// Configuration values for mole spawning.
    /// </summary>
    public sealed class MoleSpawnConfig
    {
        /// <summary>
        /// Creates spawn configuration.
        /// </summary>
        public MoleSpawnConfig(
            int holeCount = 9,
            int maxActiveMoles = 3,
            double spawnIntervalMinSeconds = 0.18d,
            double spawnIntervalMaxSeconds = 0.42d,
            double moleVisibleDurationSeconds = 1.8d,
            double bossSpawnProbability = 0.2d,
            double poisonSpawnProbability = 0.15d,
            int bossHitPoints = 100)
        {
            if (holeCount <= 0)
            {
                throw new ArgumentOutOfRangeException(nameof(holeCount), "Hole count must be greater than zero.");
            }

            if (maxActiveMoles <= 0 || maxActiveMoles > holeCount)
            {
                throw new ArgumentOutOfRangeException(nameof(maxActiveMoles), "Max active moles must be between one and hole count.");
            }

            if (spawnIntervalMinSeconds <= 0d)
            {
                throw new ArgumentOutOfRangeException(nameof(spawnIntervalMinSeconds), "Minimum spawn interval must be greater than zero.");
            }

            if (spawnIntervalMaxSeconds < spawnIntervalMinSeconds)
            {
                throw new ArgumentOutOfRangeException(nameof(spawnIntervalMaxSeconds), "Maximum spawn interval must be greater than or equal to minimum interval.");
            }

            if (moleVisibleDurationSeconds <= 0d)
            {
                throw new ArgumentOutOfRangeException(nameof(moleVisibleDurationSeconds), "Mole visible duration must be greater than zero.");
            }

            if (bossSpawnProbability < 0d || bossSpawnProbability > 1d)
            {
                throw new ArgumentOutOfRangeException(nameof(bossSpawnProbability), "Boss spawn probability must be between 0.0 and 1.0.");
            }

            if (poisonSpawnProbability < 0d || poisonSpawnProbability > 1d)
            {
                throw new ArgumentOutOfRangeException(nameof(poisonSpawnProbability), "Poison spawn probability must be between 0.0 and 1.0.");
            }

            if (bossHitPoints <= 0)
            {
                throw new ArgumentOutOfRangeException(nameof(bossHitPoints), "Boss hit points must be greater than zero.");
            }

            HoleCount = holeCount;
            MaxActiveMoles = maxActiveMoles;
            SpawnIntervalMinSeconds = spawnIntervalMinSeconds;
            SpawnIntervalMaxSeconds = spawnIntervalMaxSeconds;
            MoleVisibleDurationSeconds = moleVisibleDurationSeconds;
            BossSpawnProbability = bossSpawnProbability;
            PoisonSpawnProbability = poisonSpawnProbability;
            BossHitPoints = bossHitPoints;
        }

        /// <summary>Total number of holes.</summary>
        public int HoleCount { get; }

        /// <summary>Maximum number of moles that can be active at once.</summary>
        public int MaxActiveMoles { get; }

        /// <summary>Minimum interval between spawn attempts.</summary>
        public double SpawnIntervalMinSeconds { get; }

        /// <summary>Maximum interval between spawn attempts.</summary>
        public double SpawnIntervalMaxSeconds { get; }

        /// <summary>Seconds before an unhit mole is treated as missed.</summary>
        public double MoleVisibleDurationSeconds { get; }

        /// <summary>Probability of a boss mole spawning.</summary>
        public double BossSpawnProbability { get; }

        /// <summary>毒モグラが出現する確率。</summary>
        public double PoisonSpawnProbability { get; }

        /// <summary>Number of hits needed to defeat a boss mole.</summary>
        public int BossHitPoints { get; }
    }
}
