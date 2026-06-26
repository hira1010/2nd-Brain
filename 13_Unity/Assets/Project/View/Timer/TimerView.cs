using System.Globalization;
using UnityEngine;
using UnityEngine.UI;

// ===== Design Reason =====
// Layer: View (MonoBehaviour)
// Reason: Timer rendering depends on Unity UI and should only receive display commands.
// Responsibilities:
//   - Keep the Text component reference.
//   - Render remaining seconds without decimals.
// Unity APIs: MonoBehaviour, Text.
// =========================
namespace UnityMcpTextbook.View
{
    [DisallowMultipleComponent]
    public sealed class TimerView : MonoBehaviour
    {
        [SerializeField] private Text remainingTimeText;

        public void SetTextTarget(Text text)
        {
            remainingTimeText = text;
        }

        public void SetRemainingSeconds(int remainingSeconds)
        {
            if (remainingTimeText == null)
            {
                return;
            }

            // 「のこりじかん: 60」のように日本語でわかりやすく表示します
            remainingTimeText.text = $"のこりじかん: {remainingSeconds.ToString(CultureInfo.InvariantCulture)}";
        }
    }
}
