// シンプルなアンビエントBGM生成スクリプト（Node.js）
const fs = require('fs');
const path = require('path');

// 設定
const duration = 60; // 秒
const sampleRate = 44100;
const outputPath = path.join(__dirname, 'remotion-project', 'public', 'bgm.wav');

console.log('🎹 即席アンビエントBGMを作曲中...');

// WAVファイル書き込み関数
function writeWAV(samples, filename) {
    const buffer = Buffer.alloc(44 + samples.length * 2);

    // RIFFヘッダー
    buffer.write('RIFF', 0);
    buffer.writeUInt32LE(36 + samples.length * 2, 4);
    buffer.write('WAVE', 8);

    // fmtチャンク
    buffer.write('fmt ', 12);
    buffer.writeUInt32LE(16, 16); // fmtチャンクサイズ
    buffer.writeUInt16LE(1, 20);  // オーディオフォーマット（PCM）
    buffer.writeUInt16LE(1, 22);  // チャンネル数（モノラル）
    buffer.writeUInt32LE(sampleRate, 24); // サンプルレート
    buffer.writeUInt32LE(sampleRate * 2, 28); // バイトレート
    buffer.writeUInt16LE(2, 32);  // ブロックアライン
    buffer.writeUInt16LE(16, 34); // ビット深度

    // dataチャンク
    buffer.write('data', 36);
    buffer.writeUInt32LE(samples.length * 2, 40);

    // サンプルデータを書き込み
    for (let i = 0; i < samples.length; i++) {
        const sample = Math.max(-32767, Math.min(32767, Math.floor(samples[i] * 32767)));
        buffer.writeInt16LE(sample, 44 + i * 2);
    }

    // ディレクトリ作成
    const dir = path.dirname(filename);
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }

    fs.writeFileSync(filename, buffer);
    console.log(`✅ 生成完了: ${filename}`);
}

// コード進行 (CMaj7 - FMaj7 - Dm7 - G7)
const chords = [
    [261.63, 329.63, 392.00, 493.88], // C, E, G, B
    [349.23, 440.00, 523.25, 659.25], // F, A, C, E
    [293.66, 349.23, 440.00, 523.25], // D, F, A, C
    [392.00, 493.88, 587.33, 698.46]  // G, B, D, F
];

const audioData = [];
const samplesPerChord = sampleRate * 4; // 1コード4秒
const totalSamples = duration * sampleRate;

let currentSample = 0;
let chordIndex = 0;

while (currentSample < totalSamples) {
    const freqs = chords[chordIndex % chords.length];
    chordIndex++;

    for (let t = 0; t < samplesPerChord && currentSample < totalSamples; t++) {
        let val = 0;
        const localT = t / sampleRate;

        for (const f of freqs) {
            // 基本音 + ゆっくりした揺らぎ
            const tremolo = 1.0 + 0.2 * Math.sin(2 * Math.PI * 2 * localT);
            val += 0.1 * Math.sin(2 * Math.PI * f * localT) * tremolo;
        }

        audioData.push(val);
        currentSample++;
    }
}

// WAVファイルを生成
writeWAV(audioData, outputPath);
console.log(`📁 保存先: ${outputPath}`);
