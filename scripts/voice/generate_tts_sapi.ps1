# Audio Generation Script using SAPI.SpVoice (COM)
$voice = New-Object -ComObject SAPI.SpVoice
$voice.Rate = 0
$voice.Volume = 100

# Helper to save to wav (SAPI is tricky with streams in PS, so we might just use python if this fails or just speak)
# Actually, SAPI file output in PS requires creating a SpFileStream.

try {
    $filestream = New-Object -ComObject SAPI.SpFileStream
    
    $lyrics = @(
        @{ Text = "ひみつ"; Filename = "01_secret.wav" },
        @{ Text = "じみこ？"; Filename = "02_jimiko.wav" },
        @{ Text = "ほんき？"; Filename = "03_really.wav" },
        @{ Text = "まさか！"; Filename = "04_noway.wav" },
        @{ Text = "かくせい"; Filename = "05_awakening.wav" },
        @{ Text = "うつくしい"; Filename = "06_beautiful.wav" },
        @{ Text = "さいきょう"; Filename = "07_strongest.wav" }
    )

    $outputDir = "mv-project/public/audio_parts"
    New-Item -ItemType Directory -Force -Path $outputDir | Out-Null

    foreach ($line in $lyrics) {
        $path = Join-Path (Get-Location).Path "$outputDir\$($line.Filename)"
        $filestream.Open($path, 3, $false) # 3=SSFMCreateForWrite
        $voice.AudioOutputStream = $filestream
        $voice.Speak($line.Text)
        $filestream.Close()
        Write-Host "Generated: $($line.Text) -> $path"
    }
}
catch {
    Write-Error "SAPI failed: $_"
    exit 1
}
