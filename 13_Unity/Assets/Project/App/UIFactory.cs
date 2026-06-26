using System;
using UnityEngine;
using UnityEngine.UI;
using UnityMcpTextbook.View;

#if UNITY_EDITOR
using UnityEditor;
#endif

// ===== 設計理由 =====
// 層: Infrastructure / Factory
// 理由: GameLauncher から UI 生成の責務を分離し、コードの可読性と保守性を向上させます。
// 責務:
//   - Canvas や Image, Text などの UI 要素をコードから動的に生成する。
//   - プレハブを使わない縛りに対応するためのヘルパー。
// =========================
namespace UnityMcpTextbook.App
{
    public static class UIFactory
    {
        public static GameObject CreateGameplayCanvas(Transform parent)
        {
            var canvasObject = new GameObject("GameplayCanvas", typeof(Canvas), typeof(CanvasScaler), typeof(GraphicRaycaster));
            canvasObject.transform.SetParent(parent, false);

            ConfigureCanvas(canvasObject, 1);
            return canvasObject;
        }

        public static GameObject CreateOverlayCanvas(Transform parent, string canvasName, int sortingOrder)
        {
            var canvasObject = new GameObject(canvasName, typeof(Canvas), typeof(CanvasScaler), typeof(GraphicRaycaster));
            canvasObject.transform.SetParent(parent, false);

            ConfigureCanvas(canvasObject, sortingOrder);
            return canvasObject;
        }

        private static void ConfigureCanvas(GameObject canvasObject, int sortingOrder)
        {
            var canvas = canvasObject.GetComponent<Canvas>();
            canvas.renderMode = RenderMode.ScreenSpaceOverlay;
            canvas.sortingOrder = sortingOrder;

            var canvasScaler = canvasObject.GetComponent<CanvasScaler>();
            canvasScaler.uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
            canvasScaler.referenceResolution = new Vector2(1080f, 1920f);
            canvasScaler.matchWidthOrHeight = 1f;
        }

        public static void CreateStageBackground(Transform parent)
        {
            var imageObject = new GameObject("StageBackground", typeof(RectTransform), typeof(Image));
            imageObject.transform.SetParent(parent, false);

            var rectTransform = imageObject.GetComponent<RectTransform>();
            rectTransform.anchorMin = Vector2.zero;
            rectTransform.anchorMax = Vector2.one;
            rectTransform.offsetMin = Vector2.zero;
            rectTransform.offsetMax = Vector2.zero;

            var image = imageObject.GetComponent<Image>();
            image.sprite = LoadEditorSprite("Assets/Project/Images/Textures/stage_background.png");
            image.preserveAspect = true;
            image.raycastTarget = false;
        }

        public static Image CreateChildImage(Transform parent, string objectName, Vector2 size, Vector2 anchoredPosition, bool raycastTarget)
        {
            var imageObject = new GameObject(objectName, typeof(RectTransform), typeof(Image));
            imageObject.transform.SetParent(parent, false);

            var rectTransform = imageObject.GetComponent<RectTransform>();
            rectTransform.anchorMin = new Vector2(0.5f, 0.5f);
            rectTransform.anchorMax = new Vector2(0.5f, 0.5f);
            rectTransform.pivot = new Vector2(0.5f, 0.5f);
            rectTransform.anchoredPosition = anchoredPosition;
            rectTransform.sizeDelta = size;

            var image = imageObject.GetComponent<Image>();
            image.preserveAspect = true;
            image.raycastTarget = raycastTarget;
            return image;
        }

        public static Text CreateOverlayText(Transform parent, string objectName, Vector2 anchoredPosition, int fontSize, Color color, string initialText)
        {
            var textObject = new GameObject(objectName, typeof(RectTransform), typeof(Text));
            textObject.transform.SetParent(parent, false);

            var rectTransform = textObject.GetComponent<RectTransform>();
            rectTransform.anchorMin = new Vector2(0.5f, 1f);
            rectTransform.anchorMax = new Vector2(0.5f, 1f);
            rectTransform.pivot = new Vector2(0.5f, 1f);
            rectTransform.anchoredPosition = anchoredPosition;
            rectTransform.sizeDelta = new Vector2(600f, 150f);

            var text = textObject.GetComponent<Text>();
            text.raycastTarget = false; // テキストがクリックを遮らないようにする
            text.font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf") ?? Resources.GetBuiltinResource<Font>("Arial.ttf");
            text.alignment = TextAnchor.MiddleCenter;
            text.fontSize = fontSize;
            text.color = color;
            text.horizontalOverflow = HorizontalWrapMode.Overflow;
            text.verticalOverflow = VerticalWrapMode.Overflow;
            text.text = initialText;
            return text;
        }

        public static MoleHoleView CreateDefaultMoleHoleView(Transform parent, int index, Vector2 anchoredPosition)
        {
            var viewObject = new GameObject($"MoleHoleView_{index}", typeof(RectTransform), typeof(MoleHoleView));
            viewObject.transform.SetParent(parent, false);

            var rectTransform = viewObject.GetComponent<RectTransform>();
            rectTransform.anchorMin = new Vector2(0.5f, 0.5f);
            rectTransform.anchorMax = new Vector2(0.5f, 0.5f);
            rectTransform.pivot = new Vector2(0.5f, 0.5f);
            rectTransform.anchoredPosition = anchoredPosition;
            rectTransform.sizeDelta = new Vector2(220f, 180f);

            var holeImage = CreateChildImage(rectTransform, "HoleImage", new Vector2(220f, 155f), Vector2.zero, true);
            var moleImage = CreateChildImage(rectTransform, "MoleImage", new Vector2(180f, 160f), new Vector2(0f, 18f), true);

            var moleHoleView = viewObject.GetComponent<MoleHoleView>();
            moleHoleView.SetImageTargets(holeImage, moleImage);
            moleHoleView.SetSprites(
                LoadEditorSprite("Assets/Project/Images/Atlas/mole_idle.png"),
                LoadEditorSprite("Assets/Project/Images/Atlas/mole_appear.png"),
                LoadEditorSprite("Assets/Project/Images/Atlas/mole_hit.png"),
                LoadEditorSprite("Assets/Project/Images/Atlas/mole_escape.png"));
            moleHoleView.HideMole();
            return moleHoleView;
        }

        public static void MakeCenter(RectTransform rect)
        {
            rect.anchorMin = new Vector2(0.5f, 0.5f);
            rect.anchorMax = new Vector2(0.5f, 0.5f);
            rect.pivot = new Vector2(0.5f, 0.5f);
            rect.anchoredPosition = Vector2.zero;
        }

        public static Sprite LoadEditorSprite(string assetPath)
        {
#if UNITY_EDITOR
            var texture = AssetDatabase.LoadAssetAtPath<Texture2D>(assetPath);
            if (texture == null) return null;
            return Sprite.Create(texture, new Rect(0f, 0f, texture.width, texture.height), new Vector2(0.5f, 0.5f), 100f);
#else
            return null;
#endif
        }
    }
}
