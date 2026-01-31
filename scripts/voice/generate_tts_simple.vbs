' Simple TTS Script
Dim voice, filestream, fso

Set voice = CreateObject("SAPI.SpVoice")
Set filestream = CreateObject("SAPI.SpFileStream")
Set fso = CreateObject("Scripting.FileSystemObject")

' Create directory
If Not fso.FolderExists("mv-project\public\audio_parts") Then
    fso.CreateFolder("mv-project\public\audio_parts")
End If

Sub SpeakToFile(text, filename)
    Dim path
    path = fso.GetAbsolutePathName("mv-project\public\audio_parts\" & filename)
    
    ' 3 = SSFMCreateForWrite
    ' True = DoEvents
    filestream.Open path, 3, True
    Set voice.AudioOutputStream = filestream
    voice.Speak text
    filestream.Close
End Sub

SpeakToFile "ひみつ", "01_secret.wav"
SpeakToFile "じみこ？", "02_jimiko.wav"
SpeakToFile "ほんき？", "03_really.wav"
SpeakToFile "まさか！", "04_noway.wav"
SpeakToFile "かくせい", "05_awakening.wav"
SpeakToFile "うつくしい", "06_beautiful.wav"
SpeakToFile "さいきょう", "07_strongest.wav"
