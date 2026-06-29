using UnityEngine;
using DG.Tweening; // 高品質なアニメーションを実現するDOTweenを使用します

// バンパー衝突時などにカメラを振動（画面揺れ）させるスクリプト
public class CameraShake : MonoBehaviour
{
    public static CameraShake Instance { get; private set; }

    private Vector3 originalPos;

    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
        }
    }

    private void Start()
    {
        // 揺らした後に元の正しい位置に戻せるよう、初期位置を記録します
        originalPos = transform.position;
    }

    // 画面揺れを実行する処理
    public void Shake(float duration = 0.18f, float strength = 0.25f)
    {
        // 連続でヒットした際に前回の揺れを終わらせて初期位置からリセットします
        transform.DOComplete();
        transform.position = originalPos;

        // DOTweenのDOShakePositionを使い、カメラを瞬間的に振動させます
        // パラメータ: 期間(sec), 強さ(移動距離), 振動回数, ランダム角度, スナップ, フェードアウト
        transform.DOShakePosition(duration, new Vector3(strength, strength, 0f), 25, 90f, false, true)
            .OnComplete(() => transform.position = originalPos); // 終了後に確実に元の位置に戻す
    }
}
