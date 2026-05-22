using System;
using System.Reflection;
using UnityEditor;
using UnityEngine;

[InitializeOnLoad]
internal static class AIStarterKitGameViewSetup
{
    private const string PrefKey = "AIStarterKit.GameViewRatiosConfigured.v4";
    private const string PreferredFixedResolutionLabel = "941x1672";
    private const float PreviewZoomScale = 0.15f;

    private static readonly (string Label, int Width, int Height)[] Ratios =
    {
        ("9:16", 9, 16),
        ("10:21", 10, 21),
        ("3:4", 3, 4),
        ("9:21", 9, 21),
        ("1:1", 1, 1),
    };

    static AIStarterKitGameViewSetup()
    {
        EditorApplication.delayCall += Configure;
        EditorApplication.playModeStateChanged += HandlePlayModeStateChanged;
    }

    [MenuItem("Tools/AI Starter Kit/Set Game View Ratios")]
    private static void ConfigureFromMenu()
    {
        Configure(force: true);
    }

    private static void Configure()
    {
        Configure(force: false);
    }

    private static void Configure(bool force)
    {
        if (!force && EditorPrefs.GetBool(PrefKey, false))
        {
            return;
        }

        try
        {
            foreach (var ratio in Ratios)
            {
                EnsureGameViewSize(ratio.Label, ratio.Width, ratio.Height, "AspectRatio");
            }

            int selectedIndex = EnsureGameViewSize(PreferredFixedResolutionLabel, 941, 1672, "FixedResolution");
            SelectGameViewSize(selectedIndex);
            SetGameViewZoom(PreviewZoomScale);

            EditorPrefs.SetBool(PrefKey, true);
            Debug.Log("AI Starter Kit setup: Game View 941x1672 selected and preview zoom reset.");
        }
        catch (Exception ex)
        {
            Debug.LogWarning($"AI Starter Kit setup: failed to set Game View size. {ex.Message}");
        }
    }

    private static void HandlePlayModeStateChanged(PlayModeStateChange state)
    {
        if (state == PlayModeStateChange.EnteredEditMode)
        {
            SetGameViewZoom(PreviewZoomScale);
        }
    }

    private static int EnsureGameViewSize(string label, int width, int height, string sizeTypeName)
    {
        Assembly editorAssembly = typeof(Editor).Assembly;
        Type sizesType = editorAssembly.GetType("UnityEditor.GameViewSizes");
        Type singletonType = typeof(ScriptableSingleton<>).MakeGenericType(sizesType);
        object sizesInstance = singletonType.GetProperty("instance", BindingFlags.Public | BindingFlags.Static)?.GetValue(null, null);
        object group = sizesType.GetMethod("GetGroup")?.Invoke(sizesInstance, new object[] { (int)GameViewSizeGroupType.Standalone });
        Type groupType = group.GetType();
        MethodInfo getTotalCount = groupType.GetMethod("GetTotalCount");
        MethodInfo getGameViewSize = groupType.GetMethod("GetGameViewSize");

        int count = (int)getTotalCount.Invoke(group, null);
        for (int i = 0; i < count; i++)
        {
            object size = getGameViewSize.Invoke(group, new object[] { i });
            string displayText = size.GetType().GetProperty("displayText")?.GetValue(size, null)?.ToString() ?? string.Empty;
            if (displayText.Contains(label))
            {
                return i;
            }
        }

        Type sizeType = editorAssembly.GetType("UnityEditor.GameViewSize");
        Type gameViewSizeType = editorAssembly.GetType("UnityEditor.GameViewSizeType");
        object viewSizeType = Enum.Parse(gameViewSizeType, sizeTypeName);
        ConstructorInfo ctor = sizeType.GetConstructor(new[] { gameViewSizeType, typeof(int), typeof(int), typeof(string) });
        object newSize = ctor.Invoke(new object[] { viewSizeType, width, height, label });
        groupType.GetMethod("AddCustomSize")?.Invoke(group, new[] { newSize });
        return (int)getTotalCount.Invoke(group, null) - 1;
    }

    private static void SelectGameViewSize(int index)
    {
        Type gameViewType = typeof(Editor).Assembly.GetType("UnityEditor.GameView");
        EditorWindow gameView = EditorWindow.GetWindow(gameViewType);
        PropertyInfo selectedSizeIndex = gameViewType.GetProperty("selectedSizeIndex", BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic);
        selectedSizeIndex?.SetValue(gameView, index, null);
        gameView.Show();
        gameView.Repaint();
    }

    private static void SetGameViewZoom(float scale)
    {
        const BindingFlags BindingAttributes = BindingFlags.Instance | BindingFlags.NonPublic;
        Type gameViewType = Type.GetType("UnityEditor.GameView,UnityEditor");
        if (gameViewType == null)
        {
            return;
        }

        EditorWindow gameView = EditorWindow.GetWindow(gameViewType);
        FieldInfo zoomAreaField = gameViewType.GetField("m_ZoomArea", BindingAttributes);
        object zoomArea = zoomAreaField?.GetValue(gameView);
        FieldInfo scaleField = zoomArea?.GetType().GetField("m_Scale", BindingAttributes);
        scaleField?.SetValue(zoomArea, new Vector2(scale, scale));
        gameView.Repaint();
    }
}
