using UnityEngine;
using TMPro; // ポップアップ得点表示用
using DG.Tweening; // 得点の移動・フェード演出用

// ボール衝突時のエフェクト、得点ポップアップ、全画面フェイバー演出を管理するスクリプト
public class EffectManager : MonoBehaviour
{
    public static EffectManager Instance { get; private set; }

    [Header("パーティクルプレハブ（空でも自動で動的生成します）")]
    public GameObject sparkleParticlePrefab;
    public GameObject starParticlePrefab;
    public GameObject heartParticlePrefab;
    public GameObject ringParticlePrefab;

    [Header("1,000,000点時：全画面フィーバーエフェクト")]
    public GameObject fullScreenFeverEffectPrefab;

    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
        }
    }

    // 衝突時のきらびやかな演出（火花、星、ハート、リング）を発生させる
    public void PlayHitEffect(Vector2 position)
    {
        bool spawnedAny = false;
        
        // プレハブが登録されている場合はそれぞれ生成
        if (sparkleParticlePrefab != null) { Instantiate(sparkleParticlePrefab, position, Quaternion.identity); spawnedAny = true; }
        if (starParticlePrefab != null) { Instantiate(starParticlePrefab, position, Quaternion.identity); spawnedAny = true; }
        if (heartParticlePrefab != null) { Instantiate(heartParticlePrefab, position, Quaternion.identity); spawnedAny = true; }
        if (ringParticlePrefab != null) { Instantiate(ringParticlePrefab, position, Quaternion.identity); spawnedAny = true; }

        // もしプレハブがまだ登録されていなくても、プログラム制御のネオン火花を発生（フォールバック）
        if (!spawnedAny)
        {
            CreateFallbackSparkles(position);
        }
    }

    // 衝突箇所からふわっと得点が浮き上がるポップアップ表示
    public void SpawnScorePopup(Vector2 position, int score)
    {
        GameObject popupObj = new GameObject("ScorePopup");
        popupObj.transform.position = new Vector3(position.x, position.y, -1f); // 背景に埋もれないよう手前に配置
        
        // テキストコンポーネントをアタッチ
        var textMesh = popupObj.AddComponent<TextMeshPro>();
        textMesh.text = "+" + score.ToString();
        textMesh.fontSize = 5.5f;
        textMesh.color = new Color(1.0f, 0.84f, 0.0f); // ゴージャスなゴールドカラー
        textMesh.alignment = TextAlignmentOptions.Center;

        // 得点ポップアップを上に浮き上がらせる
        popupObj.transform.DOMoveY(position.y + 1.3f, 0.6f).SetEase(Ease.OutCubic);
        
        // 一瞬拡大してから滑らかに縮小させる
        popupObj.transform.DOScale(1.25f, 0.12f).OnComplete(() =>
        {
            popupObj.transform.DOScale(0.7f, 0.48f);
        });

        // アルファ値をフェードアウトさせて自然に消滅させます
        DOTween.To(() => textMesh.color, x => textMesh.color = x, new Color(textMesh.color.r, textMesh.color.g, textMesh.color.b, 0f), 0.6f)
            .OnComplete(() => Destroy(popupObj)); // 演出終了後に破棄
    }

    // 100万点突破時の全画面フィーバー演出
    public void PlayFullScreenEffect()
    {
        if (fullScreenFeverEffectPrefab != null)
        {
            GameObject effect = Instantiate(fullScreenFeverEffectPrefab, Vector3.zero, Quaternion.identity);
            Destroy(effect, 4.0f);
        }
        else
        {
            // プレハブが未登録時のフォールバック：メインカメラの背景色をサイケデリックに明滅させる
            Debug.Log("[EffectManager] 100万点達成！全画面フィーバー（フォールバック実行中）");
            Camera.main.DOColor(new Color(0.35f, 0.08f, 0.35f), 0.12f).SetLoops(8, LoopType.Yoyo)
                .OnComplete(() => Camera.main.backgroundColor = new Color(0.01f, 0.01f, 0.02f));
        }
    }

    // 動的にネオン火花を発生させるフォールバック処理（SparkleParticleを活用）
    private void CreateFallbackSparkles(Vector2 spawnPos)
    {
        int particleCount = 12;
        Color[] neonColors = new Color[]
        {
            new Color(1f, 0.08f, 0.58f), // ネオンピンク
            new Color(0f, 0.94f, 1f),    // ネオンブルー
            new Color(1f, 0.84f, 0f),    // ゴールド
            new Color(0.6f, 0.2f, 1f)     // ネオンパープル
        };

        for (int i = 0; i < particleCount; i++)
        {
            GameObject pObj = new GameObject("SparkleParticle");
            pObj.transform.position = spawnPos;

            SparkleParticle particle = pObj.AddComponent<SparkleParticle>();
            
            float angle = Random.Range(0f, 360f) * Mathf.Deg2Rad;
            Vector2 direction = new Vector2(Mathf.Cos(angle), Mathf.Sin(angle));
            
            float speed = Random.Range(3.5f, 7.0f);
            Color pColor = neonColors[Random.Range(0, neonColors.Length)];
            float size = Random.Range(0.12f, 0.3f);

            particle.Initialize(direction, speed, pColor, size);
        }
    }
}
