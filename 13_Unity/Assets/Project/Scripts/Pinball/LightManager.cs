using UnityEngine;
using System.Collections;
using System.Collections.Generic;

// ゲーム内のネオンライトや疑似発光体の明滅（チカチカ）および衝突時のフラッシュ演出を制御するスクリプト
public class LightManager : MonoBehaviour
{
    public static LightManager Instance { get; private set; }

    private List<SpriteRenderer> glowRenderers = new List<SpriteRenderer>();
    private float defaultAlpha = 0.35f;

    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
        }
    }

    private void Start()
    {
        // シーン内のすべての発光用スプライトをスキャン
        RefreshGlowList();
        
        // チカチカ明滅するスレッドを開始
        StartCoroutine(NeonFlickerRoutine());
    }

    // 新規作成されたパーツにも対応できるよう、スプライトを再収集する処理
    public void RefreshGlowList()
    {
        glowRenderers.Clear();
        SpriteRenderer[] allRenderers = FindObjectsByType<SpriteRenderer>(FindObjectsSortMode.None);
        foreach (var sr in allRenderers)
        {
            // "NeonGlow_" から始まる動的ライトオブジェクトを追跡します
            if (sr.gameObject.name.StartsWith("NeonGlow_"))
            {
                glowRenderers.Add(sr);
            }
        }
    }

    // 対象のオブジェクトを衝突時に一瞬ピカッと強く光らせる演出処理
    public void FlashNeonGlow(GameObject sourceObject, Color flashColor, float duration = 0.14f)
    {
        // オブジェクトの子供にある発光スプライトを検索
        SpriteRenderer sr = sourceObject.GetComponentInChildren<SpriteRenderer>();
        if (sr != null && sr.gameObject.name.StartsWith("NeonGlow_"))
        {
            StartCoroutine(FlashRoutine(sr, flashColor, duration));
        }
    }

    private IEnumerator FlashRoutine(SpriteRenderer sr, Color targetColor, float duration)
    {
        if (sr == null) yield break;
        
        Color originalColor = sr.color;
        // アルファ値を最大まで引き上げて強く輝かせます
        sr.color = new Color(targetColor.r, targetColor.g, targetColor.b, 0.85f);
        
        yield return new WaitForSeconds(duration);
        
        if (sr != null)
        {
            sr.color = originalColor;
        }
    }

    // ネオンライトが呼吸しているかのような揺らぎと、時折おこる一瞬の瞬き（チカチカ）を表現するコルーチン
    private IEnumerator NeonFlickerRoutine()
    {
        while (true)
        {
            // わずかなサイン波状のゆらぎ
            float wave = Mathf.Sin(Time.time * 4f) * 0.05f;
            float targetAlpha = Mathf.Clamp(defaultAlpha + wave + Random.Range(-0.03f, 0.03f), 0.2f, 0.5f);

            // 1.5%の確率で、ネオン管の接触不良のような「チカチカッ」としたリアルな明滅を発生
            if (Random.Range(0f, 100f) < 1.5f)
            {
                SetAllGlowAlpha(0.04f); // ほぼ消灯
                yield return new WaitForSeconds(0.06f);
                SetAllGlowAlpha(0.48f); // 復帰（やや強め）
                yield return new WaitForSeconds(0.04f);
                SetAllGlowAlpha(0.04f); // 再消灯
                yield return new WaitForSeconds(0.05f);
            }

            SetAllGlowAlpha(targetAlpha);
            yield return new WaitForSeconds(Random.Range(0.08f, 0.22f));
        }
    }

    // すべてのネオンの透明度を更新する
    private void SetAllGlowAlpha(float alpha)
    {
        for (int i = glowRenderers.Count - 1; i >= 0; i--)
        {
            if (glowRenderers[i] != null)
            {
                Color c = glowRenderers[i].color;
                glowRenderers[i].color = new Color(c.r, c.g, c.b, alpha);
            }
            else
            {
                // オブジェクトが削除されていたらリストから除外
                glowRenderers.RemoveAt(i);
            }
        }
    }
}
