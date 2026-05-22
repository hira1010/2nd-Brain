using System.Collections.Generic;
using NUnit.Framework;
using UnityMcpTextbook.Logic;

// ===== Design Reason =====
// Layer: Tests.Editor
// Reason: Score calculation is pure Logic, so hit/miss behavior is verified without PlayMode or test buttons.
// Responsibilities:
//   - Verify hit addition.
//   - Verify miss subtraction.
//   - Verify zero clamp.
//   - Verify configurable deltas.
// =========================
namespace UnityMcpTextbook.Tests.Editor
{
    public sealed class ScoreLogicTests
    {
        [Test]
        public void ApplyHit_AddsHitScoreDeltaAndNotifies()
        {
            var logic = new ScoreLogic(new ScoreConfig());
            var notifiedScores = new List<int>();
            logic.OnScoreChanged += notifiedScores.Add;

            logic.ApplyHit();

            Assert.That(logic.Score, Is.EqualTo(10));
            CollectionAssert.AreEqual(new[] { 10 }, notifiedScores);
        }

        [Test]
        public void ApplyMiss_SubtractsMissScoreDeltaAndNotifies()
        {
            var logic = new ScoreLogic(new ScoreConfig());
            var notifiedScores = new List<int>();
            logic.OnScoreChanged += notifiedScores.Add;

            logic.ApplyHit();
            logic.ApplyMiss();

            Assert.That(logic.Score, Is.EqualTo(7));
            CollectionAssert.AreEqual(new[] { 10, 7 }, notifiedScores);
        }

        [Test]
        public void ApplyMiss_ClampsScoreAtZero()
        {
            var logic = new ScoreLogic(new ScoreConfig());
            var notifyCount = 0;
            logic.OnScoreChanged += _ => notifyCount++;

            logic.ApplyMiss();

            Assert.That(logic.Score, Is.EqualTo(0));
            Assert.That(notifyCount, Is.EqualTo(0));
        }

        [Test]
        public void ApplyMiss_ClampsScoreAtZeroAfterScoreWasPositive()
        {
            var logic = new ScoreLogic(new ScoreConfig());

            logic.ApplyHit();
            logic.ApplyMiss();
            logic.ApplyMiss();
            logic.ApplyMiss();
            logic.ApplyMiss();

            Assert.That(logic.Score, Is.EqualTo(0));
        }

        [Test]
        public void CustomConfig_ChangesHitAndMissDeltas()
        {
            var logic = new ScoreLogic(new ScoreConfig(hitScoreDelta: 25, missScoreDelta: -8));

            logic.ApplyHit();
            logic.ApplyMiss();

            Assert.That(logic.Score, Is.EqualTo(17));
        }

        [Test]
        public void ApplyBossHit_AddsDoubleHitScoreDeltaAndNotifies()
        {
            var logic = new ScoreLogic(new ScoreConfig());
            var notifiedScores = new List<int>();
            logic.OnScoreChanged += notifiedScores.Add;

            logic.ApplyBossHit();

            Assert.That(logic.Score, Is.EqualTo(20));
            CollectionAssert.AreEqual(new[] { 20 }, notifiedScores);
        }

        [Test]
        public void ApplyPoisonHit_SubtractsPoisonScoreDeltaAndNotifies()
        {
            // 通常モグラで10点稼いでから毒モグラを叩く → 10 - 20 = 0（0クランプ）
            var logic = new ScoreLogic(new ScoreConfig());
            var notifiedScores = new List<int>();
            logic.OnScoreChanged += notifiedScores.Add;

            logic.ApplyHit();        // +10
            logic.ApplyPoisonHit();  // -20 → クランプで 0（10→0 の変化なので通知あり）

            Assert.That(logic.Score, Is.EqualTo(0));
            CollectionAssert.AreEqual(new[] { 10, 0 }, notifiedScores);
        }

        [Test]
        public void ApplyPoisonHit_DoesNotNotifyWhenScoreIsAlreadyZero()
        {
            // スコアが0のまま毒モグラを叩いても通知が来ない（スコアが変わらないため）
            var logic = new ScoreLogic(new ScoreConfig());
            var notifyCount = 0;
            logic.OnScoreChanged += _ => notifyCount++;

            logic.ApplyPoisonHit();

            Assert.That(logic.Score, Is.EqualTo(0));
            Assert.That(notifyCount, Is.EqualTo(0));
        }

        [Test]
        public void ApplyPoisonHit_CustomPoisonDelta_IsApplied()
        {
            // 設定値を変えたときにその値が反映される
            var logic = new ScoreLogic(new ScoreConfig(hitScoreDelta: 50, missScoreDelta: 0, poisonHitScoreDelta: -10));

            logic.ApplyHit();        // +50
            logic.ApplyPoisonHit();  // -10

            Assert.That(logic.Score, Is.EqualTo(40));
        }
    }
}
