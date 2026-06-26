using io.github.hatayama.uLoopMCP;
using UnityEditor;

/// <summary>
/// Keeps Unity CLI Loop available for the AI-driven verification loop.
/// </summary>
[InitializeOnLoad]
internal static class AIStarterKitUnityCliLoopAutoStart
{
    static AIStarterKitUnityCliLoopAutoStart()
    {
        EditorApplication.delayCall += StartWhenReady;
    }

    private static void StartWhenReady()
    {
        if (EditorApplication.isPlayingOrWillChangePlaymode)
        {
            return;
        }

        if (EditorApplication.isCompiling || EditorApplication.isUpdating)
        {
            EditorApplication.delayCall += StartWhenReady;
            return;
        }

        if (!McpServerController.IsServerRunning)
        {
            McpServerController.StartServer();
        }
    }
}
