using UnityEngine;

// スペースキーの長押しでバネを引っぱり、離してボールを打ち出すプランジャー（発射台）スクリプト
public class Plunger : MonoBehaviour
{
    [Tooltip("最大打ち出しパワー")]
    public float maxForce = 30f;

    [Tooltip("パワーが溜まる速度")]
    public float chargeSpeed = 15f;

    private float currentForce = 0f;
    private bool isBallInPlunger = false;
    private Rigidbody2D ballRigidbody;

    void Update()
    {
        // ボールが発射エリア内に準備できている場合のみ入力を受け付けます
        if (isBallInPlunger && ballRigidbody != null)
        {
            if (Input.GetKey(KeyCode.Space))
            {
                // スペースキーを押し続けている間、ゲージを溜めます
                currentForce = Mathf.MoveTowards(currentForce, maxForce, chargeSpeed * Time.deltaTime);
            }
            
            if (Input.GetKeyUp(KeyCode.Space))
            {
                // キーを離した瞬間に上方向（Vector2.up）へ衝撃を与えます
                ballRigidbody.AddForce(Vector2.up * currentForce, ForceMode2D.Impulse);
                currentForce = 0f;
                isBallInPlunger = false;
                ballRigidbody = null;
            }
        }
    }

    // ボールが発射ゾーンに触れたら検知します（トリガー判定）
    void OnTriggerEnter2D(Collider2D other)
    {
        if (other.CompareTag("Ball"))
        {
            ballRigidbody = other.GetComponent<Rigidbody2D>();
            if (ballRigidbody != null)
            {
                isBallInPlunger = true;
            }
        }
    }

    // ボールが発射ゾーンから出ていった場合の処理
    void OnTriggerExit2D(Collider2D other)
    {
        if (other.CompareTag("Ball"))
        {
            isBallInPlunger = false;
            ballRigidbody = null;
            currentForce = 0f;
        }
    }
}
