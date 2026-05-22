using System;
using System.Threading;
using Cysharp.Threading.Tasks;
using UnityEngine;
using UnityEngine.UI;

#if UNITY_EDITOR
using UnityEditor;
#endif

// ===== 設計理由 =====
// 層: View (MonoBehaviour)
// 理由: ヒット演出（星、斬撃、ドカン）の生成とアニメーションを担当します。
// 責務:
//   - ヒット位置にエフェクト画像を動的に生成する。
//   - パラパラ漫画アニメーションや移動を制御する。
//   - 再生完了後に自身（および生成したオブジェクト）を破棄する。
// =====================
namespace UnityMcpTextbook.View
{
    /// <summary>
    /// モグラを叩いたときのヒット演出を制御します。
    /// </summary>
    public sealed class HitEffectView : MonoBehaviour
    {
        private const string StarPathPrefix = "Assets/Project/Images/Atlas/hit_particle_star_0";
        private const string SlashPathPrefix = "Assets/Project/Images/Atlas/hit_particle_slash_0";
        private const string BasePath = "Assets/Project/Images/Atlas/hit_particle_base.png";
        private const string HammerPath = "Assets/Project/Images/Atlas/hammer_cursor.png";

        private Sprite[] _starSprites;
        private Sprite[] _slashSprites;
        private Sprite _baseSprite;
        private Sprite _hammerSprite;

        /// <summary>
        /// 演出に必要な素材をロードします。
        /// </summary>
        public void Initialize()
        {
            _starSprites = new Sprite[5];
            for (int i = 0; i < 5; i++)
            {
                _starSprites[i] = LoadEditorSprite($"{StarPathPrefix}{i}.png");
            }

            _slashSprites = new Sprite[4];
            for (int i = 0; i < 4; i++)
            {
                _slashSprites[i] = LoadEditorSprite($"{SlashPathPrefix}{i}.png");
            }

            _baseSprite = LoadEditorSprite(BasePath);
            _hammerSprite = LoadEditorSprite(HammerPath);
        }

        /// <summary>
        /// 指定された位置でヒット演出を再生します。
        /// </summary>
        public async UniTask PlayAsync(Vector2 anchoredPosition, CancellationToken cancellationToken)
        {
            // ドカン、星、斬撃、ピコピコハンマーの生成と再生を同時に走らせる
            await UniTask.WhenAll(
                PlayBaseAsync(anchoredPosition, cancellationToken),
                PlayStarsAsync(anchoredPosition, cancellationToken),
                PlaySlashAsync(anchoredPosition, cancellationToken),
                PlayHammerAsync(anchoredPosition, cancellationToken)
            );

            // 演出が終わったらこのコンポーネントがついているオブジェクトごと消す
            Destroy(gameObject);
        }

        private async UniTask PlayBaseAsync(Vector2 pos, CancellationToken token)
        {
            var go = CreateImageObject("Base", transform, new Vector2(150, 150), pos, _baseSprite);
            var rect = go.GetComponent<RectTransform>();
            var image = go.GetComponent<Image>();

            float duration = 0.3f;
            float elapsed = 0f;
            while (elapsed < duration)
            {
                float t = elapsed / duration;
                rect.localScale = Vector3.one * (1f + t * 0.5f); // 拡大
                image.color = new Color(1, 1, 1, 1f - t); // フェードアウト
                elapsed += Time.deltaTime;
                await UniTask.Yield(PlayerLoopTiming.Update, token);
            }
            Destroy(go);
        }

        private async UniTask PlayStarsAsync(Vector2 pos, CancellationToken token)
        {
            int count = 8;
            var tasks = new UniTask[count];
            for (int i = 0; i < count; i++)
            {
                float angle = i * (360f / count);
                tasks[i] = PlaySingleStarAsync(pos, angle, token);
            }
            await UniTask.WhenAll(tasks);
        }

        private async UniTask PlaySingleStarAsync(Vector2 pos, float angle, CancellationToken token)
        {
            var go = CreateImageObject("Star", transform, new Vector2(40, 40), pos, _starSprites[0]);
            var rect = go.GetComponent<RectTransform>();
            var image = go.GetComponent<Image>();

            Vector2 dir = new Vector2(Mathf.Cos(angle * Mathf.Deg2Rad), Mathf.Sin(angle * Mathf.Deg2Rad));
            float speed = 300f;
            float duration = 0.4f;
            float elapsed = 0f;

            while (elapsed < duration)
            {
                float t = elapsed / duration;
                rect.anchoredPosition += dir * speed * Time.deltaTime;
                
                // パラパラ漫画
                int frame = Mathf.FloorToInt(t * _starSprites.Length);
                frame = Mathf.Clamp(frame, 0, _starSprites.Length - 1);
                image.sprite = _starSprites[frame];

                elapsed += Time.deltaTime;
                await UniTask.Yield(PlayerLoopTiming.Update, token);
            }
            Destroy(go);
        }

        private async UniTask PlaySlashAsync(Vector2 pos, CancellationToken token)
        {
            var go = CreateImageObject("Slash", transform, new Vector2(200, 200), pos, _slashSprites[0]);
            var rect = go.GetComponent<RectTransform>();
            var image = go.GetComponent<Image>();

            // ランダムな角度
            rect.localRotation = Quaternion.Euler(0, 0, UnityEngine.Random.Range(0f, 360f));

            float duration = 0.2f;
            float elapsed = 0f;
            while (elapsed < duration)
            {
                float t = elapsed / duration;
                int frame = Mathf.FloorToInt(t * _slashSprites.Length);
                frame = Mathf.Clamp(frame, 0, _slashSprites.Length - 1);
                image.sprite = _slashSprites[frame];

                elapsed += Time.deltaTime;
                await UniTask.Yield(PlayerLoopTiming.Update, token);
            }
            Destroy(go);
        }

        private GameObject CreateImageObject(string name, Transform parent, Vector2 size, Vector2 pos, Sprite sprite)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(Image));
            go.transform.SetParent(parent, false);
            var rect = go.GetComponent<RectTransform>();
            rect.anchoredPosition = pos;
            rect.sizeDelta = size;
            var img = go.GetComponent<Image>();
            img.sprite = sprite;
            img.preserveAspect = true;
            img.raycastTarget = false;
            return go;
        }

        private async UniTask PlayHammerAsync(Vector2 pos, CancellationToken token)
        {
            if (_hammerSprite == null) return;

            // モグラの右上から叩くように出現させる
            Vector2 startPos = pos + new Vector2(80f, 100f);
            var go = CreateImageObject("Hammer", transform, new Vector2(120, 120), startPos, _hammerSprite);
            var rect = go.GetComponent<RectTransform>();
            var image = go.GetComponent<Image>();

            // ピボットを左下に調整（柄のあたり）
            rect.pivot = new Vector2(0.2f, 0.2f);
            // ピボット位置をずらしたため、モグラの上を叩くように位置を微調整
            rect.anchoredPosition = pos + new Vector2(30f, 40f);

            // 振り下ろすアニメーション
            float duration = 0.15f;
            float elapsed = 0f;
            
            // 開始角度（振り上げる）と終了角度（振り下ろす）
            float startAngle = 45f;
            float endAngle = -30f;

            while (elapsed < duration)
            {
                float t = elapsed / duration;
                float tEase = t * (2 - t); // イージング（OutQuad）
                
                float angle = Mathf.Lerp(startAngle, endAngle, tEase);
                rect.localRotation = Quaternion.Euler(0, 0, angle);

                elapsed += Time.deltaTime;
                await UniTask.Yield(PlayerLoopTiming.Update, token);
            }

            // 叩いた後の余韻（0.1秒フェードアウト）
            float fadeDuration = 0.10f;
            elapsed = 0f;
            while (elapsed < fadeDuration)
            {
                float t = elapsed / fadeDuration;
                image.color = new Color(1, 1, 1, 1f - t);
                elapsed += Time.deltaTime;
                await UniTask.Yield(PlayerLoopTiming.Update, token);
            }

            Destroy(go);
        }

        private static Sprite LoadEditorSprite(string assetPath)
        {
#if UNITY_EDITOR
            var texture = AssetDatabase.LoadAssetAtPath<Texture2D>(assetPath);
            if (texture == null) return null;
            return Sprite.Create(texture, new Rect(0f, 0f, texture.width, texture.height), new Vector2(0.5f, 0.5f), 100f);
#else
            return null;
#endif
        }
    }
}
