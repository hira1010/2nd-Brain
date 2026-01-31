' Audio Generation Script (VBScript)
Option Explicit

Dim voice, filestream, outputDir, fso, lyrics, i, item, text, filename, path

Set voice = CreateObject("SAPI.SpVoice")
Set filestream = CreateObject("SAPI.SpFileStream")
Set fso = CreateObject("Scripting.FileSystemObject")

outputDir = "mv-project\public\audio_parts"
If Not fso.FolderExists(outputDir) Then
    fso.CreateFolder(outputDir)
End If

' Simple array simulation
Dim texts(6)
Dim filenames(6)

texts(0) = "ひみつ"
filenames(0) = "01_secret.wav"
texts(1) = "じみこ？"
filenames(1) = "02_jimiko.wav"
texts(2) = "ほんき？"
filenames(2) = "03_really.wav"
texts(3) = "まさか！"
filenames(3) = "04_noway.wav"
texts(4) = "かくせい"
filenames(4) = "05_awakening.wav"
texts(5) = "うつくしい"
filenames(5) = "06_beautiful.wav"
texts(6) = "さいきょう"
filenames(6) = "07_strongest.wav"

For i = 0 To 6
    text = texts(i)
    filename = filenames(i)
    path = fso.BuildPath(fso.GetAbsolutePathName(outputDir), filename)
    
    ' 3 = SSFMCreateForWrite
    filestream.Open path, 3, False
    Set voice.AudioOutputStream = filestream
    voice.Speak text
    filestream.Close
Next

WScript.Echo "TTS Generation Complete"
