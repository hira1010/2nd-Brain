using System.IO;
using UnityEngine;

// 差し替え可能な背景画像をゲーム起動時に自動で読み込むスクリプト
public class BackgroundLoader : MonoBehaviour
{
    private SpriteRenderer spriteRenderer;

    void Awake()
    {
        spriteRenderer = GetComponent<SpriteRenderer>();
        LoadBackground();
    }

    // 指定フォルダから背景画像を読み込んで適用する処理
    public void LoadBackground()
    {
        string path = Path.Combine(Application.streamingAssetsPath, "background.png");
        if (File.Exists(path))
        {
            byte[] fileData = File.ReadAllBytes(path);
            Texture2D texture = new Texture2D(2, 2);
            if (texture.LoadImage(fileData))
            {
                // 画像データからスプライトを生成し、背景ボードにセットします
                Sprite newSprite = Sprite.Create(texture, new Rect(0, 0, texture.width, texture.height), new Vector2(0.5f, 0.5f), 100f);
                if (spriteRenderer != null)
                {
                    spriteRenderer.sprite = newSprite;
                    
                    // ピンボール台のサイズ（幅: 8.4ユニット, 高さ: 16.0ユニット）
                    float targetWidth = 8.4f;
                    float targetHeight = 16.0f;
                    
                    float spriteWidth = newSprite.bounds.size.x;
                    float spriteHeight = newSprite.bounds.size.y;
                    
                    if (spriteWidth > 0 && spriteHeight > 0)
                    {
                        // 縦横比（アスペクト比）を崩さずに、台を覆うようにスケールを計算します
                        float scaleX = targetWidth / spriteWidth;
                        float scaleY = targetHeight / spriteHeight;
                        
                        // 隙間ができないように大きい方の倍率を採用（切り抜きフィット）します
                        float finalScale = Mathf.Max(scaleX, scaleY);
                        transform.localScale = new Vector3(finalScale, finalScale, 1f);
                    }
                }
            }
            else
            {
                Debug.LogError("背景画像のデコードに失敗しました。");
            }
        }
        else
        {
            Debug.LogError("背景画像ファイルが見つかりません: " + path);
        }
    }
}
