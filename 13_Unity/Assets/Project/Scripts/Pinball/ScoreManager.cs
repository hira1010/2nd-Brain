using UnityEngine;

// 現在のスコア、ハイスコア、得点倍率を管理し、一定スコアに達した時のキャラクター演出との連携を行うスクリプト
public class ScoreManager : MonoBehaviour
{
    public static ScoreManager Instance { get; private set; }

    public int CurrentScore { get; private set; }
    public int HighScore { get; private set; }
    public int Multiplier { get; private set; } = 1;

    // 重複して何度も演出が走らないようにするための「突破済み」フラグ
    private bool is100kCleared = false;
    private bool is300kCleared = false;
    private bool is500kCleared = false;
    private bool is1MCleared = false;

    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
        }
    }

    private void Start()
    {
        ResetScore();
        // セーブマネージャーから保存されている過去の最高スコアをロード
        HighScore = SaveManager.LoadHighScore();
        UpdateUI();
    }

    // ゲーム開始時やリトライ時にスコアをリセットする処理
    public void ResetScore()
    {
        CurrentScore = 0;
        Multiplier = 1;
        is100kCleared = false;
        is300kCleared = false;
        is500kCleared = false;
        is1MCleared = false;
        UpdateUI();
    }

    // 得点を獲得した時の処理（仕掛けヒット時に呼ばれます）
    public void AddScore(int basePoints)
    {
        // 獲得点数 ＝ 基本点 × 現在のスコア倍率
        int finalAdd = basePoints * Multiplier;
        CurrentScore += finalAdd;

        // ハイスコアをリアルタイムで追い抜いた場合の処理
        if (CurrentScore > HighScore)
        {
            HighScore = CurrentScore;
        }

        UpdateUI();
        
        // 得点マイルストーンのチェック
        CheckScoreMilestones();
    }

    // 倍率（コンボ等と連動）をセットする処理
    public void SetMultiplier(int mult)
    {
        Multiplier = Mathf.Max(1, mult);
        if (UIManager.Instance != null)
        {
            UIManager.Instance.UpdateMultiplier(Multiplier);
        }
    }

    private void UpdateUI()
    {
        if (UIManager.Instance != null)
        {
            UIManager.Instance.UpdateScore(CurrentScore, HighScore);
        }
    }

    // スコアの節目ごとのイベントチェック処理
    private void CheckScoreMilestones()
    {
        // 100,000点突破 ＝ 笑顔
        if (CurrentScore >= 100000 && !is100kCleared)
        {
            is100kCleared = true;
            TriggerMilestone(0);
        }
        // 300,000点突破 ＝ ウインク
        if (CurrentScore >= 300000 && !is300kCleared)
        {
            is300kCleared = true;
            TriggerMilestone(1);
        }
        // 500,000点突破 ＝ 笑顔 ＋ ピョンジャンプ
        if (CurrentScore >= 500000 && !is500kCleared)
        {
            is500kCleared = true;
            TriggerMilestone(2);
        }
        // 1,000,000点突破 ＝ ジャンプ ＋ 全画面フィーバーエフェクト
        if (CurrentScore >= 1000000 && !is1MCleared)
        {
            is1MCleared = true;
            TriggerMilestone(3);
        }
    }

    // 節目に応じた演出の実行
    private void TriggerMilestone(int stageIndex)
    {
        // 節目共通のハッピーサウンドを鳴らします
        if (AudioManager.Instance != null)
        {
            AudioManager.Instance.PlayScoreBonus();
        }

        switch (stageIndex)
        {
            case 0: // 10万点突破
                if (PinballCharacterController.Instance != null)
                {
                    PinballCharacterController.Instance.TriggerSmile(3.0f); // 笑顔にさせる
                }
                break;

            case 1: // 30万点突破
                if (PinballCharacterController.Instance != null)
                {
                    PinballCharacterController.Instance.TriggerWink(1.8f); // ウインクさせる
                }
                break;

            case 2: // 50万点突破
                if (PinballCharacterController.Instance != null)
                {
                    PinballCharacterController.Instance.TriggerSmile(3.5f);
                    PinballCharacterController.Instance.Jump(); // 嬉しくてジャンプさせる
                }
                break;

            case 3: // 100万点突破
                if (PinballCharacterController.Instance != null)
                {
                    PinballCharacterController.Instance.TriggerSmile(5.0f);
                    PinballCharacterController.Instance.Jump();
                }
                if (EffectManager.Instance != null)
                {
                    EffectManager.Instance.PlayFullScreenEffect(); // 画面全体が輝く演出
                }
                if (AudioManager.Instance != null)
                {
                    AudioManager.Instance.PlayFullScreen(); // フィーバー専用SE
                }
                break;
        }
    }

    // ゲームオーバー時に現在の最高記録をファイルに保存する処理
    public void SaveScore()
    {
        SaveManager.SaveHighScore(HighScore);
    }
}
