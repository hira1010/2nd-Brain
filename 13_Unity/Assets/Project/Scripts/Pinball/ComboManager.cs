using UnityEngine;

// 連続ヒット（コンボ）の回数と、コンボ切れまでのタイマーを制御するマネージャースクリプト
public class ComboManager : MonoBehaviour
{
    public static ComboManager Instance { get; private set; }

    [Header("コンボルール設定")]
    [Tooltip("コンボが持続する制限時間（秒）")]
    public float comboLimitTime = 3.5f;

    private int currentCombo = 0;
    private float comboTimer = 0f;

    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
        }
    }

    private void Update()
    {
        // コンボが繋がっている間はタイマーを減算
        if (currentCombo > 0)
        {
            comboTimer -= Time.deltaTime;
            if (comboTimer <= 0f)
            {
                // 時間切れでコンボ終了
                BreakCombo();
            }
        }
    }

    // 仕掛けにヒットした瞬間に呼ばれるコンボ登録処理
    public void RegisterHit()
    {
        currentCombo++;
        comboTimer = comboLimitTime; // タイマーを満タンまでリセット

        // UIを更新
        if (UIManager.Instance != null)
        {
            UIManager.Instance.UpdateCombo(currentCombo);
        }

        // 2コンボ以上で、コンボ接続時専用の小気味いいSEを鳴らす
        if (currentCombo > 1 && AudioManager.Instance != null)
        {
            AudioManager.Instance.PlayComboStretch();
        }

        // コンボ数から新しいスコア倍率を計算して設定
        int nextMultiplier = EvaluateMultiplier(currentCombo);
        if (ScoreManager.Instance != null)
        {
            ScoreManager.Instance.SetMultiplier(nextMultiplier);
        }
    }

    // コンボが途切れた際の処理
    public void BreakCombo()
    {
        currentCombo = 0;
        comboTimer = 0f;

        // UIテキストを隠す
        if (UIManager.Instance != null)
        {
            UIManager.Instance.HideCombo();
        }

        // スコア倍率を等倍（1倍）に戻す
        if (ScoreManager.Instance != null)
        {
            ScoreManager.Instance.SetMultiplier(1);
        }
    }

    // コンボ数に応じたスコア倍率の振り分けテーブル
    private int EvaluateMultiplier(int combo)
    {
        if (combo >= 20) return 6; // 20連打以上: スコア6倍
        if (combo >= 12) return 5; // 12連打以上: スコア5倍
        if (combo >= 7)  return 4; // 7連打以上 : スコア4倍
        if (combo >= 4)  return 3; // 4連打以上 : スコア3倍
        if (combo >= 2)  return 2; // 2連打以上 : スコア2倍
        return 1;
    }
}
