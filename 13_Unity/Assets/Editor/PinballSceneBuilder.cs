using UnityEditor;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Collections.Generic;

// 超高品質・美少女ネオンピンボールのシーンを一発で完全自動構築するエディタスクリプト
public class PinballSceneBuilder : EditorWindow
{
    private static Sprite glowDotSprite;

    // にじみ出る光（光彩）を表現するためのぼかし円スプライト
    private static Sprite GetGlowDotSprite()
    {
        if (glowDotSprite == null)
        {
            int size = 64;
            Texture2D tex = new Texture2D(size, size);
            Color[] cols = new Color[size * size];
            float center = size / 2f;
            float radius = 30f;

            for (int y = 0; y < size; y++)
            {
                for (int x = 0; x < size; x++)
                {
                    float dx = x - center;
                    float dy = y - center;
                    float dist = Mathf.Sqrt(dx * dx + dy * dy);

                    if (dist <= radius)
                    {
                        float ratio = dist / radius;
                        float alpha = Mathf.Clamp01(1f - ratio);
                        cols[y * size + x] = new Color(1f, 1f, 1f, alpha * alpha);
                    }
                    else
                    {
                        cols[y * size + x] = Color.clear;
                    }
                }
            }
            tex.SetPixels(cols);
            tex.Apply();
            glowDotSprite = Sprite.Create(tex, new Rect(0, 0, size, size), new Vector2(0.5f, 0.5f), 100f);
        }
        return glowDotSprite;
    }

    private static Material spriteMaterial;
    private static Material GetURPSpriteMaterial()
    {
        if (spriteMaterial == null)
        {
            Shader shader = Shader.Find("Universal Render Pipeline/2D/Sprite-Unlit-Default");
            if (shader == null)
            {
                shader = Shader.Find("Universal Render Pipeline/Unlit");
            }
            if (shader == null)
            {
                shader = Shader.Find("Sprites/Default");
            }
            
            spriteMaterial = new Material(shader);
            
            if (shader.name.Contains("Universal Render Pipeline/Unlit"))
            {
                spriteMaterial.SetFloat("_Blend", 1.0f);
                spriteMaterial.SetInt("_SrcBlend", (int)UnityEngine.Rendering.BlendMode.SrcAlpha);
                spriteMaterial.SetInt("_DstBlend", (int)UnityEngine.Rendering.BlendMode.OneMinusSrcAlpha);
                spriteMaterial.SetInt("_ZWrite", 0);
                spriteMaterial.EnableKeyword("_SURFACE_TYPE_TRANSPARENT");
                spriteMaterial.renderQueue = 3000;
            }
        }
        return spriteMaterial;
    }

    [MenuItem("Tools/Build Pinball Scene")]
    public static void BuildScene()
    {
        // --- 0. [自動設定] 'Ball' タグの登録 ---
        SerializedObject tagManager = new SerializedObject(AssetDatabase.LoadAllAssetsAtPath("ProjectSettings/TagManager.asset")[0]);
        SerializedProperty tagsProp = tagManager.FindProperty("tags");
        bool tagExists = false;
        for (int i = 0; i < tagsProp.arraySize; i++)
        {
            if (tagsProp.GetArrayElementAtIndex(i).stringValue.Equals("Ball"))
            {
                tagExists = true;
                break;
            }
        }
        if (!tagExists)
        {
            tagsProp.InsertArrayElementAtIndex(tagsProp.arraySize);
            tagsProp.GetArrayElementAtIndex(tagsProp.arraySize - 1).stringValue = "Ball";
            tagManager.ApplyModifiedProperties();
            Debug.Log("[自動設定] 'Ball' タグを登録しました。");
        }

        // --- 1. [お掃除] シーン内の古いオブジェクトをすべて削除 ---
        GameObject[] oldObjects = GameObject.FindObjectsByType<GameObject>(FindObjectsInactive.Include, FindObjectsSortMode.None);
        foreach (GameObject obj in oldObjects)
        {
            if (obj != null && (obj.name == "Pinball" || obj.name.Contains("Mole") || obj.name == "Canvas" || obj.name.Contains("Smash") ||
                               obj.name == "Walls" || obj.name == "LeftFlipper" || obj.name == "RightFlipper" ||
                               obj.name.StartsWith("Bumper") || obj.name.StartsWith("Slingshot") || obj.name.StartsWith("Apron") ||
                               obj.name.StartsWith("NeonSign") || obj.name.StartsWith("GuideRail") || obj.name.StartsWith("PlungerCover") ||
                               obj.name == "OutboxSensor" || obj.name == "PlungerZone" || obj.name == "BallSpawnPoint" ||
                               obj.name == "BackgroundBoard" || obj.name == "PinballGameManager" || obj.name == "EventSystem" ||
                               obj.name == "Character" || obj.name == "ScoreManager" || obj.name == "ComboManager" ||
                               obj.name == "AudioManager" || obj.name == "EffectManager" || obj.name == "LightManager" ||
                               obj.name == "CameraShake" || obj.name == "UIManager" || obj.name == "SaveManager"))
            {
                DestroyImmediate(obj);
            }
        }

        // 2. 新規シーンの作成
        var newScene = UnityEditor.SceneManagement.EditorSceneManager.NewScene(
            UnityEditor.SceneManagement.NewSceneSetup.DefaultGameObjects, 
            UnityEditor.SceneManagement.NewSceneMode.Single
        );
        
        // 重複オブジェクトの削除
        UnityEngine.SceneManagement.Scene activeScene = UnityEngine.SceneManagement.SceneManager.GetActiveScene();
        GameObject[] rootObjects = activeScene.GetRootGameObjects();
        foreach (GameObject obj in rootObjects)
        {
            if (obj.name != "Main Camera" && obj.name != "Directional Light")
            {
                DestroyImmediate(obj);
            }
        }

        // 3D見下ろしカメラの絶妙な遠近セッティング
        Camera mainCam = Camera.main;
        if (mainCam != null)
        {
            mainCam.clearFlags = CameraClearFlags.SolidColor;
            mainCam.orthographic = false; // 3Dカメラに変更
            mainCam.fieldOfView = 60f;     // 視野角を調整して盤面をフル画面に
            
            // X軸を傾けて、奥行き感のある3D見下ろしアングルにします
            mainCam.transform.position = new Vector3(0f, -0.4f, -14.5f);
            mainCam.transform.rotation = Quaternion.Euler(12f, 0f, 0f);
            mainCam.backgroundColor = new Color(0.01f, 0.01f, 0.02f);

            // カメラにCameraShakeをアタッチ
            if (mainCam.gameObject.GetComponent<CameraShake>() == null)
            {
                mainCam.gameObject.AddComponent<CameraShake>();
            }
        }

        // 3. 背景（美少女イラスト＆ネオンランプ描き込みボード）
        GameObject bgObj = new GameObject("BackgroundBoard");
        var bgRenderer = bgObj.AddComponent<SpriteRenderer>();
        bgRenderer.material = GetURPSpriteMaterial();
        bgRenderer.sortingOrder = -10;
        bgRenderer.color = new Color(0.85f, 0.85f, 0.9f, 1f); // 綺麗な発色
        bgObj.AddComponent<BackgroundLoader>();
        // 3D見下ろしでパーツが背景の裏に隠れないように、少し奥(Z=0.5)へずらして配置
        bgObj.transform.position = new Vector3(0f, 0f, 0.5f);

        // 背景プレビューロード
        string bgPath = System.IO.Path.Combine(Application.streamingAssetsPath, "background.png");
        if (System.IO.File.Exists(bgPath))
        {
            byte[] fileData = System.IO.File.ReadAllBytes(bgPath);
            Texture2D texture = new Texture2D(2, 2);
            if (texture.LoadImage(fileData))
            {
                Sprite bgSprite = Sprite.Create(texture, new Rect(0, 0, texture.width, texture.height), new Vector2(0.5f, 0.5f), 100f);
                bgRenderer.sprite = bgSprite;
                
                float targetWidth = 8.4f;
                float targetHeight = 16.0f;
                float spriteWidth = bgSprite.bounds.size.x;
                float spriteHeight = bgSprite.bounds.size.y;
                if (spriteWidth > 0 && spriteHeight > 0)
                {
                    float scaleX = targetWidth / spriteWidth;
                    float scaleY = targetHeight / spriteHeight;
                    float finalScale = Mathf.Max(scaleX, scaleY);
                    bgObj.transform.localScale = new Vector3(finalScale, finalScale, 1f);
                }
            }
        }

        // 4. 外枠ネオン壁
        Sprite neonWallSprite = CreateNeonWallSprite();
        GameObject wallsObj = new GameObject("Walls");
        
        CreateWall(wallsObj, "LeftWall", new Vector2(-4.2f, 0f), new Vector2(0.18f, 16f), neonWallSprite);
        CreateWall(wallsObj, "RightWall", new Vector2(4.2f, 0f), new Vector2(0.18f, 16f), neonWallSprite);
        CreateWall(wallsObj, "TopWall", new Vector2(0f, 8f), new Vector2(8.58f, 0.18f), neonWallSprite);

        // 5. 発射台の仕切り壁
        CreateWall(wallsObj, "PlungerWall", new Vector2(3.3f, -2.5f), new Vector2(0.14f, 11f), neonWallSprite);

        // 6. 斜めのガイドレール（上部コーナーの丸み、水色ネオン）
        Sprite cyanWallSprite = CreateColorNeonWallSprite(new Color(0f, 0.94f, 1f));
        CreateWallWithAngle(wallsObj, "GuideRail_TL", new Vector2(-3.4f, 7.2f), new Vector2(0.15f, 2.5f), 45f, cyanWallSprite);
        CreateWallWithAngle(wallsObj, "GuideRail_TR", new Vector2(2.5f, 7.2f), new Vector2(0.15f, 2.5f), -45f, cyanWallSprite);

        // 7. 物理フリッパー (ツートンカラーネオン、疑似発光アタッチ)
        GameObject leftFlipper = CreateFlipper("LeftFlipper", new Vector2(-1.5f, -5.5f), FlipperController.FlipperSide.Left);
        GameObject rightFlipper = CreateFlipper("RightFlipper", new Vector2(1.5f, -5.5f), FlipperController.FlipperSide.Right);

        // 8. 豪華5点配置の肉球バンパー (お手本と同じアーチ状配列、疑似ネオンライトアタッチ)
        Sprite bumperPink = CreateBumperSprite(new Color(1f, 0.08f, 0.58f));
        Sprite bumperCyan = CreateBumperSprite(new Color(0f, 0.94f, 1f));
        Sprite bumperGold = CreateBumperSprite(new Color(1f, 0.84f, 0f));
        
        CreateBumper("Bumper_1", new Vector2(0f, 4.3f), bumperGold, new Color(1f, 0.75f, 0f));
        CreateBumper("Bumper_2", new Vector2(-1.5f, 3.5f), bumperCyan, new Color(0f, 0.94f, 1f));
        CreateBumper("Bumper_3", new Vector2(1.5f, 3.5f), bumperPink, new Color(1f, 0.08f, 0.58f));
        CreateBumper("Bumper_4", new Vector2(-0.8f, 1.8f), bumperGold, new Color(1f, 0.75f, 0f));
        CreateBumper("Bumper_5", new Vector2(0.8f, 1.8f), bumperPink, new Color(1f, 0.08f, 0.58f));

        // 9. スリングショット (左右非対称デザイン、疑似発光付き)
        CreateSlingshot("Slingshot_Left", new Vector2(-3.1f, -3.0f), true);
        CreateSlingshot("Slingshot_Right", new Vector2(3.1f, -3.0f), false);

        // 10. 下部コーナーエプロン (ゴールド枠＆ネオンライン、肉球入り斜めカバー)
        CreateApron("Apron_Left", new Vector2(-3.3f, -6.9f), true);
        CreateApron("Apron_Right", new Vector2(3.3f, -6.9f), false);

        // 11. 装飾用ネコ耳ネオン看板 (ピンク、シアン、ゴールド)
        CreateNeonSign("NeonSign_NYA", new Vector2(0f, 5.9f), "NYA!", new Color(1f, 0.08f, 0.58f));
        CreateNeonSign("NeonSign_PLAY", new Vector2(-2.8f, 5.0f), "GO!", new Color(0f, 0.94f, 1f));
        CreateNeonSign("NeonSign_STAR", new Vector2(2.0f, 5.0f), "OK!", new Color(1f, 0.84f, 0f));

        // 12. 発射台の透明アクリルカバー (Z-Order = 4)
        GameObject coverObj = new GameObject("PlungerCover");
        // 3Dアングルで見下ろしたときにパーツと重なってチラつかないよう、Zをわずかに手前(-0.1f)に配置
        coverObj.transform.position = new Vector3(3.75f, -2.5f, -0.1f);
        var coverRenderer = coverObj.AddComponent<SpriteRenderer>();
        coverRenderer.material = GetURPSpriteMaterial();
        coverRenderer.sprite = CreatePlungerCoverSprite();
        coverRenderer.color = Color.white;
        coverRenderer.sortingOrder = 4;
        coverObj.transform.localScale = new Vector3(0.8f, 11f, 1f);

        // 13. 落下検知センサー
        GameObject outboxObj = new GameObject("OutboxSensor");
        outboxObj.transform.position = new Vector2(0f, -7.8f);
        var outboxCol = outboxObj.AddComponent<BoxCollider2D>();
        outboxCol.size = new Vector2(8.4f, 1f);
        outboxCol.isTrigger = true;
        outboxObj.AddComponent<BallReset>();

        // 14. プランジャー (発射台)
        GameObject plungerObj = new GameObject("PlungerZone");
        plungerObj.transform.position = new Vector2(3.75f, -7.5f);
        var plungerCol = plungerObj.AddComponent<BoxCollider2D>();
        plungerCol.size = new Vector2(0.7f, 1f);
        plungerCol.isTrigger = true;
        plungerObj.AddComponent<Launcher>(); // 新しいLauncherをアタッチ

        GameObject spawnPoint = new GameObject("BallSpawnPoint");
        spawnPoint.transform.position = new Vector2(3.75f, -7.2f);

        // 15. ボールプレハブの作成 (ほんのり発光するシアンのネオンボール)
        GameObject ballPrefab = CreateBallPrefab();

        // 16. ゲームマネージャーとUI関係マネージャーの作成
        GameObject gameManagerObj = new GameObject("PinballGameManager");
        var gm = gameManagerObj.AddComponent<PinballGameManager>();
        gm.ballPrefab = ballPrefab;
        gm.ballSpawnPoint = spawnPoint.transform;

        // 各種マネージャーの自動アタッチ
        var scoreMgr = gameManagerObj.AddComponent<ScoreManager>();
        var comboMgr = gameManagerObj.AddComponent<ComboManager>();
        var audioMgr = gameManagerObj.AddComponent<AudioManager>();
        var effectMgr = gameManagerObj.AddComponent<EffectManager>();
        var lightMgr = gameManagerObj.AddComponent<LightManager>();
        var uiMgr = gameManagerObj.AddComponent<UIManager>();
        gameManagerObj.AddComponent<SaveManager>();

        // CanvasUIの自動構築
        GameObject canvasObj = new GameObject("Canvas");
        Canvas canvas = canvasObj.AddComponent<Canvas>();
        canvas.renderMode = RenderMode.ScreenSpaceOverlay;
        canvasObj.AddComponent<CanvasScaler>();
        canvasObj.AddComponent<GraphicRaycaster>();

        // UIManagerへのテキスト・UIパーツの登録と作成
        uiMgr.scoreText = CreateUIText(canvasObj, "ScoreText", "SCORE\n0", 34f, TextAlignmentOptions.Left, new Vector2(140f, -80f), new Vector2(0f, 1f), new Vector2(0f, 1f));
        uiMgr.highScoreText = CreateUIText(canvasObj, "HighScoreText", "HI-SCORE\n0", 22f, TextAlignmentOptions.Center, new Vector2(0f, -80f), new Vector2(0.5f, 1f), new Vector2(0.5f, 1f));
        uiMgr.ballText = CreateUIText(canvasObj, "BallText", "BALL: 3", 34f, TextAlignmentOptions.Right, new Vector2(-140f, -80f), new Vector2(1f, 1f), new Vector2(1f, 1f));
        
        uiMgr.comboText = CreateUIText(canvasObj, "ComboText", "COMBO!", 48f, TextAlignmentOptions.Center, new Vector2(0f, 120f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
        uiMgr.comboText.color = new Color(0f, 0.94f, 1f); // 水色ネオン
        
        uiMgr.multiplierText = CreateUIText(canvasObj, "MultiplierText", "BONUS x1", 32f, TextAlignmentOptions.Center, new Vector2(0f, -180f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
        uiMgr.multiplierText.color = new Color(1f, 0.84f, 0f); // ゴールドネオン

        // パワーゲージスライダーUIの作成
        GameObject sliderObj = new GameObject("PowerSlider");
        sliderObj.transform.SetParent(canvasObj.transform);
        var sliderRect = sliderObj.AddComponent<RectTransform>();
        sliderRect.sizeDelta = new Vector2(250f, 20f);
        sliderRect.anchoredPosition = new Vector2(0f, -380f);
        sliderRect.anchorMin = new Vector2(0.5f, 0.5f);
        sliderRect.anchorMax = new Vector2(0.5f, 0.5f);
        var slider = sliderObj.AddComponent<Slider>();
        slider.interactable = false;
        slider.minValue = 0f;
        slider.maxValue = 1f;

        GameObject sliderBg = new GameObject("Background");
        sliderBg.transform.SetParent(sliderObj.transform);
        var sliderBgRect = sliderBg.AddComponent<RectTransform>();
        sliderBgRect.anchoredPosition = Vector2.zero;
        sliderBgRect.sizeDelta = Vector2.zero;
        sliderBgRect.anchorMin = Vector2.zero;
        sliderBgRect.anchorMax = Vector2.one;
        var sliderBgImg = sliderBg.AddComponent<Image>();
        sliderBgImg.color = new Color(0.18f, 0.18f, 0.2f, 0.65f);

        GameObject fillArea = new GameObject("Fill Area");
        fillArea.transform.SetParent(sliderObj.transform);
        var fillAreaRect = fillArea.AddComponent<RectTransform>();
        fillAreaRect.anchoredPosition = Vector2.zero;
        fillAreaRect.sizeDelta = Vector2.zero;
        fillAreaRect.anchorMin = Vector2.zero;
        fillAreaRect.anchorMax = Vector2.one;

        GameObject fill = new GameObject("Fill");
        fill.transform.SetParent(fillArea.transform);
        var fillRect = fill.AddComponent<RectTransform>();
        fillRect.anchoredPosition = Vector2.zero;
        fillRect.sizeDelta = Vector2.zero;
        var fillImg = fill.AddComponent<Image>();
        fillImg.color = new Color(1f, 0.08f, 0.58f); // ネオンピンク
        slider.fillRect = fillRect;

        uiMgr.powerGaugeSlider = slider;
        uiMgr.powerGaugeFill = fillImg;

        // ゲームオーバーパネルの作成
        GameObject panelObj = new GameObject("GameOverPanel");
        panelObj.transform.SetParent(canvasObj.transform);
        var panelRect = panelObj.AddComponent<RectTransform>();
        panelRect.sizeDelta = new Vector2(400f, 320f);
        panelRect.anchoredPosition = Vector2.zero;
        panelRect.anchorMin = new Vector2(0.5f, 0.5f);
        panelRect.anchorMax = new Vector2(0.5f, 0.5f);
        var panelImg = panelObj.AddComponent<Image>();
        panelImg.color = new Color(0.04f, 0.04f, 0.07f, 0.96f);
        uiMgr.gameOverPanel = panelObj;

        uiMgr.finalScoreText = CreateUIText(panelObj, "FinalScoreText", "FINAL SCORE\n0", 30f, TextAlignmentOptions.Center, new Vector2(0f, 60f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));

        GameObject btnObj = new GameObject("RestartButton");
        btnObj.transform.SetParent(panelObj.transform);
        var btnRect = btnObj.AddComponent<RectTransform>();
        btnRect.sizeDelta = new Vector2(220f, 54f);
        btnRect.anchoredPosition = new Vector2(0f, -60f);
        btnRect.anchorMin = new Vector2(0.5f, 0.5f);
        btnRect.anchorMax = new Vector2(0.5f, 0.5f);
        var btnImg = btnObj.AddComponent<Image>();
        btnImg.color = new Color(1f, 0.08f, 0.58f); // ネオンピンク

        var button = btnObj.AddComponent<Button>();
        button.targetGraphic = btnImg;
        CreateUIText(btnObj, "BtnText", "RETRY", 24f, TextAlignmentOptions.Center, Vector2.zero, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f)).color = Color.white;

        // リトライボタンにゲーム再始動メソッドを登録
        UnityEditor.Events.UnityEventTools.AddPersistentListener(button.onClick, gm.RestartGame);
        uiMgr.restartButton = button;

        if (FindFirstObjectByType<UnityEngine.EventSystems.EventSystem>() == null)
        {
            GameObject esObj = new GameObject("EventSystem");
            esObj.AddComponent<UnityEngine.EventSystems.EventSystem>();
            esObj.AddComponent<UnityEngine.EventSystems.StandaloneInputModule>();
        }

        // 17. 美少女キャラクターオブジェクトの自動組み立て
        GameObject charObj = new GameObject("Character");
        charObj.transform.position = new Vector3(0f, 0.4f, 0.22f); // 背景の手前、仕掛け(Z=0)の奥に配置
        var charCtrl = charObj.AddComponent<PinballCharacterController>();

        GameObject faceObj = new GameObject("Face");
        faceObj.transform.SetParent(charObj.transform);
        faceObj.transform.localPosition = Vector3.zero;
        var faceRenderer = faceObj.AddComponent<SpriteRenderer>();
        faceRenderer.material = GetURPSpriteMaterial();
        faceRenderer.sortingOrder = -5; // 遊具の下、背景の上にソート

        Color hairColor = new Color(1.0f, 0.08f, 0.58f); // ピンク髪
        Color eyeColor = new Color(0.95f, 0.08f, 0.18f); // 赤い目
        charCtrl.defaultFace = CreateDummyFaceSprite(hairColor, eyeColor, "default");
        charCtrl.smileFace = CreateDummyFaceSprite(hairColor, eyeColor, "smile");
        charCtrl.winkFace = CreateDummyFaceSprite(hairColor, eyeColor, "wink");
        charCtrl.faceRenderer = faceRenderer;

        GameObject tailObj = new GameObject("Tail");
        tailObj.transform.SetParent(charObj.transform);
        tailObj.transform.localPosition = new Vector3(-0.4f, -1.0f, 0.02f);
        var tailRenderer = tailObj.AddComponent<SpriteRenderer>();
        tailRenderer.material = GetURPSpriteMaterial();
        tailRenderer.sprite = CreateDummyTailSprite();
        tailRenderer.sortingOrder = -6; // キャラ本体の裏側に描画

        charCtrl.tailTransform = tailObj.transform;

        string scenePath = "Assets/Scenes/PinballScene.unity";
        UnityEditor.SceneManagement.EditorSceneManager.SaveScene(newScene, scenePath);
        Debug.Log("[成功] 美少女アニメ風超高品質ピンボールシーンの自動構築が完了しました: " + scenePath);
    }

    private static TextMeshProUGUI CreateUIText(GameObject parent, string name, string text, float size, TextAlignmentOptions alignment, Vector2 pos, Vector2 anchorMin, Vector2 anchorMax)
    {
        GameObject textObj = new GameObject(name);
        textObj.transform.SetParent(parent.transform);
        var rect = textObj.AddComponent<RectTransform>();
        rect.sizeDelta = new Vector2(450f, 120f);
        rect.anchoredPosition = pos;
        rect.anchorMin = anchorMin;
        rect.anchorMax = anchorMax;

        var t = textObj.AddComponent<TextMeshProUGUI>();
        t.text = text;
        t.fontSize = size;
        t.color = new Color(1.0f, 0.08f, 0.58f); // テーマカラーのネオンピンク
        t.alignment = alignment;
        return t;
    }

    private static Sprite CreateDummyFaceSprite(Color hairColor, Color eyeColor, string expression)
    {
        int size = 128;
        Texture2D tex = new Texture2D(size, size);
        Color[] cols = new Color[size * size];
        float cx = size / 2f;
        float cy = size / 2f;

        for (int y = 0; y < size; y++)
        {
            for (int x = 0; x < size; x++)
            {
                float dx = x - cx;
                float dy = y - cy;
                float dist = Mathf.Sqrt(dx * dx + dy * dy);

                cols[y * size + x] = Color.clear;

                // 輪郭（肌色）
                if (dist <= 48f)
                {
                    cols[y * size + x] = new Color(1f, 0.88f, 0.82f);
                }
                
                // ツインテール左右
                float dLeftHair = Mathf.Sqrt(Mathf.Pow(x - 18f, 2) + Mathf.Pow(y - 82f, 2));
                float dRightHair = Mathf.Sqrt(Mathf.Pow(x - 110f, 2) + Mathf.Pow(y - 82f, 2));
                if (dLeftHair <= 22f || dRightHair <= 22f)
                {
                    cols[y * size + x] = hairColor;
                }

                // 前髪・頭部
                if (dist <= 52f && y >= 64)
                {
                    cols[y * size + x] = hairColor;
                }

                // 猫耳（黒）
                // 左耳
                if (x >= 20 && x <= 50 && y >= 90 && y <= 120)
                {
                    float earLeft = (x - 20f);
                    float earTop = (y - 90f);
                    if (earTop <= earLeft * 1.2f)
                    {
                        cols[y * size + x] = new Color(0.12f, 0.12f, 0.14f);
                    }
                }
                // 右耳
                if (x >= 78 && x <= 108 && y >= 90 && y <= 120)
                {
                    float earRight = (108f - x);
                    float earTop = (y - 90f);
                    if (earTop <= earRight * 1.2f)
                    {
                        cols[y * size + x] = new Color(0.12f, 0.12f, 0.14f);
                    }
                }

                // 瞳の描画
                if (expression == "default")
                {
                    float dLeftEye = Mathf.Sqrt(Mathf.Pow(x - 44f, 2) + Mathf.Pow(y - 58f, 2));
                    float dRightEye = Mathf.Sqrt(Mathf.Pow(x - 84f, 2) + Mathf.Pow(y - 58f, 2));
                    if (dLeftEye <= 6f || dRightEye <= 6f) cols[y * size + x] = eyeColor;
                    if (dLeftEye <= 2.2f || dRightEye <= 2.2f) cols[y * size + x] = Color.white; // ハイライト
                }
                else if (expression == "smile")
                {
                    // にっこり目
                    if (x >= 38 && x <= 52 && Mathf.Abs(y - (56f + Mathf.Sin((x - 38f) / 14f * Mathf.PI) * 6f)) <= 2.2f) cols[y * size + x] = Color.black;
                    if (x >= 76 && x <= 90 && Mathf.Abs(y - (56f + Mathf.Sin((x - 76f) / 14f * Mathf.PI) * 6f)) <= 2.2f) cols[y * size + x] = Color.black;
                }
                else if (expression == "wink")
                {
                    // 左目は通常、右目はにっこりウインク
                    float dLeftEye = Mathf.Sqrt(Mathf.Pow(x - 44f, 2) + Mathf.Pow(y - 58f, 2));
                    if (dLeftEye <= 6f) cols[y * size + x] = eyeColor;
                    if (dLeftEye <= 2.2f) cols[y * size + x] = Color.white;

                    if (x >= 76 && x <= 90 && Mathf.Abs(y - (56f + Mathf.Sin((x - 76f) / 14f * Mathf.PI) * 6f)) <= 2.2f) cols[y * size + x] = Color.black;
                }

                // 口の描画
                if (expression == "smile" || expression == "wink")
                {
                    float dMouth = Mathf.Sqrt(Mathf.Pow(x - 64f, 2) + Mathf.Pow(y - 40f, 2));
                    if (dMouth <= 6.5f && y <= 40) cols[y * size + x] = new Color(0.9f, 0.35f, 0.35f); // 開けた口
                }
                else
                {
                    if (x >= 60 && x <= 68 && Mathf.Abs(y - (42f - Mathf.Pow(x - 64f, 2) * 0.15f)) <= 1.5f) cols[y * size + x] = Color.black; // 微笑み
                }
            }
        }
        tex.SetPixels(cols);
        tex.Apply();
        return Sprite.Create(tex, new Rect(0, 0, size, size), new Vector2(0.5f, 0.5f), 100f);
    }

    private static Sprite CreateDummyTailSprite()
    {
        int w = 64;
        int h = 128;
        Texture2D tex = new Texture2D(w, h);
        Color[] cols = new Color[w * h];
        
        for (int y = 0; y < h; y++)
        {
            for (int x = 0; x < w; x++)
            {
                cols[y * w + x] = Color.clear;
                // S字に曲がった尾
                float targetX = 32f + Mathf.Sin(y / 20f) * 12f;
                float dist = Mathf.Abs(x - targetX);
                float radius = Mathf.Lerp(12f, 4f, (float)y / h); // 先端を細く

                if (dist <= radius)
                {
                    if (y >= 105)
                    {
                        cols[y * w + x] = new Color(1f, 0.08f, 0.58f); // 尾先はピンク
                    }
                    else
                    {
                        cols[y * w + x] = new Color(0.12f, 0.12f, 0.14f); // 本体は黒
                    }
                }
            }
        }
        tex.SetPixels(cols);
        tex.Apply();
        return Sprite.Create(tex, new Rect(0, 0, w, h), new Vector2(0.5f, 0.1f), 100f);
    }

    private static void CreateWall(GameObject parent, string name, Vector2 pos, Vector2 size, Sprite wallSprite)
    {
        GameObject wall = new GameObject(name);
        wall.transform.SetParent(parent.transform);
        wall.transform.position = pos;
        var col = wall.AddComponent<BoxCollider2D>();
        col.size = size;
        var renderer = wall.AddComponent<SpriteRenderer>();
        renderer.material = GetURPSpriteMaterial();
        renderer.sprite = wallSprite;
        renderer.color = Color.white;
        wall.transform.localScale = new Vector3(size.x, size.y, 1f);
    }

    private static void CreateWallWithAngle(GameObject parent, string name, Vector2 pos, Vector2 size, float angle, Sprite wallSprite)
    {
        GameObject wall = new GameObject(name);
        wall.transform.SetParent(parent.transform);
        wall.transform.position = pos;
        wall.transform.rotation = Quaternion.Euler(0f, 0f, angle);
        var col = wall.AddComponent<BoxCollider2D>();
        col.size = size;
        var renderer = wall.AddComponent<SpriteRenderer>();
        renderer.material = GetURPSpriteMaterial();
        renderer.sprite = wallSprite;
        renderer.color = Color.white;
        wall.transform.localScale = new Vector3(size.x, size.y, 1f);
    }

    private static GameObject CreateFlipper(string name, Vector2 pos, FlipperController.FlipperSide side)
    {
        GameObject flipper = new GameObject(name);
        flipper.transform.position = pos;
        
        var rb = flipper.AddComponent<Rigidbody2D>();
        rb.bodyType = RigidbodyType2D.Dynamic;
        rb.mass = 25f;
        rb.gravityScale = 0f;
        rb.collisionDetectionMode = CollisionDetectionMode2D.Continuous;
        
        var renderer = flipper.AddComponent<SpriteRenderer>();
        renderer.material = GetURPSpriteMaterial();
        bool isLeft = (side == FlipperController.FlipperSide.Left);
        
        Color flipperColor = isLeft ? new Color(0f, 0.94f, 1f) : new Color(1f, 0.08f, 0.58f);
        renderer.sprite = CreateFlipperSprite(isLeft, flipperColor);
        renderer.color = Color.white;
        renderer.sortingOrder = 2;

        var polyCol = flipper.AddComponent<PolygonCollider2D>();
        polyCol.points = CalculateFlipperPoints(isLeft);

        var hinge = flipper.AddComponent<HingeJoint2D>();
        hinge.useLimits = true;
        
        float anchorX = isLeft ? -0.96f : 0.96f;
        hinge.anchor = new Vector2(anchorX, 0f);
        
        JointAngleLimits2D limits = new JointAngleLimits2D();
        limits.min = -28f;
        limits.max = 28f;
        hinge.limits = limits;

        var controller = flipper.AddComponent<FlipperController>();
        controller.side = side;
        controller.hitStrength = 1800f;
        controller.returnStrength = 700f;

        AddFakeNeonGlow(flipper, flipperColor, 2.5f, -1);

        return flipper;
    }

    private static void CreateBumper(string name, Vector2 pos, Sprite bSprite, Color lightColor)
    {
        GameObject bumper = new GameObject(name);
        bumper.transform.position = pos;
        var col = bumper.AddComponent<CircleCollider2D>();
        col.radius = 0.65f;

        var renderer = bumper.AddComponent<SpriteRenderer>();
        renderer.material = GetURPSpriteMaterial();
        renderer.sprite = bSprite;
        renderer.color = Color.white;
        renderer.sortingOrder = 1;
        bumper.transform.localScale = new Vector3(1.3f, 1.3f, 1f);

        var bScript = bumper.AddComponent<Bumper>();
        bScript.bounceForce = 15f;
        bScript.flashColor = new Color(1.5f, 1.5f, 1.5f);

        AddFakeNeonGlow(bumper, lightColor, 2.8f, -1);
    }

    private static void CreateSlingshot(string name, Vector2 pos, bool isLeft)
    {
        GameObject slingshot = new GameObject(name);
        slingshot.transform.position = pos;

        var renderer = slingshot.AddComponent<SpriteRenderer>();
        renderer.material = GetURPSpriteMaterial();
        Color slColor = isLeft ? new Color(0f, 0.94f, 1f) : new Color(1f, 0.08f, 0.58f);
        renderer.sprite = CreateSlingshotSprite(isLeft, slColor);
        renderer.color = Color.white;
        renderer.sortingOrder = 1;
        slingshot.transform.localScale = new Vector3(1.2f, 1.2f, 1f);

        var polyCol = slingshot.AddComponent<PolygonCollider2D>();
        Vector2[] points = new Vector2[3];
        if (isLeft)
        {
            points[0] = new Vector2(-0.44f, -0.44f);
            points[1] = new Vector2(-0.44f, 0.44f);
            points[2] = new Vector2(0.44f, -0.44f);
        }
        else
        {
            points[0] = new Vector2(0.44f, -0.44f);
            points[1] = new Vector2(0.44f, 0.44f);
            points[2] = new Vector2(-0.44f, -0.44f);
        }
        polyCol.points = points;

        var bScript = slingshot.AddComponent<Bumper>();
        bScript.bounceForce = 16f;
        bScript.scoreValue = 50;
        bScript.flashColor = new Color(1.5f, 1.5f, 1.5f);

        AddFakeNeonGlow(slingshot, slColor, 2.6f, -1);
    }

    private static void CreateApron(string name, Vector2 pos, bool isLeft)
    {
        GameObject apron = new GameObject(name);
        apron.transform.position = pos;

        var renderer = apron.AddComponent<SpriteRenderer>();
        renderer.material = GetURPSpriteMaterial();
        renderer.sprite = CreateApronSprite(isLeft);
        renderer.color = Color.white;
        renderer.sortingOrder = 1;
        apron.transform.localScale = new Vector3(1.4f, 1.4f, 1f);

        var polyCol = apron.AddComponent<PolygonCollider2D>();
        Vector2[] points = new Vector2[4];
        if (isLeft)
        {
            points[0] = new Vector2(-0.6f, -0.6f);
            points[1] = new Vector2(-0.6f, 0.6f);
            points[2] = new Vector2(0.3f, -0.2f);
            points[3] = new Vector2(0.3f, -0.6f);
        }
        else
        {
            points[0] = new Vector2(0.6f, -0.6f);
            points[1] = new Vector2(0.6f, 0.6f);
            points[2] = new Vector2(-0.3f, -0.2f);
            points[3] = new Vector2(-0.3f, -0.6f);
        }
        polyCol.points = points;

        PhysicsMaterial2D slipMat = new PhysicsMaterial2D("ApronMaterial");
        slipMat.friction = 0.01f;
        slipMat.bounciness = 0.15f;
        polyCol.sharedMaterial = slipMat;

        Color apronLight = isLeft ? new Color(0f, 0.94f, 1f) : new Color(1f, 0.08f, 0.58f);
        AddFakeNeonGlow(apron, apronLight, 2.8f, -1);
    }

    private static void CreateNeonSign(string name, Vector2 pos, string text, Color color)
    {
        GameObject sign = new GameObject(name);
        sign.transform.position = pos;

        var renderer = sign.AddComponent<SpriteRenderer>();
        renderer.material = GetURPSpriteMaterial();
        renderer.sprite = CreateNeonSignSprite(text, color);
        renderer.color = Color.white;
        renderer.sortingOrder = 1;

        AddFakeNeonGlow(sign, color, 3.2f, -1);
    }

    private static GameObject CreateBallPrefab()
    {
        GameObject ball = new GameObject("BallPrefab");
        var rb = ball.AddComponent<Rigidbody2D>();
        rb.bodyType = RigidbodyType2D.Dynamic;
        rb.collisionDetectionMode = CollisionDetectionMode2D.Continuous;
        
        PhysicsMaterial2D physMat = new PhysicsMaterial2D("BallMaterial");
        physMat.bounciness = 0.65f;
        physMat.friction = 0.01f;
        rb.sharedMaterial = physMat;
        
        var col = ball.AddComponent<CircleCollider2D>();
        col.radius = 0.28f;

        var renderer = ball.AddComponent<SpriteRenderer>();
        renderer.material = GetURPSpriteMaterial();
        renderer.sprite = CreateSoftCircleSprite();
        renderer.color = Color.white;
        renderer.sortingOrder = 3;
        ball.transform.localScale = new Vector3(1f, 1f, 1f);
        ball.tag = "Ball";

        // 動的軌跡スクリプトアタッチ
        ball.AddComponent<BallController>();

        AddFakeNeonGlow(ball, new Color(0f, 0.94f, 1f), 1.8f, -1);

        string prefabPath = "Assets/Project/Prefabs/Ball.prefab";
        System.IO.Directory.CreateDirectory("Assets/Project/Prefabs");
        GameObject prefab = PrefabUtility.SaveAsPrefabAsset(ball, prefabPath);
        DestroyImmediate(ball);
        
        return prefab;
    }

    private static void AddFakeNeonGlow(GameObject obj, Color color, float size, int sortOrder = 0)
    {
        GameObject glowObj = new GameObject("NeonGlow_" + obj.name);
        glowObj.transform.SetParent(obj.transform);
        glowObj.transform.localPosition = new Vector3(0f, 0f, 0.05f); // わずかに手前に重ねる
        glowObj.transform.localScale = new Vector3(size, size, 1f);
        
        var renderer = glowObj.AddComponent<SpriteRenderer>();
        renderer.material = GetURPSpriteMaterial();
        renderer.sprite = GetGlowDotSprite();
        renderer.color = new Color(color.r, color.g, color.b, 0.35f); // 柔らかな半透明発光
        renderer.sortingOrder = sortOrder;
    }

    private static Sprite CreateNeonWallSprite()
    {
        int width = 32;
        int height = 32;
        Texture2D tex = new Texture2D(width, height);
        Color[] cols = new Color[width * height];
        Color neonColor = new Color(1f, 0.08f, 0.58f, 1f);

        for (int y = 0; y < height; y++)
        {
            for (int x = 0; x < width; x++)
            {
                float dx = Mathf.Abs(x - 16f);
                if (dx <= 2f)
                {
                    cols[y * width + x] = Color.Lerp(Color.white, neonColor, dx / 2f);
                }
                else
                {
                    float alpha = Mathf.Clamp01(1f - (dx - 2f) / 14f);
                    cols[y * width + x] = new Color(neonColor.r, neonColor.g, neonColor.b, alpha * alpha);
                }
            }
        }
        tex.SetPixels(cols);
        tex.Apply();
        return Sprite.Create(tex, new Rect(0, 0, width, height), new Vector2(0.5f, 0.5f));
    }

    private static Sprite CreateColorNeonWallSprite(Color neonColor)
    {
        int width = 32;
        int height = 32;
        Texture2D tex = new Texture2D(width, height);
        Color[] cols = new Color[width * height];

        for (int y = 0; y < height; y++)
        {
            for (int x = 0; x < width; x++)
            {
                float dx = Mathf.Abs(x - 16f);
                if (dx <= 2f)
                {
                    cols[y * width + x] = Color.Lerp(Color.white, neonColor, dx / 2f);
                }
                else
                {
                    float alpha = Mathf.Clamp01(1f - (dx - 2f) / 14f);
                    cols[y * width + x] = new Color(neonColor.r, neonColor.g, neonColor.b, alpha * alpha);
                }
            }
        }
        tex.SetPixels(cols);
        tex.Apply();
        return Sprite.Create(tex, new Rect(0, 0, width, height), new Vector2(0.5f, 0.5f));
    }

    private static Sprite CreatePlungerCoverSprite()
    {
        int w = 64;
        int h = 128;
        Texture2D tex = new Texture2D(w, h);
        Color[] cols = new Color[w * h];
        Color coverColor = new Color(1f, 0.08f, 0.58f, 0.25f);
        Color rimColor = new Color(1f, 0.08f, 0.58f, 0.9f);

        for (int y = 0; y < h; y++)
        {
            for (int x = 0; x < w; x++)
            {
                cols[y * w + x] = Color.clear;
                float dLeft = x;
                float dRight = w - 1 - x;
                float dist = Mathf.Min(dLeft, dRight);
                
                if (dist <= 3f)
                {
                    cols[y * w + x] = rimColor;
                }
                else if (dist > 3f && dist <= 7f)
                {
                    float ratio = (dist - 3f) / 4f;
                    cols[y * w + x] = Color.Lerp(rimColor, coverColor, ratio);
                }
                else
                {
                    if (x >= 40 && x <= 46)
                    {
                        cols[y * w + x] = new Color(1f, 1f, 1f, 0.4f);
                    }
                    else
                    {
                        cols[y * w + x] = coverColor;
                    }
                }
            }
        }
        tex.SetPixels(cols);
        tex.Apply();
        return Sprite.Create(tex, new Rect(0, 0, w, h), new Vector2(0.5f, 0.5f), 100f);
    }

    private static Sprite CreateBumperSprite(Color neonColor)
    {
        int size = 128;
        Texture2D tex = new Texture2D(size, size);
        Color[] cols = new Color[size * size];
        Color goldColor = new Color(1f, 0.72f, 0.06f, 1f);
        float centerX = size / 2f;
        float centerY = size / 2f;

        for (int y = 0; y < size; y++)
        {
            for (int x = 0; x < size; x++)
            {
                float dx = x - centerX;
                float dy = y - centerY;
                float dist = Mathf.Sqrt(dx * dx + dy * dy);

                cols[y * size + x] = Color.clear;

                if (dist >= 58f && dist <= 64f)
                {
                    float borderRatio = (dist - 58f) / 6f;
                    cols[y * size + x] = Color.Lerp(goldColor, Color.white, 1.0f - Mathf.Abs(borderRatio - 0.5f) / 0.5f);
                }
                else if (dist >= 42f && dist <= 54f)
                {
                    float glow = 1.0f - Mathf.Abs(dist - 48f) / 6f;
                    cols[y * size + x] = new Color(neonColor.r, neonColor.g, neonColor.b, glow * 0.95f);
                }
                else if (dist > 54f && dist < 58f)
                {
                    float glow = 1.0f - (dist - 54f) / 4f;
                    cols[y * size + x] = new Color(neonColor.r, neonColor.g, neonColor.b, glow * 0.6f);
                }
                else if (dist < 42f)
                {
                    cols[y * size + x] = new Color(neonColor.r, neonColor.g, neonColor.b, 0.15f);
                }

                float mainDx = x - 64f;
                float mainDy = y - 52f;
                if ((mainDx * mainDx) / (18f * 18f) + (mainDy * mainDy) / (14f * 14f) <= 1.0f)
                {
                    cols[y * size + x] = Color.white;
                }

                if (Mathf.Sqrt(Mathf.Pow(x - 38f, 2) + Mathf.Pow(y - 78f, 2)) <= 7.5f) cols[y * size + x] = Color.white;
                if (Mathf.Sqrt(Mathf.Pow(x - 53f, 2) + Mathf.Pow(y - 91f, 2)) <= 8.5f) cols[y * size + x] = Color.white;
                if (Mathf.Sqrt(Mathf.Pow(x - 75f, 2) + Mathf.Pow(y - 91f, 2)) <= 8.5f) cols[y * size + x] = Color.white;
                if (Mathf.Sqrt(Mathf.Pow(x - 90f, 2) + Mathf.Pow(y - 78f, 2)) <= 7.5f) cols[y * size + x] = Color.white;
            }
        }
        tex.SetPixels(cols);
        tex.Apply();
        return Sprite.Create(tex, new Rect(0, 0, size, size), new Vector2(0.5f, 0.5f), 100f);
    }

    private static Sprite CreateFlipperSprite(bool isLeft, Color neonColor)
    {
        int width = 256;
        int height = 64;
        Texture2D tex = new Texture2D(width, height);
        Color[] cols = new Color[width * height];
        Color goldColor = new Color(1f, 0.72f, 0.06f, 1f);

        float x0 = 32f;
        float x1 = 224f;
        float r0 = 20f;
        float r1 = 6f;

        for (int y = 0; y < height; y++)
        {
            for (int x = 0; x < width; x++)
            {
                int checkX = isLeft ? x : (width - 1 - x);
                float px = (float)checkX;
                float py = (float)y;

                float d0 = Mathf.Sqrt(Mathf.Pow(px - x0, 2) + Mathf.Pow(py - 32f, 2));
                float d1 = Mathf.Sqrt(Mathf.Pow(px - x1, 2) + Mathf.Pow(py - 32f, 2));

                bool inside = false;
                float distToEdge = 999f;

                if (px < x0)
                {
                    inside = d0 <= r0;
                    distToEdge = d0 - r0;
                }
                else if (px > x1)
                {
                    inside = d1 <= r1;
                    distToEdge = d1 - r1;
                }
                else
                {
                    float t = (px - x0) / (x1 - x0);
                    float r = r0 + t * (r1 - r0);
                    float dy = Mathf.Abs(py - 32f);
                    inside = dy <= r;
                    distToEdge = dy - r;
                }

                cols[y * width + x] = Color.clear;

                if (inside)
                {
                    float absDist = Mathf.Abs(distToEdge);
                    if (absDist <= 2.5f)
                    {
                        cols[y * width + x] = goldColor;
                    }
                    else if (absDist > 2.5f && absDist <= 7f)
                    {
                        cols[y * width + x] = Color.Lerp(Color.white, neonColor, (7f - absDist) / 4.5f);
                    }
                    else
                    {
                        float innerRatio = (py - 32f) / r0;
                        if (innerRatio > 0.4f && innerRatio < 0.65f)
                        {
                            cols[y * width + x] = Color.white;
                        }
                        else
                        {
                            cols[y * width + x] = neonColor;
                        }
                    }
                }
                else
                {
                    if (distToEdge <= 10f)
                    {
                        float alpha = Mathf.Clamp01(1f - distToEdge / 10f);
                        cols[y * width + x] = new Color(neonColor.r, neonColor.g, neonColor.b, alpha * alpha * 0.85f);
                    }
                }
            }
        }
        tex.SetPixels(cols);
        tex.Apply();
        return Sprite.Create(tex, new Rect(0, 0, width, height), new Vector2(0.5f, 0.5f), 100f);
    }

    private static Vector2[] CalculateFlipperPoints(bool isLeft)
    {
        List<Vector2> pts = new List<Vector2>();
        int segments = 12;
        float r0 = 0.20f;
        float r1 = 0.06f;
        float leftX = -1.28f + 0.32f;
        float rightX = 1.28f - 0.32f;

        if (isLeft)
        {
            for (int i = 0; i <= segments; i++)
            {
                float angle = Mathf.Lerp(90f, 270f, (float)i / segments) * Mathf.Deg2Rad;
                pts.Add(new Vector2(leftX + Mathf.Cos(angle) * r0, Mathf.Sin(angle) * r0));
            }
            for (int i = 0; i <= segments; i++)
            {
                float angle = Mathf.Lerp(270f, 450f, (float)i / segments) * Mathf.Deg2Rad;
                pts.Add(new Vector2(rightX + Mathf.Cos(angle) * r1, Mathf.Sin(angle) * r1));
            }
        }
        else
        {
            for (int i = 0; i <= segments; i++)
            {
                float angle = Mathf.Lerp(90f, 270f, (float)i / segments) * Mathf.Deg2Rad;
                pts.Add(new Vector2(leftX + Mathf.Cos(angle) * r1, Mathf.Sin(angle) * r1));
            }
            for (int i = 0; i <= segments; i++)
            {
                float angle = Mathf.Lerp(270f, 450f, (float)i / segments) * Mathf.Deg2Rad;
                pts.Add(new Vector2(rightX + Mathf.Cos(angle) * r0, Mathf.Sin(angle) * r0));
            }
        }
        return pts.ToArray();
    }

    private static Sprite CreateSlingshotSprite(bool isLeft, Color neonColor)
    {
        int size = 128;
        Texture2D tex = new Texture2D(size, size);
        Color[] cols = new Color[size * size];
        Color goldColor = new Color(1f, 0.72f, 0.06f, 1f);

        for (int y = 0; y < size; y++)
        {
            for (int x = 0; x < size; x++)
            {
                int checkX = isLeft ? x : (size - 1 - x);
                float px = (float)checkX;
                float py = (float)y;

                bool inside = false;
                float distToEdge = 999f;

                if (px >= 20f && py >= 20f && (px - 20f) + (py - 20f) <= 88f)
                {
                    inside = true;
                    float distLeft = px - 20f;
                    float distBottom = py - 20f;
                    float distHypot = Mathf.Abs(px + py - 128f) / 1.414f;
                    distToEdge = Mathf.Min(distLeft, Mathf.Min(distBottom, distHypot));
                }
                else
                {
                    float distLeft = 20f - px;
                    float distBottom = 20f - py;
                    float distHypot = (px + py - 128f) / 1.414f;

                    if (px < 20f && py >= 20f && py <= 108f) distToEdge = distLeft;
                    else if (py < 20f && px >= 20f && px <= 108f) distToEdge = distBottom;
                    else if (px + py > 128f && px >= 20f && py >= 20f) distToEdge = distHypot;
                    else
                    {
                        float dVert1 = Mathf.Sqrt(Mathf.Pow(px - 20f, 2) + Mathf.Pow(py - 20f, 2));
                        float dVert2 = Mathf.Sqrt(Mathf.Pow(px - 20f, 2) + Mathf.Pow(py - 108f, 2));
                        float dVert3 = Mathf.Sqrt(Mathf.Pow(px - 108f, 2) + Mathf.Pow(py - 20f, 2));
                        distToEdge = Mathf.Min(dVert1, Mathf.Min(dVert2, dVert3));
                    }
                }

                cols[y * size + x] = Color.clear;

                if (inside)
                {
                    if (distToEdge <= 2.5f)
                    {
                        cols[y * size + x] = goldColor;
                    }
                    else if (distToEdge > 2.5f && distToEdge <= 8f)
                    {
                        float mid = distToEdge - 5.5f;
                        float light = Mathf.Clamp01(1f - Mathf.Abs(mid) / 2.5f);
                        cols[y * size + x] = Color.Lerp(neonColor, Color.white, light);
                    }
                    else
                    {
                        cols[y * size + x] = new Color(neonColor.r, neonColor.g, neonColor.b, 0.2f);
                    }
                }
                else
                {
                    if (distToEdge <= 9f)
                    {
                        float alpha = Mathf.Clamp01(1f - distToEdge / 9f);
                        cols[y * size + x] = new Color(neonColor.r, neonColor.g, neonColor.b, alpha * alpha * 0.75f);
                    }
                }
            }
        }
        tex.SetPixels(cols);
        tex.Apply();
        return Sprite.Create(tex, new Rect(0, 0, size, size), new Vector2(0.5f, 0.5f), 100f);
    }

    private static Sprite CreateApronSprite(bool isLeft)
    {
        int size = 128;
        Texture2D tex = new Texture2D(size, size);
        Color[] cols = new Color[size * size];
        Color goldColor = new Color(1f, 0.72f, 0.06f, 1f);
        Color neonPink = new Color(1f, 0.08f, 0.58f, 1f);

        for (int y = 0; y < size; y++)
        {
            for (int x = 0; x < size; x++)
            {
                int checkX = isLeft ? x : (size - 1 - x);
                float px = (float)checkX;
                float py = (float)y;

                bool inside = false;
                float distToEdge = 999f;

                if (px >= 20f && py >= 20f && px <= 108f)
                {
                    float slopeLimit = 108f - (px - 20f) * 0.55f;
                    if (py <= slopeLimit)
                    {
                        inside = true;
                        float dLeft = px - 20f;
                        float dBottom = py - 20f;
                        float dRight = 108f - px;
                        float dSlope = Mathf.Abs(0.55f * px + py - 119f) / Mathf.Sqrt(1f + 0.55f * 0.55f);
                        distToEdge = Mathf.Min(dLeft, Mathf.Min(dBottom, Mathf.Min(dRight, dSlope)));
                    }
                }

                cols[y * size + x] = Color.clear;

                if (inside)
                {
                    if (distToEdge <= 3f)
                    {
                        cols[y * size + x] = goldColor;
                    }
                    else if (distToEdge > 3f && distToEdge <= 8f)
                    {
                        cols[y * size + x] = Color.Lerp(Color.white, neonPink, (8f - distToEdge) / 5f);
                    }
                    else
                    {
                        cols[y * size + x] = new Color(neonPink.r, neonPink.g, neonPink.b, 0.25f);
                        
                        float pawX = isLeft ? 52f : 76f;
                        float pawY = 45f;
                        float dPaw = Mathf.Sqrt(Mathf.Pow(px - pawX, 2) + Mathf.Pow(py - pawY, 2));
                        
                        if (dPaw <= 9f) cols[y * size + x] = Color.white;
                        if (Mathf.Sqrt(Mathf.Pow(px - (pawX-11f), 2) + Mathf.Pow(py - (pawY+9f), 2)) <= 3.5f) cols[y * size + x] = Color.white;
                        if (Mathf.Sqrt(Mathf.Pow(px - (pawX-4f), 2) + Mathf.Pow(py - (pawY+15f), 2)) <= 4.5f) cols[y * size + x] = Color.white;
                        if (Mathf.Sqrt(Mathf.Pow(px - (pawX+8f), 2) + Mathf.Pow(py - (pawY+15f), 2)) <= 4.5f) cols[y * size + x] = Color.white;
                        if (Mathf.Sqrt(Mathf.Pow(px - (pawX+14f), 2) + Mathf.Pow(py - (pawY+9f), 2)) <= 3.5f) cols[y * size + x] = Color.white;
                    }
                }
                else
                {
                    if (distToEdge <= 8f)
                    {
                        float alpha = Mathf.Clamp01(1f - distToEdge / 8f);
                        cols[y * size + x] = new Color(neonPink.r, neonPink.g, neonPink.b, alpha * alpha * 0.7f);
                    }
                }
            }
        }
        tex.SetPixels(cols);
        tex.Apply();
        return Sprite.Create(tex, new Rect(0, 0, size, size), new Vector2(0.5f, 0.5f), 100f);
    }

    private static Sprite CreateNeonSignSprite(string text, Color neonColor)
    {
        int width = 160;
        int height = 80;
        Texture2D tex = new Texture2D(width, height);
        Color[] cols = new Color[width * height];
        Color goldColor = new Color(1f, 0.72f, 0.06f, 1f);

        for (int y = 0; y < height; y++)
        {
            for (int x = 0; x < width; x++)
            {
                float px = (float)x;
                float py = (float)y;

                bool isFrame = false;
                bool isGoldBorder = false;
                float dist = 999f;

                if (px >= 18f && px <= 142f && py >= 14f && py <= 52f)
                {
                    float dLeft = px - 18f;
                    float dRight = 142f - px;
                    float dBottom = py - 14f;
                    float dTop = 52f - py;
                    dist = Mathf.Min(dLeft, Mathf.Min(dRight, Mathf.Min(dBottom, dTop)));
                    
                    if (dist <= 1.5f) isGoldBorder = true;
                    else if (dist > 1.5f && dist <= 4f) isFrame = true;
                }
                
                if (px >= 18f && px <= 58f && py >= 52f)
                {
                    float lx = px - 18f;
                    float ly = py - 52f;
                    if (ly <= lx * 0.9f && ly <= (40f - lx) * 0.9f)
                    {
                        float d1 = Mathf.Abs(lx * 0.9f - ly) / 1.34f;
                        float d2 = Mathf.Abs((40f - lx) * 0.9f - ly) / 1.34f;
                        float dEar = Mathf.Min(d1, d2);
                        if (dEar <= 1.5f) isGoldBorder = true;
                        else if (dEar > 1.5f && dEar <= 4f) isFrame = true;
                        dist = dEar;
                    }
                }
                if (px >= 102f && px <= 142f && py >= 52f)
                {
                    float lx = px - 102f;
                    float ly = py - 52f;
                    if (ly <= lx * 0.9f && ly <= (40f - lx) * 0.9f)
                    {
                        float d1 = Mathf.Abs(lx * 0.9f - ly) / 1.34f;
                        float d2 = Mathf.Abs((40f - lx) * 0.9f - ly) / 1.34f;
                        float dEar = Mathf.Min(d1, d2);
                        if (dEar <= 1.5f) isGoldBorder = true;
                        else if (dEar > 1.5f && dEar <= 4f) isFrame = true;
                        dist = dEar;
                    }
                }

                cols[y * width + x] = Color.clear;

                if (isGoldBorder)
                {
                    cols[y * width + x] = goldColor;
                }
                else if (isFrame)
                {
                    cols[y * width + x] = Color.white;
                }
                else if (dist <= 12f)
                {
                    float alpha = Mathf.Clamp01(1f - dist / 12f);
                    cols[y * width + x] = new Color(neonColor.r, neonColor.g, neonColor.b, alpha * alpha * 0.85f);
                }

                float starDx = px - 80f;
                float starDy = py - 33f;
                float starDist = Mathf.Sqrt(starDx*starDx + starDy*starDy);

                if (text == "NYA!")
                {
                    if (px >= 48f && px <= 52f && py >= 22f && py <= 44f) cols[y * width + x] = Color.white;
                    if (px >= 64f && px <= 68f && py >= 22f && py <= 44f) cols[y * width + x] = Color.white;
                    float nRatio = (px - 48f) / 16f;
                    if (px >= 48f && px <= 64f && Mathf.Abs(py - (44f - nRatio * 22f)) <= 2.5f) cols[y * width + x] = Color.white;
                    
                    if (px >= 72f && px <= 88f && py >= 33f && py <= 44f) {
                        float yRatio = Mathf.Abs(px - 80f) / 8f;
                        if (Mathf.Abs(py - (33f + yRatio * 11f)) <= 2.5f) cols[y * width + x] = Color.white;
                    }
                    if (px >= 78f && px <= 82f && py >= 22f && py <= 33f) cols[y * width + x] = Color.white;

                    if (px >= 92f && px <= 108f && py >= 22f && py <= 44f) {
                        float aRatio = Mathf.Abs(px - 100f) / 8f;
                        if (py >= 22f && Mathf.Abs(py - (44f - aRatio * 22f)) <= 2.5f) cols[y * width + x] = Color.white;
                    }
                    if (px >= 96f && px <= 104f && Mathf.Abs(py - 31f) <= 2.0f) cols[y * width + x] = Color.white;

                    if (px >= 111f && px <= 114f && py >= 28f && py <= 44f) cols[y * width + x] = Color.white;
                    if (px >= 111f && px <= 114f && py >= 22f && py <= 25f) cols[y * width + x] = Color.white;
                }
                else if (text == "GO!")
                {
                    if (px >= 50f && px <= 66f && py >= 22f && py <= 44f) {
                        float dL = px - 50f;
                        float dT = 44f - py;
                        float dB = py - 22f;
                        if (dL <= 3f || dT <= 3f || dB <= 3f) cols[y * width + x] = Color.white;
                        if (px >= 58f && py >= 30f && py <= 33f) cols[y * width + x] = Color.white;
                        if (px >= 63f && py >= 22f && py <= 33f) cols[y * width + x] = Color.white;
                    }
                    if (px >= 72f && px <= 88f && py >= 22f && py <= 44f) {
                        float dL = px - 72f;
                        float dR = 88f - px;
                        float dT = 44f - py;
                        float dB = py - 22f;
                        if (dL <= 3f || dR <= 3f || dT <= 3f || dB <= 3f) cols[y * width + x] = Color.white;
                    }
                    if (px >= 94f && px <= 97f && py >= 28f && py <= 44f) cols[y * width + x] = Color.white;
                    if (px >= 94f && px <= 97f && py >= 22f && py <= 25f) cols[y * width + x] = Color.white;
                }
                else
                {
                    if (px >= 50f && px <= 66f && py >= 22f && py <= 44f) {
                        float dL = px - 50f;
                        float dR = 66f - px;
                        float dT = 44f - py;
                        float dB = py - 22f;
                        if (dL <= 3f || dR <= 3f || dT <= 3f || dB <= 3f) cols[y * width + x] = Color.white;
                    }
                    if (px >= 72f && px <= 75f && py >= 22f && py <= 44f) cols[y * width + x] = Color.white;
                    float kRatio = (py - 33f) / 11f;
                    if (px >= 75f && px <= 88f) {
                        if (Mathf.Abs((px - 75f) / 13f - Mathf.Abs(kRatio)) <= 0.2f) cols[y * width + x] = Color.white;
                    }
                    if (px >= 94f && px <= 97f && py >= 28f && py <= 44f) cols[y * width + x] = Color.white;
                    if (px >= 94f && px <= 97f && py >= 22f && py <= 25f) cols[y * width + x] = Color.white;
                }
            }
        }
        tex.SetPixels(cols);
        tex.Apply();
        return Sprite.Create(tex, new Rect(0, 0, width, height), new Vector2(0.5f, 0.5f), 100f);
    }

    private static Sprite CreateSoftCircleSprite()
    {
        int size = 64;
        Texture2D tex = new Texture2D(size, size);
        Color[] cols = new Color[size * size];
        float center = size / 2f;
        float radius = 26f;
        Color neonCyan = new Color(0f, 0.94f, 1f, 1f);

        for (int y = 0; y < size; y++)
        {
            for (int x = 0; x < size; x++)
            {
                float dx = x - center;
                float dy = y - center;
                float dist = Mathf.Sqrt(dx * dx + dy * dy);

                cols[y * size + x] = Color.clear;

                if (dist <= radius)
                {
                    float ratio = dist / radius;
                    float alpha = Mathf.Clamp01(1f - ratio);
                    Color ballColor = Color.Lerp(Color.white, neonCyan, ratio);
                    cols[y * size + x] = new Color(ballColor.r, ballColor.g, ballColor.b, alpha);
                }
                else if (dist > radius && dist <= radius + 6f)
                {
                    float outRatio = (dist - radius) / 6f;
                    float alpha = Mathf.Clamp01(1f - outRatio) * 0.4f;
                    cols[y * size + x] = new Color(neonCyan.r, neonCyan.g, neonCyan.b, alpha * alpha);
                }
            }
        }
        tex.SetPixels(cols);
        tex.Apply();
        return Sprite.Create(tex, new Rect(0, 0, size, size), new Vector2(0.5f, 0.5f), 100f);
    }
}
