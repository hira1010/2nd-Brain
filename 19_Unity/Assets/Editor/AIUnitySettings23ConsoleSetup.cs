using System;
using System.Reflection;
using UnityEditor;
using UnityEngine;

[InitializeOnLoad]
internal static class AIUnitySettings23ConsoleSetup
{
    private const string PrefKey = "AIUnitySettings23.ConsoleSetup.v1";

    static AIUnitySettings23ConsoleSetup()
    {
        EditorApplication.delayCall += ApplyOnce;
    }

    [MenuItem("Tools/AI Unity Settings 23/Apply Console Preferences")]
    private static void ApplyFromMenu()
    {
        Apply(force: true);
    }

    private static void ApplyOnce()
    {
        Apply(force: false);
    }

    private static void Apply(bool force)
    {
        if (!force && EditorPrefs.GetBool(PrefKey, false))
        {
            return;
        }

        try
        {
            // UnityCsReference ConsoleFlags: ErrorPause = 1 << 2, UseMonospaceFont = 1 << 13.
            Type logEntries = typeof(Editor).Assembly.GetType("UnityEditor.LogEntries");
            MethodInfo setConsoleFlag = logEntries?.GetMethod("SetConsoleFlag", BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic);
            setConsoleFlag?.Invoke(null, new object[] { 1 << 2, false });
            setConsoleFlag?.Invoke(null, new object[] { 1 << 13, true });
            EditorPrefs.SetBool(PrefKey, true);
            Debug.Log("AI Unity Settings 23: Console Error Pause OFF and Monospace font ON applied.");
        }
        catch (Exception ex)
        {
            Debug.LogWarning($"AI Unity Settings 23: failed to apply Console preferences. {ex.Message}");
        }
    }
}