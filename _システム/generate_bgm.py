import math
import struct
import random
import os

# 設定
duration = 60      # 秒数
sample_rate = 44100
output_dir = r"C:\Users\hirak\Desktop\2nd-Brain\18_システム\remotion-project\public"
filename = os.path.join(output_dir, "bgm.wav")

# ディレクトリ確認・作成
os.makedirs(output_dir, exist_ok=True)

def generate_tone(frequency, duration_sec, volume=0.5):
    n_samples = int(sample_rate * duration_sec)
    return [volume * math.sin(2 * math.pi * frequency * t / sample_rate) for t in range(n_samples)]

def save_wav(data, filename):
    print(f"🎵 WAVファイルを生成中: {filename}")
    with open(filename, 'wb') as f:
        # WAVヘッダー
        f.write(b'RIFF')
        f.write(struct.pack('<I', 36 + len(data) * 2))
        f.write(b'WAVE')
        f.write(b'fmt ')
        f.write(struct.pack('<IHHIIHH', 16, 1, 1, sample_rate, sample_rate * 2, 2, 16))
        f.write(b'data')
        f.write(struct.pack('<I', len(data) * 2))
        
        # データ書き込み
        for sample in data:
            s = int(sample * 32767)
            f.write(struct.pack('<h', max(-32767, min(32767, s))))
    print("✅ 生成完了")

# シンプルなコード進行 (CMaj7 - FMaj7 - Dm7 - G7)
chords = [
    [261.63, 329.63, 392.00, 493.88], # C, E, G, B
    [349.23, 440.00, 523.25, 659.25], # F, A, C, E
    [293.66, 349.23, 440.00, 523.25], # D, F, A, C
    [392.00, 493.88, 587.33, 698.46]  # G, B, D, F
]

audio_data = []
samples_per_chord = sample_rate * 4 # 1コード4秒

total_samples = duration * sample_rate
current_sample = 0
chord_index = 0

print("🎹 即席アンビエントBGMを作曲中...")

while current_sample < total_samples:
    # コードを循環
    freqs = chords[chord_index % len(chords)]
    chord_index += 1
    
    # 1秒分の波形を生成して追加
    for t in range(samples_per_chord):
        if current_sample >= total_samples: break
        
        # 複数の周波数を合成
        val = 0
        local_t = t / sample_rate
        
        for f in freqs:
            # 基本音 + ゆっくりした揺らぎ
            tremolo = 1.0 + 0.2 * math.sin(2 * math.pi * 2 * local_t) 
            val += 0.1 * math.sin(2 * math.pi * f * local_t) * tremolo
            
        audio_data.append(val)
        current_sample += 1

# 保存
save_wav(audio_data, filename)
print(f"📁 保存先: {filename}")
