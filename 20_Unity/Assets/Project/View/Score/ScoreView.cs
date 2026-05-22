using System.Globalization;
using DG.Tweening;
using UnityEngine;
using UnityEngine.UI;

// ===== Design Reason =====
// Layer: View (MonoBehaviour)
// Reason: Score rendering depends on Unity UI, so it stays in View and receives display commands from Presenter.
// Responsibilities:
//   - Keep the Text component reference.
//   - Render the current score as a number.
// Unity APIs: MonoBehaviour, Text.
// =========================
namespace UnityMcpTextbook.View
{
    [DisallowMultipleComponent]
    public sealed class ScoreView : MonoBehaviour
    {
        [SerializeField] private Text scoreText;

        private int _currentDisplayedScore = 0;
        private Tween _scoreTween;
        private Color _originalColor = Color.white;
        private bool _hasOriginalColor = false;

        public void SetTextTarget(Text text)
        {
            scoreText = text;
        }

        public void SetScore(int score)
        {
            if (scoreText == null)
            {
                return;
            }

            if (!_hasOriginalColor)
            {
                _originalColor = scoreText.color;
                _hasOriginalColor = true;
            }

            int startScore = _currentDisplayedScore;
            int targetScore = score;
            _currentDisplayedScore = targetScore;

            _scoreTween?.Kill();
            scoreText.rectTransform.DOKill();
            scoreText.DOKill();

            scoreText.rectTransform.localScale = Vector3.one;
            scoreText.color = _originalColor;

            // 0.2秒でカウントアップするアニメーション
            _scoreTween = DOTween.To(() => startScore, x =>
            {
                // 「スコア: 0」のように日本語でわかりやすく表示します
                scoreText.text = $"スコア: {x.ToString(CultureInfo.InvariantCulture)}";
            }, targetScore, 0.2f).SetEase(Ease.OutQuad);

            // 増点時（スコアアップ時）のみ、大きく弾ませて黄色く光らせる
            if (targetScore > startScore)
            {
                // 弾む
                scoreText.rectTransform.DOPunchScale(new Vector3(0.3f, 0.3f, 0f), 0.3f, 5, 1);
                // 黄色く光らせて元の色に戻す
                scoreText.color = Color.yellow;
                DOTween.To(() => scoreText.color, c => scoreText.color = c, _originalColor, 0.3f).SetEase(Ease.OutQuad);
            }
        }
    }
}
