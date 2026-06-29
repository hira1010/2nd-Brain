using UnityEngine;

// スペースキー長押しで発射パワーをチャージし、キーを離した瞬間にボールを勢いよく打ち出すランチャー（発射台）スクリプト
public class Launcher : MonoBehaviour
{
    [Header("ランチャー調整")]
    [Tooltip("最大まで溜めた際の発射推進力")]
    public float maxLaunchForce = 35f;

    [Tooltip("パワーが溜まる速度（チャージ速度）")]
    public float chargeSpeed = 18f;

    private float currentPower = 0f;
    private bool isBallReady = false;
    private Rigidbody2D ballRigidbody;

    private void Update()
    {
        // ボールが発射ゾーンに触れており、かつ物理コンポーネントが取得できている場合のみ入力を受ける
        if (isBallReady && ballRigidbody != null)
        {
            if (Input.GetKey(KeyCode.Space))
            {
                // スペースキー長押し中、最大値までパワーを溜める
                currentPower = Mathf.MoveTowards(currentPower, maxLaunchForce, chargeSpeed * Time.deltaTime);
                
                // UIManagerを介して、画面のパワーゲージ（0.0 〜 1.0）の表示を更新します
                if (UIManager.Instance != null)
                {
                    UIManager.Instance.SetPowerGauge(currentPower / maxLaunchForce);
                }
            }

            if (Input.GetKeyUp(KeyCode.Space))
            {
                // キーを離した瞬間に上方向（Vector2.up）へ衝撃力（Impulse）を与えて打ち出す
                ballRigidbody.AddForce(Vector2.up * currentPower, ForceMode2D.Impulse);
                
                // 発射SEを再生します
                if (AudioManager.Instance != null)
                {
                    AudioManager.Instance.PlayLauncherLaunch();
                }

                // パワーとゲージを初期化
                currentPower = 0f;
                if (UIManager.Instance != null)
                {
                    UIManager.Instance.SetPowerGauge(0f);
                }

                // 発射済みとして状態を戻す
                isBallReady = false;
                ballRigidbody = null;
            }
        }
    }

    // ボールが発射台（トリガーコライダー）に進入した時の処理
    private void OnTriggerEnter2D(Collider2D other)
    {
        if (other.CompareTag("Ball"))
        {
            ballRigidbody = other.GetComponent<Rigidbody2D>();
            if (ballRigidbody != null)
            {
                isBallReady = true;
            }
        }
    }

    // ボールが途中で発射台から零れ落ちるなどして出ていった時の処理
    private void OnTriggerExit2D(Collider2D other)
    {
        if (other.CompareTag("Ball"))
        {
            isBallReady = false;
            ballRigidbody = null;
            currentPower = 0f;
            
            // ゲージの表示をリセット
            if (UIManager.Instance != null)
            {
                UIManager.Instance.SetPowerGauge(0f);
            }
        }
    }
}
