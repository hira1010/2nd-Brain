using System.Collections;
using UnityEngine;

// ボール衝突時に物理反発を与え、新マネージャー群と連動してスコア、コンボ、エフェクト、画面揺れ、SEなどを発生させるバンパースクリプト
public class Bumper : MonoBehaviour
{
    [Tooltip("ボールを強く跳ね返す力")]
    public float bounceForce = 15f;

    [Tooltip("衝突時に得られる基礎スコア")]
    public int scoreValue = 100;

    [Tooltip("衝突時に一瞬ピカッと光るカラー")]
    public Color flashColor = Color.yellow;

    private SpriteRenderer spriteRenderer;
    private Color originalColor;
    private bool isFlashing = false;

    void Start()
    {
        spriteRenderer = GetComponent<SpriteRenderer>();
        if (spriteRenderer != null)
        {
            originalColor = spriteRenderer.color;
        }
    }

    // ボール（2D物理オブジェクト）が衝突した瞬間の処理
    void OnCollisionEnter2D(Collision2D collision)
    {
        if (collision.gameObject.CompareTag("Ball"))
        {
            Rigidbody2D ballRb = collision.gameObject.GetComponent<Rigidbody2D>();
            if (ballRb != null)
            {
                // ボールを押し戻す反射ベクトルを算出
                Vector2 bounceDirection = (collision.transform.position - transform.position).normalized;
                
                // ボールの既存速度を一旦リセットして一定の反射速度を与えます
                ballRb.linearVelocity = Vector2.zero;
                ballRb.AddForce(bounceDirection * bounceForce, ForceMode2D.Impulse);
            }

            // --- 新システム（各マネージャー）への通知連携 ---

            // 1. スコア加算 (倍率はScoreManager側で自動適用されます)
            if (ScoreManager.Instance != null)
            {
                ScoreManager.Instance.AddScore(scoreValue);
            }

            // 2. コンボ数の追加
            if (ComboManager.Instance != null)
            {
                ComboManager.Instance.RegisterHit();
            }

            // 衝突位置の正確な特定
            Vector2 contactPoint = collision.transform.position;
            if (collision.contactCount > 0)
            {
                contactPoint = collision.GetContact(0).point;
            }

            // 3. 衝突演出（火花、星、ハートなどのパーティクル）と得点ポップアップの生成
            if (EffectManager.Instance != null)
            {
                EffectManager.Instance.PlayHitEffect(contactPoint);
                
                // 現在の倍率を考慮したポップアップ数値を計算して表示
                int finalScore = scoreValue * (ScoreManager.Instance != null ? ScoreManager.Instance.Multiplier : 1);
                EffectManager.Instance.SpawnScorePopup(contactPoint, finalScore);
            }

            // 4. 衝撃に合わせたカメラの画面揺れ
            if (CameraShake.Instance != null)
            {
                CameraShake.Instance.Shake(0.16f, 0.22f);
            }

            // 5. 疑似ネオンライトを衝突時にフラッシュ（発光強調）させる
            if (LightManager.Instance != null)
            {
                LightManager.Instance.FlashNeonGlow(gameObject, flashColor);
            }

            // 6. バンパーヒット効果音の再生
            if (AudioManager.Instance != null)
            {
                AudioManager.Instance.PlayBumperHit();
            }

            // 7. バンパー自体の拡大＆明滅演出
            if (!isFlashing)
            {
                StartCoroutine(FlashBumperRoutine());
            }
        }
    }

    // バンパーを一瞬大きくし、色を変えてから元に戻す演出コルーチン
    private IEnumerator FlashBumperRoutine()
    {
        isFlashing = true;
        if (spriteRenderer != null)
        {
            spriteRenderer.color = flashColor;
            transform.localScale = transform.localScale * 1.15f; // スケールを拡大
            
            yield return new WaitForSeconds(0.1f);
            
            spriteRenderer.color = originalColor;
            transform.localScale = transform.localScale / 1.15f; // 元のスケールに戻す
        }
        isFlashing = false;
    }
}
