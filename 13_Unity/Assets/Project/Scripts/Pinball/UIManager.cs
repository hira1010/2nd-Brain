using UnityEngine;
using TMPro; // UIのテキスト表現（TextMeshPro）
using UnityEngine.UI;
using DG.Tweening; // ポップアニメーション用のDOTween

// SCORE, BALL, COMBO, 倍率 などの画面UI要素を一括更新するマネージャー
public class UIManager : MonoBehaviour
{
    public static UIManager Instance { get; private set; }

    [Header("テキストUI要素")]
    public TextMeshProUGUI scoreText;
    public TextMeshProUGUI highScoreText;
    public TextMeshProUGUI ballText;
    public TextMeshProUGUI comboText;
    public TextMeshProUGUI multiplierText;

    [Header("ゲームオーバーUI要素")]
    public GameObject gameOverPanel;
    public TextMeshProUGUI finalScoreText;
    public Button restartButton;

    [Header("発射パワーゲージUI要素")]
    public Slider powerGaugeSlider;
    public Image powerGaugeFill;

    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
        }
    }

    private void Start()
    {
        // 開始時はゲームオーバーを非表示、コンボUIを隠す
        if (gameOverPanel != null)
        {
            gameOverPanel.SetActive(false);
        }
        HideCombo();
        SetPowerGauge(0f);
    }

    // スコア表示の更新とポップ演出
    public void UpdateScore(int score, int highScore)
    {
        if (scoreText != null)
        {
            scoreText.text = "SCORE\n" + score.ToString("N0");
            
            // スコアが増えた瞬間に「ポンッ」と一瞬大きくなるアニメーション
            scoreText.transform.DOComplete();
            scoreText.transform.localScale = Vector3.one;
            scoreText.transform.DOScale(1.18f, 0.08f).SetEase(Ease.OutQuad)
                .OnComplete(() => scoreText.transform.DOScale(1f, 0.1f));
        }
        if (highScoreText != null)
        {
            highScoreText.text = "HI-SCORE\n" + highScore.ToString("N0");
        }
    }

    // ボール残数の表示更新
    public void UpdateBall(int currentBall)
    {
        if (ballText != null)
        {
            ballText.text = "BALL: " + currentBall.ToString();
        }
    }

    // コンボ表示の更新とポップ演出
    public void UpdateCombo(int combo)
    {
        if (comboText == null) return;

        if (combo > 1)
        {
            comboText.gameObject.SetActive(true);
            comboText.text = combo.ToString() + " COMBO!";
            
            // コンボが増えるたびにバウンドするような演出
            comboText.transform.DOComplete();
            comboText.transform.localScale = Vector3.one * 0.7f;
            comboText.transform.DOScale(1.25f, 0.1f).SetEase(Ease.OutBack)
                .OnComplete(() => comboText.transform.DOScale(1.0f, 0.12f));
        }
        else
        {
            HideCombo();
        }
    }

    // コンボ表示を非表示にする
    public void HideCombo()
    {
        if (comboText != null)
        {
            comboText.gameObject.SetActive(false);
        }
    }

    // 倍率（ボーナス倍率）表示の更新
    public void UpdateMultiplier(int multiplier)
    {
        if (multiplierText != null)
        {
            if (multiplier > 1)
            {
                multiplierText.gameObject.SetActive(true);
                multiplierText.text = "BONUS x" + multiplier.ToString();
                
                // 倍率表示時も小さくポップさせる
                multiplierText.transform.DOComplete();
                multiplierText.transform.localScale = Vector3.one * 0.8f;
                multiplierText.transform.DOScale(1.15f, 0.1f).SetEase(Ease.OutBack)
                    .OnComplete(() => multiplierText.transform.DOScale(1f, 0.1f));
            }
            else
            {
                multiplierText.gameObject.SetActive(false);
            }
        }
    }

    // 発射時のパワーゲージ（0.0 〜 1.0）の表示更新
    public void SetPowerGauge(float normalizedPower)
    {
        if (powerGaugeSlider != null)
        {
            powerGaugeSlider.value = normalizedPower;
            if (powerGaugeFill != null)
            {
                // パワーが溜まるにつれて、ピンクから輝くゴールドカラーへ滑らかに変化させます
                powerGaugeFill.color = Color.Lerp(new Color(1f, 0.08f, 0.58f), new Color(1f, 0.84f, 0.06f), normalizedPower);
            }
        }
    }

    // ゲームオーバー画面の表示
    public void ShowGameOver(int finalScore)
    {
        if (gameOverPanel != null)
        {
            gameOverPanel.SetActive(true);
            if (finalScoreText != null)
            {
                finalScoreText.text = "FINAL SCORE\n" + finalScore.ToString("N0");
            }
            
            // 下からふわっと浮き出てくるようなアニメーション
            gameOverPanel.transform.DOComplete();
            gameOverPanel.transform.localScale = Vector3.zero;
            gameOverPanel.transform.DOScale(1f, 0.35f).SetEase(Ease.OutBack);
        }
    }

    // ゲームオーバー画面を隠す
    public void HideGameOver()
    {
        if (gameOverPanel != null)
        {
            gameOverPanel.SetActive(false);
        }
    }
}
