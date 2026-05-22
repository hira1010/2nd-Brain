using System;
using System.Collections.Generic;
using System.Threading;
using Cysharp.Threading.Tasks;

// ===== 設計理由 =====
// 層: Logic (Pure C#)
// 理由: 活性な穴の選択、最大同時出現数の制限、ヒット判定、およびタイムアウト（見逃し）の計時はゲームのルールです。
// 責務:
//   - 穴のインデックスによってモグラをランダムに出現させる。
//   - View オブジェクトを知ることなく、活性なモグラの状態を保持する。
//   - 出現、ヒット、および見逃しイベントをインデックス付きで通知する。
//   - CancellationToken を通じて協調的に動作する。
// =====================
namespace UnityMcpTextbook.Logic
{
    public enum MoleType
    {
        Normal,
        Boss,
        /// <summary>叩いてはいけない毒モグラ。叩くと減点、見逃しても減点なし。</summary>
        Poison
    }

    /// <summary>
    /// 論理的な穴のインデックスによってモグラの出現状態を制御します。
    /// </summary>
    public sealed class MoleSpawnLogic
    {
        private readonly MoleSpawnConfig _config;
        private readonly Random _random;
        private readonly bool[] _activeMoles;
        private readonly MoleType[] _moleTypes;
        private readonly int[] _moleHps;
        private int _activeCount;

        /// <summary>
        /// モグラ出現ロジックを作成します。
        /// </summary>
        public MoleSpawnLogic(MoleSpawnConfig config, Random random = null)
        {
            _config = config ?? throw new ArgumentNullException(nameof(config));
            _random = random ?? new Random();
            _activeMoles = new bool[config.HoleCount];
            _moleTypes = new MoleType[config.HoleCount];
            _moleHps = new int[config.HoleCount];
        }

        /// <summary>モグラが穴のインデックスに出現したときに発生します。</summary>
        public event Action<int, MoleType> OnMoleAppeared;

        /// <summary>活性なモグラが完全に倒されたときに発生します。</summary>
        public event Action<int, MoleType> OnMoleHitDefeated;

        /// <summary>ボスモグラがダメージを受けて生き残っているときに発生します。</summary>
        public event Action<int, int> OnMoleHitDamaged;

        /// <summary>活性なモグラがヒットされずにタイムアウトしたときに発生します。</summary>
        public event Action<int, MoleType> OnMoleMissed;

        /// <summary>このロジックによって管理される穴の総数。</summary>
        public int HoleCount => _config.HoleCount;

        /// <summary>現在の活性なモグラの数。</summary>
        public int ActiveCount => _activeCount;

        /// <summary>インデックスのモグラが現在活性であるかどうかを返します。</summary>
        public bool IsActive(int holeIndex)
        {
            ValidateHoleIndex(holeIndex);
            return _activeMoles[holeIndex];
        }

        /// <summary>
        /// 指定した穴のモグラの現在HPを返します。モグラが非活性の場合は0を返します。
        /// </summary>
        public int GetCurrentHp(int holeIndex)
        {
            ValidateHoleIndex(holeIndex);
            return _activeMoles[holeIndex] ? _moleHps[holeIndex] : 0;
        }

        /// <summary>
        /// キャンセルされるまで、ランダムな出現の試みを繰り返します。
        /// </summary>
        public async UniTask RunAsync(CancellationToken cancellationToken)
        {
            while (!cancellationToken.IsCancellationRequested)
            {
                TrySpawnRandom(cancellationToken);
                var delaySeconds = GetNextSpawnIntervalSeconds();
                await UniTask.Delay(TimeSpan.FromSeconds(delaySeconds), DelayType.Realtime, cancellationToken: cancellationToken);
            }
        }

        /// <summary>
        /// 特定の穴のインデックスにモグラを出現させようとします。
        /// </summary>
        public bool TrySpawn(int holeIndex, MoleType type)
        {
            ValidateHoleIndex(holeIndex);
            if (_activeCount >= _config.MaxActiveMoles || _activeMoles[holeIndex])
            {
                return false;
            }

            _activeMoles[holeIndex] = true;
            _moleTypes[holeIndex] = type;
            _moleHps[holeIndex] = GetInitialHp(type);
            _activeCount++;
            OnMoleAppeared?.Invoke(holeIndex, type);
            return true;
        }

        /// <summary>
        /// 通常モグラを出現させようとします（互換性用）。
        /// </summary>
        public bool TrySpawn(int holeIndex)
        {
            return TrySpawn(holeIndex, MoleType.Normal);
        }

        /// <summary>
        /// 特定の穴のインデックスのモグラをヒットしようとします。
        /// </summary>
        public bool TryHit(int holeIndex)
        {
            ValidateHoleIndex(holeIndex);
            if (!_activeMoles[holeIndex])
            {
                return false;
            }

            _moleHps[holeIndex]--;
            if (_moleHps[holeIndex] > 0)
            {
                OnMoleHitDamaged?.Invoke(holeIndex, _moleHps[holeIndex]);
                return true;
            }

            var type = _moleTypes[holeIndex];
            Deactivate(holeIndex);
            OnMoleHitDefeated?.Invoke(holeIndex, type);
            return true;
        }

        private void TrySpawnRandom(CancellationToken cancellationToken)
        {
            if (_activeCount >= _config.MaxActiveMoles)
            {
                return;
            }

            var candidates = BuildInactiveCandidateIndices();

            if (candidates.Count == 0)
            {
                return;
            }

            var holeIndex = candidates[_random.Next(candidates.Count)];
            var type = GetRandomMoleType();

            if (TrySpawn(holeIndex, type) && type != MoleType.Boss)
            {
                WaitForMissAsync(holeIndex, cancellationToken).Forget();
            }
        }

        private List<int> BuildInactiveCandidateIndices()
        {
            var candidates = new List<int>(_config.HoleCount);
            for (var i = 0; i < _activeMoles.Length; i++)
            {
                if (!_activeMoles[i])
                {
                    candidates.Add(i);
                }
            }

            return candidates;
        }

        private MoleType GetRandomMoleType()
        {
            var roll = _random.NextDouble();
            if (roll < _config.PoisonSpawnProbability)
            {
                return MoleType.Poison;
            }

            if (roll < _config.PoisonSpawnProbability + _config.BossSpawnProbability)
            {
                return MoleType.Boss;
            }

            return MoleType.Normal;
        }

        private int GetInitialHp(MoleType type)
        {
            return type == MoleType.Boss ? _config.BossHitPoints : 1;
        }

        private async UniTask WaitForMissAsync(int holeIndex, CancellationToken cancellationToken)
        {
            try
            {
                await UniTask.Delay(TimeSpan.FromSeconds(_config.MoleVisibleDurationSeconds), DelayType.Realtime, cancellationToken: cancellationToken);
                if (!_activeMoles[holeIndex])
                {
                    return;
                }

                var type = _moleTypes[holeIndex];
                Deactivate(holeIndex);
                OnMoleMissed?.Invoke(holeIndex, type);
            }
            catch (OperationCanceledException) when (cancellationToken.IsCancellationRequested)
            {
            }
        }

        private double GetNextSpawnIntervalSeconds()
        {
            var range = _config.SpawnIntervalMaxSeconds - _config.SpawnIntervalMinSeconds;
            return _config.SpawnIntervalMinSeconds + _random.NextDouble() * range;
        }

        private void Deactivate(int holeIndex)
        {
            _activeMoles[holeIndex] = false;
            _activeCount--;
        }

        private void ValidateHoleIndex(int holeIndex)
        {
            if (holeIndex < 0 || holeIndex >= _activeMoles.Length)
            {
                throw new ArgumentOutOfRangeException(nameof(holeIndex), "Hole index is out of range.");
            }
        }
    }
}
