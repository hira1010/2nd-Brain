using UnityEngine;

// フリッパーの下にボールが落ちたことを検知し、ライフを減らしてリセットするスクリプト
public class BallReset : MonoBehaviour
{
    private PinballGameManager gameManager;

    void Start()
    {
        // シーンからゲームマネージャーを見つけます
        gameManager = FindFirstObjectByType<PinballGameManager>();
    }

    // トリガーコライダーにボールが進入した時の処理
    void OnTriggerEnter2D(Collider2D other)
    {
        // ボールタグのオブジェクトが触れた場合のみ動作します
        if (other.CompareTag("Ball"))
        {
            // 落ちたボールオブジェクトを破壊（消去）します
            Destroy(other.gameObject);
            
            // ゲームマネージャーにボールを失ったことを通知します
            if (gameManager != null)
            {
                gameManager.BallLost();
            }
            else
            {
                Debug.LogWarning("ゲームマネージャーが見つかりません。ボールをリセットできません。");
            }
        }
    }
}
