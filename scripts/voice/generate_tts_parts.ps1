# Audio Generation Script for Jimiko PV
Add-Type -AssemblyName System.Speech

$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.Rate = 0  # Normal speed
$synth.Volume = 100

# Define lyrics and filenames
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
    $path = Join-Path $outputDir $line.Filename
    $synth.SetOutputToWaveFile($path)
    $synth.Speak($line.Text)
    $synth.SetOutputToNull()
    Write-Host "Generated: $($line.Text) -> $path"
}
