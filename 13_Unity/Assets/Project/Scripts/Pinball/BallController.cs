using UnityEngine;

// ピンボールのボール自体にアタッチし、速度制限、壁すり抜け防止、ネオン軌跡（トレイル）、スタック脱出を制御するスクリプト
public class BallController : MonoBehaviour
{
    [Header("ボール物理設定")]
    [Tooltip("玉が速すぎて壁を突き抜けたり物理計算が壊れたりするのを防ぐ最高制限速度")]
    public float maxSpeedLimit = 22f;

    [Tooltip("静止した（挟まった）とみなすまでの時間（秒）")]
    public float stuckTriggerTime = 3.0f;

    private Rigidbody2D rb;
    private TrailRenderer trailRenderer;
    private float stuckTimer = 0f;

    private void Awake()
    {
        rb = GetComponent<Rigidbody2D>();
        if (rb != null)
        {
            // 動的衝突判定（Continuous）にして高速での突き抜けを防止します
            rb.collisionDetectionMode = CollisionDetectionMode2D.Continuous;
        }

        // プログラムで動的にボールの背後にネオン色の軌跡を引くエフェクトを追加
        AttachNeonTrail();
    }

    private void Update()
    {
        if (rb == null) return;

        // ボールの速度制限（スピード超過による挙動破綻を防ぐ）
        if (rb.linearVelocity.magnitude > maxSpeedLimit)
        {
            rb.linearVelocity = rb.linearVelocity.normalized * maxSpeedLimit;
        }

        // 動かなくなった（スタック）場合のレスキュー判定
        CheckAndRescueStuck();
    }

    // 動的にネオンの光跡をアタッチする処理
    private void AttachNeonTrail()
    {
        trailRenderer = gameObject.AddComponent<TrailRenderer>();
        
        // 軌跡の寿命、幅の設定
        trailRenderer.time = 0.32f;
        trailRenderer.startWidth = 0.3f;
        trailRenderer.endWidth = 0f;
        
        // ネオンブルーからネオンピンクへとグラデーションしながらフェードアウトする配色
        Gradient trailGradient = new Gradient();
        trailGradient.SetKeys(
            new GradientColorKey[] { 
                new GradientColorKey(new Color(0f, 0.94f, 1f), 0.0f),    // 先頭: シアンブルー
                new GradientColorKey(new Color(1f, 0.08f, 0.58f), 0.5f)  // 中間: ホットピンク
            },
            new GradientAlphaKey[] { 
                new GradientAlphaKey(0.8f, 0.0f), 
                new GradientAlphaKey(0f, 1.0f) 
            }
        );
        trailRenderer.colorGradient = trailGradient;
        
        // マテリアルには標準のSprites/Defaultを割り当てることでマゼンタエラーを防ぐ
        Shader unlitShader = Shader.Find("Sprites/Default");
        if (unlitShader != null)
        {
            trailRenderer.material = new Material(unlitShader);
        }
    }

    // ボールが挟まって動かなくなった際に微弱な力を加えて救出する処理
    private void CheckAndRescueStuck()
    {
        // 速度が極小（ほぼ止まっている）状態の場合
        if (rb.linearVelocity.magnitude < 0.16f)
        {
            stuckTimer += Time.deltaTime;
            if (stuckTimer >= stuckTriggerTime)
            {
                // ランダムに左右・上方向へ弾いて脱出させます
                float pushX = Random.value > 0.5f ? 2.2f : -2.2f;
                rb.AddForce(new Vector2(pushX, 1.8f), ForceMode2D.Impulse);
                
                stuckTimer = 0f; // タイマーリセット
                Debug.Log("[BallController] ボールのスタックを検知、救出用ノックバックを行いました。");
            }
        }
        else
        {
            stuckTimer = 0f;
        }
    }
}
