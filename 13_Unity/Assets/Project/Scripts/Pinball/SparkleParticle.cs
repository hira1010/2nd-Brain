using UnityEngine;

// キラキラ光るエフェクトの粒子を制御するスクリプト
public class SparkleParticle : MonoBehaviour
{
    private Vector2 velocity;
    private float fadeSpeed = 2.0f; // フェードアウト（透明になる）スピード
    private float shrinkSpeed = 1.5f; // だんだん小さくなるスピード
    private SpriteRenderer spriteRenderer;
    private Color color;

    // 粒子の初期化（飛ぶ方向、速さ、色、初期サイズを設定）
    public void Initialize(Vector2 direction, float speed, Color particleColor, float startSize = 0.3f)
    {
        velocity = direction * speed;
        color = particleColor;
        transform.localScale = new Vector3(startSize, startSize, 1f);

        spriteRenderer = GetComponent<SpriteRenderer>();
        if (spriteRenderer == null)
        {
            spriteRenderer = gameObject.AddComponent<SpriteRenderer>();
            Shader unlitShader = Shader.Find("Universal Render Pipeline/2D/Sprite-Unlit-Default") ?? 
                                 Shader.Find("Universal Render Pipeline/Unlit") ?? 
                                 Shader.Find("Sprites/Default");
            if (unlitShader != null)
            {
                spriteRenderer.material = new Material(unlitShader);
            }
            spriteRenderer.sprite = CreateMiniCircleSprite();
        }
        spriteRenderer.color = color;
        spriteRenderer.sortingOrder = 5; // ボールや盤面の手前に表示
    }

    private Sprite CreateMiniCircleSprite()
    {
        Texture2D tex = new Texture2D(16, 16);
        Color[] cols = new Color[16 * 16];
        float radius = 8f;
        for (int y = 0; y < 16; y++)
        {
            for (int x = 0; x < 16; x++)
            {
                float dx = x - 8f;
                float dy = y - 8f;
                float distSq = dx * dx + dy * dy;
                if (distSq <= radius * radius)
                {
                    float dist = Mathf.Sqrt(distSq);
                    float alpha = Mathf.Clamp01(1f - (dist / radius));
                    cols[y * 16 + x] = new Color(1f, 1f, 1f, alpha);
                }
                else
                {
                    cols[y * 16 + x] = Color.clear;
                }
            }
        }
        tex.SetPixels(cols);
        tex.Apply();
        return Sprite.Create(tex, new Rect(0, 0, 16, 16), new Vector2(0.5f, 0.5f));
    }

    void Update()
    {
        // 1. 位置を移動させます
        transform.Translate(velocity * Time.deltaTime);

        // 2. 徐々に減速させます（フワッと止まる演出）
        velocity *= 0.95f;

        // 3. サイズを小さくしていきます
        transform.localScale = Vector3.Max(Vector3.zero, transform.localScale - Vector3.one * shrinkSpeed * Time.deltaTime);

        // 4. アルファ値（透明度）を下げていきます
        if (spriteRenderer != null)
        {
            color.a = Mathf.Max(0f, color.a - fadeSpeed * Time.deltaTime);
            spriteRenderer.color = color;
        }

        // 5. 完全に透明になるか、サイズがゼロになったら自動で消滅します
        if (color.a <= 0f || transform.localScale.x <= 0f)
        {
            Destroy(gameObject);
        }
    }
}
