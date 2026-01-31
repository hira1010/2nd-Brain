' Haruka TTS Script Simplified
Option Explicit

Dim voice, filestream, fso, outDir

Set voice = CreateObject("SAPI.SpVoice")
Set filestream = CreateObject("SAPI.SpFileStream")
Set fso = CreateObject("Scripting.FileSystemObject")

' Select Haruka
On Error Resume Next
Set voice.Voice = voice.GetVoices("Name=Microsoft Haruka Desktop").Item(0)
If Err.Number <> 0 Then
    WScript.Echo "Haruka not found, using default."
    Err.Clear
End If
On Error GoTo 0

outDir = "mv-project\public\audio_parts"
If Not fso.FolderExists(outDir) Then
    fso.CreateFolder(outDir)
End If

Sub Speak(txt, fname)
    Dim p
    p = fso.BuildPath(fso.GetAbsolutePathName(outDir), fname)
    ' 3 = SSFMCreateForWrite
    filestream.Open p, 3
    Set voice.AudioOutputStream = filestream
    voice.Speak txt
    filestream.Close
End Sub

Speak "秘密", "01_secret.wav"
Speak "地味子？", "02_jimiko.wav"
Speak "本気？", "03_really.wav"
Speak "まさか！", "04_noway.wav"
Speak "覚醒", "05_awakening.wav"
Speak "美しい", "06_beautiful.wav"
Speak "最強", "07_strongest.wav"

WScript.Echo "Haruka TTS Done."
