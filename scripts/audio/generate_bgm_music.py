import wave
import math
import struct

def generate_tone(freq, duration, volume=0.5, sample_rate=44100):
    n_samples = int(sample_rate * duration)
    data = []
    for i in range(n_samples):
        # Sine wave
        value = int(volume * 32767.0 * math.sin(2.0 * math.pi * freq * i / sample_rate))
        # Add some harmonics for richness
        value += int(volume * 0.3 * 32767.0 * math.sin(2.0 * math.pi * (freq * 1.5) * i / sample_rate))
        data.append(struct.pack('<h', max(-32767, min(32767, value))))
    return b''.join(data)

# Upbeat Arpeggio: C Major (C4, E4, G4, C5) + Bass
notes = [261.63, 329.63, 392.00, 523.25]
bpm = 160 # Faster tempo
beat_duration = 60 / bpm
total_duration = 15 # seconds

output_file = "mv-project/public/bgm_music.wav"

with wave.open(output_file, 'w') as wav_file:
    wav_file.setnchannels(1) # Mono
    wav_file.setsampwidth(2) # 16-bit
    wav_file.setframerate(44100)
    
    current_time = 0
    note_idx = 0
    while current_time < total_duration:
        freq = notes[note_idx % len(notes)]
        
        # Add rhythm: Every 4th note is a Bass hit (Octave down + louder)
        vol_scale = 0.3
        if note_idx % 4 == 0:
            freq *= 0.5
            vol_scale = 0.5 # Bass kick
        elif (note_idx // len(notes)) % 2 == 1:
            freq *= 0.5 # Variation
            
        audio_data = generate_tone(freq, beat_duration, volume=vol_scale)
        wav_file.writeframes(audio_data)
        
        current_time += beat_duration
        note_idx += 1

print(f"Generated musical BGM: {output_file}")
