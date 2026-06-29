using UnityEngine;

// ゲーム全体の進行状況（プレイ開始、ボール紛失、ゲームオーバー、再起動）を統括管理する大元マネージャー
public class PinballGameManager : MonoBehaviour
{
    public static PinballGameManager Instance { get; private set; }

    [Header("ゲームルール設定")]
    [Tooltip("ゲームプレイ可能なボールの総数（3機制など）")]
    public int maxLives = 3;
    private int currentLives;

    [Header("プレハブ＆出現地点")]
    [Tooltip("打ち出すピンボールのプレハブ")]
    public GameObject ballPrefab;
    [Tooltip("発射台にボールが出現する場所のTransform")]
    public Transform ballSpawnPoint;

    private bool isGameOver = false;

    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
        }
    }

    private void Start()
    {
        // 初期状態としてゲームを再スタートさせて準備します
        RestartGame();
    }

    // 新しいボールをシューターレーンにスポーン（出現）させる処理
    public void SpawnNewBall()
    {
        if (isGameOver) return;

        if (ballPrefab != null && ballSpawnPoint != null)
        {
            GameObject newBall = Instantiate(ballPrefab, ballSpawnPoint.position, Quaternion.identity);
            newBall.name = "Pinball";
            
            // もしプレハブにBallControllerがついていない場合は自動追加して保護します
            if (newBall.GetComponent<BallController>() == null)
            {
                newBall.AddComponent<BallController>();
            }
        }
    }

    // ボールを下に落として失った（アウトした）時の処理
    public void BallLost()
    {
        if (isGameOver) return;

        // ボール紛失時のSEを再生
        if (AudioManager.Instance != null)
        {
            AudioManager.Instance.PlayBallLost();
        }

        currentLives--;

        // UIの残りボール数を更新
        if (UIManager.Instance != null)
        {
            UIManager.Instance.UpdateBall(currentLives);
        }

        // コンボをリセット
        if (ComboManager.Instance != null)
        {
            ComboManager.Instance.BreakCombo();
        }

        if (currentLives > 0)
        {
            // 1秒間の余韻をもたせてから、次のボールを自動スポーンさせます
            Invoke(nameof(SpawnNewBall), 1.0f);
        }
        else
        {
            TriggerGameOver();
        }
    }

    // ゲームオーバーに突入する際の処理
    private void TriggerGameOver()
    {
        isGameOver = true;

        // スコアマネージャーに最高記録のセーブをリクエスト
        if (ScoreManager.Instance != null)
        {
            ScoreManager.Instance.SaveScore();
        }

        // UIManagerを介してゲームオーバー結果パネルを表示
        if (UIManager.Instance != null)
        {
            int finalScore = ScoreManager.Instance != null ? ScoreManager.Instance.CurrentScore : 0;
            UIManager.Instance.ShowGameOver(finalScore);
        }

        Debug.Log("[GameManager] 残球数が0になり、ゲームオーバーとなりました。");
    }

    // ゲームの数値や状態をすべて初期状態にリセットして新ゲームを始める処理
    public void RestartGame()
    {
        isGameOver = false;
        currentLives = maxLives;

        // 各種数値・コンボ・UIのリセット
        if (ScoreManager.Instance != null)
        {
            ScoreManager.Instance.ResetScore();
        }
        if (ComboManager.Instance != null)
        {
            ComboManager.Instance.BreakCombo();
        }
        if (UIManager.Instance != null)
        {
            UIManager.Instance.HideGameOver();
            UIManager.Instance.UpdateBall(currentLives);
        }

        // 盤面に残っている古いボールがあれば全削除します
        GameObject[] activeBalls = GameObject.FindGameObjectsWithTag("Ball");
        foreach (var b in activeBalls)
        {
            Destroy(b);
        }

        // 初球をスポーン
        SpawnNewBall();
    }
}
