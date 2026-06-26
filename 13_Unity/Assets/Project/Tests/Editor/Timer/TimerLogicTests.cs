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
// Reason: Timer rules live in Logic and can be verified with tiny async durations without PlayMode.
// Responsibilities:
//   - Verify countdown notifications.
//   - Verify time-up notification.
//   - Verify CancellationToken stops without time-up.
// =========================
namespace UnityMcpTextbook.Tests.Editor
{
    public sealed class TimerLogicTests
    {
        [Test]
        public void Constructor_UsesConfiguredTimeLimit()
        {
            var logic = new TimerLogic(new GameConfig(timeLimitSeconds: 60d));

            Assert.That(logic.RemainingSeconds, Is.EqualTo(60));
        }

        [UnityTest]
        public IEnumerator RunAsync_NotifiesCountdownAndTimeUpWithTinyDuration()
        {
            return UniTask.ToCoroutine(async () =>
            {
                var logic = new TimerLogic(new GameConfig(timeLimitSeconds: 0.05d), TimeSpan.FromMilliseconds(5));
                var remainingValues = new List<int>();
                var timeUpCount = 0;
                using var cancellationTokenSource = new CancellationTokenSource();

                logic.OnRemainingSecondsChanged += remainingValues.Add;
                logic.OnTimeUp += () => timeUpCount++;

                await logic.RunAsync(cancellationTokenSource.Token);

                Assert.That(remainingValues, Does.Contain(1));
                Assert.That(remainingValues[^1], Is.EqualTo(0));
                Assert.That(timeUpCount, Is.EqualTo(1));
                Assert.That(logic.IsRunning, Is.False);
            });
        }

        [UnityTest]
        public IEnumerator RunAsync_CancellationStopsWithoutTimeUp()
        {
            return UniTask.ToCoroutine(async () =>
            {
                var logic = new TimerLogic(new GameConfig(timeLimitSeconds: 1d), TimeSpan.FromMilliseconds(10));
                var timeUpCount = 0;
                using var cancellationTokenSource = new CancellationTokenSource();
                logic.OnTimeUp += () => timeUpCount++;

                cancellationTokenSource.CancelAfter(TimeSpan.FromMilliseconds(30));
                await logic.RunAsync(cancellationTokenSource.Token);

                Assert.That(timeUpCount, Is.EqualTo(0));
                Assert.That(logic.RemainingSeconds, Is.GreaterThan(0));
                Assert.That(logic.IsRunning, Is.False);
            });
        }
    }
}
