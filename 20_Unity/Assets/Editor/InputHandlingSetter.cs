using UnityEditor;
using UnityEngine;

namespace UnityMcpTextbook.Editor
{
    /// <summary>
    /// Unityの入力設定（Active Input Handling）を自動的に「Both（新旧両方）」に設定するエディタスクリプトです。
    /// </summary>
    [InitializeOnLoad]
    public static class InputHandlingSetter
    {
        static InputHandlingSetter()
        {
            // プロジェクト設定のアセットをロードします
            var projectSettings = AssetDatabase.LoadAllAssetsAtPath("ProjectSettings/ProjectSettings.asset");
            if (projectSettings.Length > 0)
            {
                var serializedObject = new SerializedObject(projectSettings[0]);
                var activeInputHandlerProp = serializedObject.FindProperty("activeInputHandler");
                
                // 現在の設定が「Both (値: 2)」ではない場合、自動的に「Both」に書き換えます
                if (activeInputHandlerProp != null && activeInputHandlerProp.intValue != 2)
                {
                    activeInputHandlerProp.intValue = 2; // 2 は Both を表します
                    serializedObject.ApplyModifiedProperties();
                    Debug.Log("[アンチグラビティ] Unityの入力設定（Active Input Handling）を「Both（新旧両方）」に自動変更しました。エラーが解消されます。");
                }
            }
        }
    }
}
