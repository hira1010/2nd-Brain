' List SAPI Voices
Set voice = CreateObject("SAPI.SpVoice")
For Each token In voice.GetVoices
    WScript.Echo token.GetDescription
Next
