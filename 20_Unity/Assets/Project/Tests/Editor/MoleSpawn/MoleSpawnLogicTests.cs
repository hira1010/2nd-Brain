using System;
using System.Collections;
using System.Collections.Generic;
using System.Threading;
using Cysharp.Threading.Tasks;
using NUnit.Framework;
using UnityEngine.TestTools;
using UnityMcpTextbook.Logic;

// ===== Design Reason =====
// Layer: Tests.Editor
// Reason: Spawn rules are Logic concerns and can be verified without Unity View objects.
// Responsibilities:
//   - Verify fixed-index spawn and hit notifications.
//   - Verify max active mole clamping.
//   - Verify tiny-duration miss notification through UniTask timing.
// =========================
namespace UnityMcpTextbook.Tests.Editor
{
    public sealed class MoleSpawnLogicTests
    {
        [Test]
        public void TrySpawn_ActivatesHoleAndNotifiesAppear()
        {
            var logic = new MoleSpawnLogic(new MoleSpawnConfig(holeCount: 9, maxActiveMoles: 3));
            var appeared = new List<Tuple<int, MoleType>>();
            logic.OnMoleAppeared += (index, type) => appeared.Add(Tuple.Create(index, type));

            var spawned = logic.TrySpawn(4);

            Assert.That(spawned, Is.True);
            Assert.That(logic.IsActive(4), Is.True);
            Assert.That(logic.ActiveCount, Is.EqualTo(1));
            Assert.That(appeared.Count, Is.EqualTo(1));
            Assert.That(appeared[0].Item1, Is.EqualTo(4));
            Assert.That(appeared[0].Item2, Is.EqualTo(MoleType.Normal));
        }

        [Test]
        public void TryHit_DeactivatesActiveHoleAndNotifiesHit()
        {
            var logic = new MoleSpawnLogic(new MoleSpawnConfig(holeCount: 9, maxActiveMoles: 3));
            var hits = new List<Tuple<int, MoleType>>();
            logic.OnMoleHitDefeated += (index, type) => hits.Add(Tuple.Create(index, type));

            logic.TrySpawn(2);
            var hit = logic.TryHit(2);

            Assert.That(hit, Is.True);
            Assert.That(logic.IsActive(2), Is.False);
            Assert.That(logic.ActiveCount, Is.EqualTo(0));
            Assert.That(hits.Count, Is.EqualTo(1));
            Assert.That(hits[0].Item1, Is.EqualTo(2));
            Assert.That(hits[0].Item2, Is.EqualTo(MoleType.Normal));
        }

        [Test]
        public void TrySpawn_ClampsToMaxActiveMoles()
        {
            var logic = new MoleSpawnLogic(new MoleSpawnConfig(holeCount: 4, maxActiveMoles: 3));

            Assert.That(logic.TrySpawn(0), Is.True);
            Assert.That(logic.TrySpawn(1), Is.True);
            Assert.That(logic.TrySpawn(2), Is.True);
            Assert.That(logic.TrySpawn(3), Is.False);
            Assert.That(logic.ActiveCount, Is.EqualTo(3));
        }

        [UnityTest]
        public IEnumerator RunAsync_NotifiesMissAfterTinyVisibleDuration()
        {
            return UniTask.ToCoroutine(async () =>
            {
                var config = new MoleSpawnConfig(
                    holeCount: 1,
                    maxActiveMoles: 1,
                    spawnIntervalMinSeconds: 0.005d,
                    spawnIntervalMaxSeconds: 0.005d,
                    moleVisibleDurationSeconds: 0.02d,
                    bossSpawnProbability: 0d,
                    poisonSpawnProbability: 0d); // 通常モグラのみ出現させて、テストの再現性を保証する
                var logic = new MoleSpawnLogic(config, new Random(1));
                var missed = new List<Tuple<int, MoleType>>();
                using var cancellationTokenSource = new CancellationTokenSource();
                logic.OnMoleMissed += (holeIndex, type) =>
                {
                    missed.Add(Tuple.Create(holeIndex, type));
                    cancellationTokenSource.Cancel();
                };

                try
                {
                    await logic.RunAsync(cancellationTokenSource.Token);
                }
                catch (OperationCanceledException)
                {
                }

                Assert.That(missed.Count, Is.GreaterThan(0));
                Assert.That(missed[0].Item1, Is.EqualTo(0));
                Assert.That(missed[0].Item2, Is.EqualTo(MoleType.Normal));
                Assert.That(logic.ActiveCount, Is.EqualTo(0));
            });
        }

        [Test]
        public void TrySpawn_BossMole_RequiresThreeHitsToDefeat()
        {
            var logic = new MoleSpawnLogic(new MoleSpawnConfig(holeCount: 9, maxActiveMoles: 3));
            var damaged = new List<Tuple<int, int>>();
            var defeated = new List<Tuple<int, MoleType>>();
            
            logic.OnMoleHitDamaged += (index, hp) => damaged.Add(Tuple.Create(index, hp));
            logic.OnMoleHitDefeated += (index, type) => defeated.Add(Tuple.Create(index, type));

            // ボスモグラを出現させる
            logic.TrySpawn(3, MoleType.Boss);
            Assert.That(logic.IsActive(3), Is.True);

            // 1回目のヒット
            var hit1 = logic.TryHit(3);
            Assert.That(hit1, Is.True);
            Assert.That(logic.IsActive(3), Is.True); // まだ倒れていない
            Assert.That(damaged.Count, Is.EqualTo(1));
            Assert.That(damaged[0].Item2, Is.EqualTo(2)); // 残りHP 2

            // 2回目のヒット
            var hit2 = logic.TryHit(3);
            Assert.That(hit2, Is.True);
            Assert.That(logic.IsActive(3), Is.True); // まだ倒れていない
            Assert.That(damaged.Count, Is.EqualTo(2));
            Assert.That(damaged[1].Item2, Is.EqualTo(1)); // 残りHP 1

            // 3回目のヒット
            var hit3 = logic.TryHit(3);
            Assert.That(hit3, Is.True);
            Assert.That(logic.IsActive(3), Is.False); // 倒れた！
            Assert.That(defeated.Count, Is.EqualTo(1));
            Assert.That(defeated[0].Item1, Is.EqualTo(3));
            Assert.That(defeated[0].Item2, Is.EqualTo(MoleType.Boss));
        }

        [Test]
        public void TrySpawn_PoisonMole_AppearsAndDefeatedByOneHit()
        {
            // 毒モグラは1回で倒れる（HPは1）
            var logic = new MoleSpawnLogic(new MoleSpawnConfig(holeCount: 9, maxActiveMoles: 3));
            var appeared = new List<Tuple<int, MoleType>>();
            var defeated = new List<Tuple<int, MoleType>>();

            logic.OnMoleAppeared += (index, type) => appeared.Add(Tuple.Create(index, type));
            logic.OnMoleHitDefeated += (index, type) => defeated.Add(Tuple.Create(index, type));

            var spawned = logic.TrySpawn(5, MoleType.Poison);
            Assert.That(spawned, Is.True);
            Assert.That(logic.IsActive(5), Is.True);
            Assert.That(appeared.Count, Is.EqualTo(1));
            Assert.That(appeared[0].Item2, Is.EqualTo(MoleType.Poison));

            // 1回叩けば倒れる
            var hit = logic.TryHit(5);
            Assert.That(hit, Is.True);
            Assert.That(logic.IsActive(5), Is.False);
            Assert.That(defeated.Count, Is.EqualTo(1));
            Assert.That(defeated[0].Item2, Is.EqualTo(MoleType.Poison));
        }

        [Test]
        public void TrySpawn_PoisonMole_GetCurrentHp_ReturnsOneOnSpawn()
        {
            // 出現直後のHP取得がLogicから正しく取れることを確認
            var logic = new MoleSpawnLogic(new MoleSpawnConfig(holeCount: 9, maxActiveMoles: 3));

            logic.TrySpawn(2, MoleType.Poison);
            Assert.That(logic.GetCurrentHp(2), Is.EqualTo(1));
        }

        [Test]
        public void GetCurrentHp_ReturnsZeroWhenInactive()
        {
            // 非活性の穴はHP 0 を返す
            var logic = new MoleSpawnLogic(new MoleSpawnConfig(holeCount: 9, maxActiveMoles: 3));
            Assert.That(logic.GetCurrentHp(0), Is.EqualTo(0));
        }
    }
}

