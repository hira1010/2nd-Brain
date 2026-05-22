using System;
using System.Threading;
using Cysharp.Threading.Tasks;
using DG.Tweening;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

// ===== Design Reason =====
// Layer: View (MonoBehaviour)
// Reason: Mole hole rendering, pointer input, and visual animation are Unity UI concerns and must stay out of Logic.
// Responsibilities:
//   - Keep the empty hole image visible as the lower layer.
//   - Show, hide, and animate the mole image as the upper layer.
//   - Publish hit input as an event without scoring or rule decisions.
// Unity APIs: Image, RectTransform, EventSystems, DOTween.
// =========================
namespace UnityMcpTextbook.View
{
    /// <summary>
    /// View层内で使用するモグラ表示種別。Presenterが Logic層の MoleType を変換して渡す。
    /// </summary>
    public enum MoleDisplayType
    {
        /// <summary>通常モグラ。</summary>
        Normal,
        /// <summary>ボスモグラ（赤色・画面いっぱい・HP100）。</summary>
        Boss,
        /// <summary>叩いてはいけない毒モグラ（緑色）。叩くと減点。</summary>
        Poison
    }

    /// <summary>
    /// Displays one mole hole with a permanent lower hole layer and a temporary upper mole layer.
    /// </summary>
    public sealed class MoleHoleView : MonoBehaviour, IPointerDownHandler
    {
        private const float AppearDurationSeconds = 0.22f;
        private const float HitDurationSeconds = 0.16f;
        private const float EscapeDurationSeconds = 0.24f;
        private const int AuraTextureSize = 128;

        [SerializeField] private Image holeImage;
        [SerializeField] private Image moleImage;
        [SerializeField] private Sprite holeSprite;
        [SerializeField] private Sprite appearSprite;
        [SerializeField] private Sprite hitSprite;
        [SerializeField] private Sprite escapeSprite;

        private Tween activeTween;
        private Tween auraTween;
        private Vector2 defaultMoleAnchoredPosition;
        private Vector2 defaultMoleSizeDelta;
        private bool hasDefaultMolePosition;
        private bool isHitEnabled;
        private Image bossAuraImage;
        private Text hpText;
        private static Sprite bossAuraSprite;

        /// <summary>Raised when the visible mole is clicked or tapped while hit input is enabled.</summary>
        public event Action OnHitRequested;

        /// <summary>Returns true when the upper mole image is currently visible.</summary>
        public bool IsMoleVisible => moleImage != null && moleImage.enabled;

        /// <summary>Assigns the lower hole image and upper mole image controlled by this view.</summary>
        public void SetImageTargets(Image targetHoleImage, Image targetMoleImage)
        {
            holeImage = targetHoleImage ?? throw new ArgumentNullException(nameof(targetHoleImage));
            moleImage = targetMoleImage ?? throw new ArgumentNullException(nameof(targetMoleImage));
            CaptureDefaultMolePosition();
        }

        /// <summary>Assigns sprites used by the hole and each mole visual state.</summary>
        public void SetSprites(Sprite targetHoleSprite, Sprite targetAppearSprite, Sprite targetHitSprite, Sprite targetEscapeSprite)
        {
            holeSprite = targetHoleSprite;
            appearSprite = targetAppearSprite;
            hitSprite = targetHitSprite;
            escapeSprite = targetEscapeSprite;

            if (holeImage != null)
            {
                holeImage.sprite = holeSprite;
            }
        }

        /// <summary>Enables or disables hit input for this hole.</summary>
        public void SetHitEnabled(bool enabled)
        {
            isHitEnabled = enabled;
        }

        /// <summary>Shows the mole instantly in its appeared state.</summary>
        public void ShowMole()
        {
            EnsureImages();
            KillActiveTween();
            SetMoleSprite(appearSprite);
            moleImage.enabled = true;
            moleImage.rectTransform.anchoredPosition = defaultMoleAnchoredPosition;
            moleImage.rectTransform.sizeDelta = defaultMoleSizeDelta;
            moleImage.rectTransform.localScale = Vector3.one;
        }

        /// <summary>Hides the upper mole image while keeping the lower empty hole visible.</summary>
        public void HideMole()
        {
            EnsureImages();
            KillActiveTween();
            SetHitEnabled(false);
            moleImage.enabled = false;
            moleImage.rectTransform.anchoredPosition = defaultMoleAnchoredPosition;
            moleImage.rectTransform.sizeDelta = defaultMoleSizeDelta;
            moleImage.rectTransform.localScale = Vector3.one;
            moleImage.color = Color.white;
            HideBossAura();
            HideHpText();
        }

        /// <summary>Plays the appear animation and enables hit input after it finishes.</summary>
        public async UniTask PlayAppearAsync(CancellationToken cancellationToken)
        {
            EnsureImages();
            KillActiveTween();
            SetHitEnabled(true); // 出現アニメーションの開始と同時にクリック判定を有効化する
            SetMoleSprite(appearSprite);
            moleImage.enabled = true;

            var rectTransform = moleImage.rectTransform;
            rectTransform.anchoredPosition = defaultMoleAnchoredPosition + new Vector2(0f, -38f);
            rectTransform.localScale = new Vector3(0.72f, 0.72f, 1f);

            var overshootPosition = defaultMoleAnchoredPosition + new Vector2(0f, 12f);
            activeTween = DOTween.Sequence()
                .Join(DOTween.To(() => rectTransform.anchoredPosition, value => rectTransform.anchoredPosition = value, overshootPosition, 0.14f).SetEase(Ease.OutQuad))
                .Join(DOTween.To(() => rectTransform.localScale, value => rectTransform.localScale = value, Vector3.one, 0.14f).SetEase(Ease.OutBack))
                .Append(DOTween.To(() => rectTransform.anchoredPosition, value => rectTransform.anchoredPosition = value, defaultMoleAnchoredPosition, 0.08f).SetEase(Ease.OutQuad));

            await WaitForTweenDurationAsync(AppearDurationSeconds, cancellationToken);
            rectTransform.anchoredPosition = defaultMoleAnchoredPosition;
            rectTransform.localScale = Vector3.one;
        }

        /// <summary>Plays the hit animation and hides the mole.</summary>
        public async UniTask PlayHitAsync(CancellationToken cancellationToken)
        {
            EnsureImages();
            KillActiveTween();
            SetHitEnabled(false);
            SetMoleSprite(hitSprite);
            moleImage.enabled = true;

            var rectTransform = moleImage.rectTransform;
            rectTransform.anchoredPosition = defaultMoleAnchoredPosition;
            rectTransform.localScale = Vector3.one;
            activeTween = DOTween.To(() => rectTransform.localScale, value => rectTransform.localScale = value, Vector3.zero, HitDurationSeconds)
                .SetEase(Ease.InBack);

            PlayHitFeedbackAsync(rectTransform.anchoredPosition, cancellationToken).Forget();

            await WaitForTweenDurationAsync(HitDurationSeconds, cancellationToken);
            HideMole();
        }

        /// <summary>Plays the escape animation and hides the mole.</summary>
        public async UniTask PlayEscapeAsync(CancellationToken cancellationToken)
        {
            EnsureImages();
            KillActiveTween();
            SetHitEnabled(false);
            SetMoleSprite(escapeSprite);
            moleImage.enabled = true;

            var rectTransform = moleImage.rectTransform;
            rectTransform.anchoredPosition = defaultMoleAnchoredPosition;
            rectTransform.localScale = Vector3.one;
            activeTween = DOTween.Sequence()
                .Join(DOTween.To(() => rectTransform.anchoredPosition, value => rectTransform.anchoredPosition = value, defaultMoleAnchoredPosition + new Vector2(0f, -54f), EscapeDurationSeconds).SetEase(Ease.InQuad))
                .Join(DOTween.To(() => rectTransform.localScale, value => rectTransform.localScale = value, new Vector3(0.78f, 0.78f, 1f), EscapeDurationSeconds).SetEase(Ease.InQuad));

            await WaitForTweenDurationAsync(EscapeDurationSeconds, cancellationToken);
            HideMole();
        }

        /// <summary>Returns the world position where hit effects should be spawned later.</summary>
        public Vector3 GetEffectWorldPosition()
        {
            EnsureImages();
            return moleImage.rectTransform.position;
        }

        /// <summary>Publishes hit input when this hole is clicked or tapped.</summary>
        public void OnPointerDown(PointerEventData eventData)
        {
            if (!isHitEnabled || !IsMoleVisible)
            {
                return;
            }

            OnHitRequested?.Invoke();
        }

        /// <summary>Presenterから渡された表示種別に応じてモグラの外観を切り替えます。</summary>
        public void SetMoleType(MoleDisplayType displayType)
        {
            if (moleImage == null) return;

            switch (displayType)
            {
                case MoleDisplayType.Boss:
                    ApplyBossMoleAppearance();
                    break;

                case MoleDisplayType.Poison:
                    ApplyPoisonMoleAppearance();
                    break;

                default:
                    ApplyNormalMoleAppearance();
                    break;
            }
        }

        private void ApplyBossMoleAppearance()
        {
            moleImage.rectTransform.sizeDelta = new Vector2(1080f, 1200f);
            moleImage.rectTransform.localScale = Vector3.one;
            moleImage.color = Color.red;
            ShowBossAura();
            EnsureHpText();
            hpText.text = string.Empty;
            hpText.gameObject.SetActive(true);
        }

        private void ApplyPoisonMoleAppearance()
        {
            moleImage.rectTransform.sizeDelta = defaultMoleSizeDelta;
            moleImage.rectTransform.localScale = Vector3.one;
            moleImage.color = new Color(0.2f, 0.85f, 0.3f, 1f);
            HideBossAura();
            HideHpText();
        }

        private void ApplyNormalMoleAppearance()
        {
            moleImage.rectTransform.sizeDelta = defaultMoleSizeDelta;
            moleImage.rectTransform.localScale = Vector3.one;
            moleImage.color = Color.white;
            HideBossAura();
            HideHpText();
        }

        private void ShowBossAura()
        {
            EnsureBossAuraImage();
            bossAuraImage.gameObject.SetActive(true);
            bossAuraImage.color = new Color(1f, 0.12f, 0f, 0.45f);
            bossAuraImage.rectTransform.localScale = Vector3.one;

            auraTween?.Kill();
            auraTween = DOTween.Sequence()
                .Join(bossAuraImage.rectTransform.DOScale(new Vector3(1.12f, 1.12f, 1f), 0.65f).SetEase(Ease.InOutSine))
                .Join(DOTween.To(GetBossAuraAlpha, SetBossAuraAlpha, 0.18f, 0.65f).SetEase(Ease.InOutSine))
                .SetLoops(-1, LoopType.Yoyo);
        }

        private float GetBossAuraAlpha()
        {
            return bossAuraImage.color.a;
        }

        private void SetBossAuraAlpha(float alpha)
        {
            var color = bossAuraImage.color;
            color.a = alpha;
            bossAuraImage.color = color;
        }

        private void HideBossAura()
        {
            auraTween?.Kill();
            auraTween = null;

            if (bossAuraImage == null)
            {
                return;
            }

            bossAuraImage.gameObject.SetActive(false);
            bossAuraImage.rectTransform.localScale = Vector3.one;
        }

        private void EnsureBossAuraImage()
        {
            if (bossAuraImage != null)
            {
                return;
            }

            var auraObject = new GameObject("BossAura", typeof(RectTransform), typeof(Image));
            auraObject.transform.SetParent(transform, false);
            auraObject.transform.SetSiblingIndex(moleImage.transform.GetSiblingIndex());

            var rectTransform = auraObject.GetComponent<RectTransform>();
            rectTransform.anchorMin = new Vector2(0.5f, 0.5f);
            rectTransform.anchorMax = new Vector2(0.5f, 0.5f);
            rectTransform.pivot = new Vector2(0.5f, 0.5f);
            rectTransform.anchoredPosition = defaultMoleAnchoredPosition + new Vector2(0f, 40f);
            rectTransform.sizeDelta = new Vector2(1280f, 1440f);

            bossAuraImage = auraObject.GetComponent<Image>();
            bossAuraImage.sprite = GetBossAuraSprite();
            bossAuraImage.preserveAspect = false;
            bossAuraImage.raycastTarget = false;
        }

        private static Sprite GetBossAuraSprite()
        {
            if (bossAuraSprite != null)
            {
                return bossAuraSprite;
            }

            var texture = new Texture2D(AuraTextureSize, AuraTextureSize, TextureFormat.RGBA32, false)
            {
                name = "GeneratedBossAura",
                wrapMode = TextureWrapMode.Clamp,
                filterMode = FilterMode.Bilinear
            };

            var center = new Vector2((AuraTextureSize - 1) * 0.5f, (AuraTextureSize - 1) * 0.5f);
            var radius = AuraTextureSize * 0.5f;
            for (var y = 0; y < AuraTextureSize; y++)
            {
                for (var x = 0; x < AuraTextureSize; x++)
                {
                    var distance = Vector2.Distance(new Vector2(x, y), center) / radius;
                    var alpha = Mathf.Clamp01(1f - distance);
                    alpha = alpha * alpha;
                    texture.SetPixel(x, y, new Color(1f, 0.08f, 0f, alpha));
                }
            }

            texture.Apply();
            bossAuraSprite = Sprite.Create(texture, new Rect(0f, 0f, AuraTextureSize, AuraTextureSize), new Vector2(0.5f, 0.5f), 100f);
            return bossAuraSprite;
        }

        private void HideHpText()
        {
            if (hpText != null)
            {
                hpText.gameObject.SetActive(false);
            }
        }

        private void EnsureHpText()
        {
            if (hpText != null) return;

            var hpTextGo = new GameObject("HpText", typeof(RectTransform), typeof(Text));
            hpTextGo.transform.SetParent(transform, false);

            var rectTransform = hpTextGo.GetComponent<RectTransform>();
            rectTransform.anchorMin = new Vector2(0.5f, 1f);
            rectTransform.anchorMax = new Vector2(0.5f, 1f);
            rectTransform.pivot = new Vector2(0.5f, 0.5f);
            rectTransform.anchoredPosition = new Vector2(0f, 10f);
            rectTransform.sizeDelta = new Vector2(100f, 30f);

            hpText = hpTextGo.GetComponent<Text>();
            hpText.font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf") ?? Resources.GetBuiltinResource<Font>("Arial.ttf");
            hpText.alignment = TextAnchor.MiddleCenter;
            hpText.fontSize = 24;
            hpText.color = Color.yellow;
            
            var outline = hpTextGo.AddComponent<Outline>();
            outline.effectColor = Color.black;
            outline.effectDistance = new Vector2(1f, -1f);
            
            hpText.raycastTarget = false;
        }

        public void UpdateHpDisplay(int remainingHp)
        {
            EnsureHpText();
            if (hpText != null)
            {
                hpText.text = $"HP: {remainingHp}";
            }
        }

        public async UniTask PlayDamageEffectAsync(CancellationToken cancellationToken)
        {
            EnsureImages();
            KillActiveTween();

            var rectTransform = moleImage.rectTransform;
            var originalColor = moleImage.color;
            
            moleImage.color = new Color(1f, 0.3f, 0.3f, 1f);
            activeTween = rectTransform.DOShakePosition(0.15f, 15f, 10, 90, false, true);

            PlayHitFeedbackAsync(rectTransform.anchoredPosition, cancellationToken).Forget();

            await UniTask.Delay(TimeSpan.FromSeconds(0.15f), cancellationToken: cancellationToken);

            moleImage.color = originalColor;
            rectTransform.anchoredPosition = defaultMoleAnchoredPosition;
        }

        private async UniTask PlayHitFeedbackAsync(Vector2 anchoredPosition, CancellationToken cancellationToken)
        {
            var effectGo = new GameObject("HitEffect", typeof(RectTransform), typeof(HitEffectView));
            effectGo.transform.SetParent(transform.parent, false);

            var effectView = effectGo.GetComponent<HitEffectView>();
            effectView.Initialize();

            if (RandomAudioPlayer.Instance != null)
            {
                RandomAudioPlayer.Instance.PlayRandomAsync().Forget();
            }

            await effectView.PlayAsync(anchoredPosition, cancellationToken);
        }

        private void OnDestroy()
        {
            KillActiveTween();
            HideBossAura();
        }

        private void EnsureImages()
        {
            if (holeImage == null)
            {
                throw new InvalidOperationException("Hole image is not assigned.");
            }

            if (moleImage == null)
            {
                throw new InvalidOperationException("Mole image is not assigned.");
            }

            CaptureDefaultMolePosition();
        }

        private void CaptureDefaultMolePosition()
        {
            if (moleImage == null || hasDefaultMolePosition)
            {
                return;
            }

            defaultMoleAnchoredPosition = moleImage.rectTransform.anchoredPosition;
            defaultMoleSizeDelta = moleImage.rectTransform.sizeDelta;
            hasDefaultMolePosition = true;
        }

        private void SetMoleSprite(Sprite sprite)
        {
            if (sprite != null)
            {
                moleImage.sprite = sprite;
            }
        }

        private async UniTask WaitForTweenDurationAsync(float durationSeconds, CancellationToken cancellationToken)
        {
            try
            {
                await UniTask.Delay(TimeSpan.FromSeconds(durationSeconds), cancellationToken: cancellationToken);
            }
            finally
            {
                KillActiveTween();
            }
        }

        private void KillActiveTween()
        {
            if (activeTween == null)
            {
                return;
            }

            activeTween.Kill();
            activeTween = null;
        }
    }
}
