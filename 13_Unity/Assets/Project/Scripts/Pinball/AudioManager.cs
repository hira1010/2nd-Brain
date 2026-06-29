using UnityEngine;

// ゲーム内のBGMや効果音を一括管理・再生するシングルトンマネージャー
public class AudioManager : MonoBehaviour
{
    public static AudioManager Instance { get; private set; }

    [Header("BGM設定")]
    [Tooltip("ゲーム中に流れるメインBGM")]
    public AudioClip mainBGM;

    [Header("効果音(SE)設定 - 物理仕掛け")]
    public AudioClip bumperHitSE;
    public AudioClip flipperMoveSE;
    public AudioClip launcherLaunchSE;
    public AudioClip ballLostSE;

    [Header("効果音(SE)設定 - 特殊演出")]
    public AudioClip comboStretchSE;
    public AudioClip scoreBonusSE;
    public AudioClip winExpSE;
    public AudioClip fullScreenSE;

    private AudioSource bgmSource;
    private AudioSource seSource;

    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
            
            // シーンをまたいでも効果音が途切れないようにします
            if (transform.parent == null)
            {
                DontDestroyOnLoad(gameObject);
            }
            
            // BGM用とSE用のスピーカー（AudioSource）を自動追加
            bgmSource = gameObject.AddComponent<AudioSource>();
            bgmSource.loop = true;
            bgmSource.volume = 0.35f;

            seSource = gameObject.AddComponent<AudioSource>();
            seSource.volume = 0.7f;
        }
        else
        {
            Destroy(gameObject);
        }
    }

    private void Start()
    {
        PlayBGM();
    }

    // BGMを再生する処理
    public void PlayBGM()
    {
        if (mainBGM != null && bgmSource != null)
        {
            bgmSource.clip = mainBGM;
            bgmSource.Play();
        }
    }

    // 任意の効果音を再生する汎用処理
    public void PlaySE(AudioClip clip, float volumeScale = 1.0f)
    {
        if (clip != null && seSource != null)
        {
            seSource.PlayOneShot(clip, volumeScale);
        }
    }

    // 各アクションごとのショートカットSE再生メソッド
    public void PlayBumperHit() => PlaySE(bumperHitSE, 0.9f);
    public void PlayFlipperMove() => PlaySE(flipperMoveSE, 0.35f);
    public void PlayLauncherLaunch() => PlaySE(launcherLaunchSE, 0.8f);
    public void PlayBallLost() => PlaySE(ballLostSE, 0.9f);
    public void PlayComboStretch() => PlaySE(comboStretchSE, 0.85f);
    public void PlayScoreBonus() => PlaySE(scoreBonusSE, 0.85f);
    public void PlayWinExp() => PlaySE(winExpSE, 0.9f);
    public void PlayFullScreen() => PlaySE(fullScreenSE, 1.0f);
}
