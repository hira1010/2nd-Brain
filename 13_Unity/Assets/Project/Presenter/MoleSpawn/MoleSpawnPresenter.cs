using System;
using System.Collections.Generic;
using System.Threading;
using Cysharp.Threading.Tasks;
using UnityMcpTextbook.Logic;
using UnityMcpTextbook.View;

// ===== 設計理由 =====
// 層: Presenter (Pure C#)
// 理由: MoleSpawnPresenter は、インデックスベースの出現ルールを具体的な MoleHoleView インスタンスおよびスコアのコールバックに結びつけます。
// 責務:
//   - MoleSpawnLogic の出現、ヒット、および見逃しイベントを購読する。
//   - 各 MoleHoleView のヒット要求を購読し、それをインデックスによって転送する。
//   - MoleType（Logic 層）を MoleDisplayType（View 層）に変換して View に渡す。
//   - 出現時のボス HP は Logic.GetCurrentHp() で取得し、View に渡す（View は HP を知らない）。
//   - 出現やスコアのルールを所有することなく、View のアニメーションをトリガーする。
//   - Dispose 時にすべてのイベントの購読を解除する。
// =====================
namespace UnityMcpTextbook.Presenter
{
    /// <summary>
    /// モグラ出現ロジックを穴の View に接続します。
    /// </summary>
    public sealed class MoleSpawnPresenter : IDisposable
    {
        private readonly MoleSpawnLogic _logic;
        private readonly IReadOnlyList<MoleHoleView> _views;
        private readonly Action _onHitScored;
        private readonly Action _onBossHitScored;
        private readonly Action _onPoisonHitScored;
        private readonly Action _onMissScored;
        private readonly Action[] _hitRequestHandlers;
        private CancellationToken _runningToken;

        /// <summary>
        /// モグラ出現のプレゼンターを作成します。
        /// </summary>
        public MoleSpawnPresenter(
            MoleSpawnLogic logic,
            IReadOnlyList<MoleHoleView> views,
            Action onHitScored,
            Action onBossHitScored,
            Action onPoisonHitScored,
            Action onMissScored)
        {
            _logic = logic ?? throw new ArgumentNullException(nameof(logic));
            _views = views ?? throw new ArgumentNullException(nameof(views));
            _onHitScored = onHitScored ?? throw new ArgumentNullException(nameof(onHitScored));
            _onBossHitScored = onBossHitScored ?? throw new ArgumentNullException(nameof(onBossHitScored));
            _onPoisonHitScored = onPoisonHitScored ?? throw new ArgumentNullException(nameof(onPoisonHitScored));
            _onMissScored = onMissScored ?? throw new ArgumentNullException(nameof(onMissScored));

            if (views.Count != logic.HoleCount)
            {
                throw new ArgumentException("View count must match hole count.", nameof(views));
            }

            _hitRequestHandlers = new Action[views.Count];
        }

        /// <summary>
        /// イベントを購読し、すべての穴の View を非表示として初期化します。
        /// </summary>
        public void Initialize()
        {
            _logic.OnMoleAppeared += OnMoleAppeared;
            _logic.OnMoleHitDefeated += OnMoleHitDefeated;
            _logic.OnMoleHitDamaged += OnMoleHitDamaged;
            _logic.OnMoleMissed += OnMoleMissed;

            for (var i = 0; i < _views.Count; i++)
            {
                var index = i;
                _hitRequestHandlers[i] = () => OnHitRequested(index);
                _views[i].OnHitRequested += _hitRequestHandlers[i];
                _views[i].HideMole();
            }
        }

        /// <summary>
        /// 繰り返しの出現の試みを開始します。
        /// </summary>
        public UniTask StartAsync(CancellationToken cancellationToken)
        {
            _runningToken = cancellationToken;
            return _logic.RunAsync(cancellationToken);
        }

        /// <summary>
        /// すべての Logic および View のイベントの購読を解除します。
        /// </summary>
        public void Dispose()
        {
            _logic.OnMoleAppeared -= OnMoleAppeared;
            _logic.OnMoleHitDefeated -= OnMoleHitDefeated;
            _logic.OnMoleHitDamaged -= OnMoleHitDamaged;
            _logic.OnMoleMissed -= OnMoleMissed;

            for (var i = 0; i < _views.Count; i++)
            {
                if (_hitRequestHandlers[i] != null)
                {
                    _views[i].OnHitRequested -= _hitRequestHandlers[i];
                    _hitRequestHandlers[i] = null;
                }
            }
        }

        private void OnHitRequested(int holeIndex)
        {
            _logic.TryHit(holeIndex);
        }

        private void OnMoleAppeared(int holeIndex, MoleType type)
        {
            // Logic の MoleType を View 層の MoleDisplayType に変換して渡す
            // （View は Logic アセンブリを参照できないため、Presenter が変換を担う）
            var displayType = ToDisplayType(type);
            _views[holeIndex].SetMoleType(displayType);

            // ボスの場合は Logic から現在 HP を取得して View に渡す
            // （HP の数値はゲーム状態なので Logic が持ち、View はこの数値を表示するだけ）
            if (type == MoleType.Boss)
            {
                _views[holeIndex].UpdateHpDisplay(_logic.GetCurrentHp(holeIndex));
            }

            _views[holeIndex].PlayAppearAsync(_runningToken).Forget();
        }

        private void OnMoleHitDefeated(int holeIndex, MoleType type)
        {
            // 種別に応じてスコアコールバックを振り分ける
            switch (type)
            {
                case MoleType.Boss:
                    _onBossHitScored.Invoke();
                    break;
                case MoleType.Poison:
                    // 毒モグラを叩いた → 減点
                    _onPoisonHitScored.Invoke();
                    break;
                default:
                    // 通常モグラを叩いた → 加点
                    _onHitScored.Invoke();
                    break;
            }

            _views[holeIndex].PlayHitAsync(_runningToken).Forget();
        }

        private void OnMoleHitDamaged(int holeIndex, int remainingHp)
        {
            // ボスがダメージを受けたが生き残っている：Logic から渡された残 HP をそのまま View へ
            _views[holeIndex].UpdateHpDisplay(remainingHp);
            _views[holeIndex].PlayDamageEffectAsync(_runningToken).Forget();
        }

        private void OnMoleMissed(int holeIndex, MoleType type)
        {
            // 通常モグラの見逃しのみ減点。ボスと毒モグラは見逃しても減点しない
            if (type == MoleType.Normal)
            {
                _onMissScored.Invoke();
            }

            _views[holeIndex].PlayEscapeAsync(_runningToken).Forget();
        }

        /// <summary>
        /// Logic 層の MoleType を View 層の MoleDisplayType に変換します。
        /// </summary>
        private static MoleDisplayType ToDisplayType(MoleType type)
        {
            switch (type)
            {
                case MoleType.Boss:   return MoleDisplayType.Boss;
                case MoleType.Poison: return MoleDisplayType.Poison;
                default:              return MoleDisplayType.Normal;
            }
        }
    }
}
