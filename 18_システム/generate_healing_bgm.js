// ヒーリングBGM生成スクリプト（Node.js）
const fs = require('fs');
const path = require('path');

// 設定
const duration = 60; // 秒
const sampleRate = 44100;
const outputPath = path.join(__dirname, 'remotion-project', 'public', 'bgm.wav');

console.log('🎵 ヒーリングBGMを作曲中...');

// WAVファイル書き込み関数
function writeWAV(samples, filename) {
    const buffer = Buffer.alloc(44 + samples.length * 2);

    // RIFFヘッダー
    buffer.write('RIFF', 0);
    buffer.writeUInt32LE(36 + samples.length * 2, 4);
    buffer.write('WAVE', 8);

    // fmtチャンク
    buffer.write('fmt ', 12);
    buffer.writeUInt32LE(16, 16);
    buffer.writeUInt16LE(1, 20);
    buffer.writeUInt16LE(1, 22);
    buffer.writeUInt32LE(sampleRate, 24);
    buffer.writeUInt32LE(sampleRate * 2, 28);
    buffer.writeUInt16LE(2, 32);
    buffer.writeUInt16LE(16, 34);

    // dataチャンク
    buffer.write('data', 36);
    buffer.writeUInt32LE(samples.length * 2, 40);

    // サンプルデータを書き込み
    for (let i = 0; i < samples.length; i++) {
        const sample = Math.max(-32767, Math.min(32767, Math.floor(samples[i] * 32767)));
        buffer.writeInt16LE(sample, 44 + i * 2);
    }

    const dir = path.dirname(filename);
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }

    fs.writeFileSync(filename, buffer);
    console.log(`✅ 生成完了: ${filename}`);
}

// 432Hz基準のヒーリング周波数（ソルフェジオ周波数を含む）
// C=256Hz基準の純正律に近い周波数
const healingFrequencies = [
    256.00,  // C (ルートチャクラ)
    288.00,  // D 
    324.00,  // E (第3チャクラ)
    341.33,  // F
    384.00,  // G (喉チャクラ)
    432.00,  // A (宇宙の周波数)
    486.00   // B
];

const audioData = [];
const totalSamples = duration * sampleRate;
const fadeTime = 3; // フェード時間（秒）
const fadeSamples = fadeTime * sampleRate;

// ベース音生成（深く、柔らかい）
for (let i = 0; i < totalSamples; i++) {
    const t = i / sampleRate;
    let sample = 0;

    // フェードイン/アウト計算
    let envelope = 1.0;
    if (i < fadeSamples) {
        envelope = i / fadeSamples; // フェードイン
    } else if (i > totalSamples - fadeSamples) {
        envelope = (totalSamples - i) / fadeSamples; // フェードアウト
    }

    // ドローン音（低音の持続音）
    const droneFreq = healingFrequencies[0] / 2; // 128Hz
    sample += 0.08 * Math.sin(2 * Math.PI * droneFreq * t);

    // ゆっくり変化するメロディアスな音
    const cycleTime = 12; // 12秒サイクル
    const phase = (t % cycleTime) / cycleTime;

    // サイクル内で周波数をゆっくり変化
    const freqIndex = Math.floor(phase * healingFrequencies.length);
    const nextFreqIndex = (freqIndex + 1) % healingFrequencies.length;
    const blend = (phase * healingFrequencies.length) % 1;

    const freq = healingFrequencies[freqIndex] * (1 - blend) +
        healingFrequencies[nextFreqIndex] * blend;

    // メインの癒し音
    sample += 0.15 * Math.sin(2 * Math.PI * freq * t);

    // 倍音（柔らかさを追加）
    sample += 0.05 * Math.sin(2 * Math.PI * freq * 2 * t);
    sample += 0.025 * Math.sin(2 * Math.PI * freq * 3 * t);

    // ゆっくりとしたトレモロ（呼吸のようなリズム）
    const breathCycle = 0.15; // 呼吸サイクル（約6.7秒）
    const tremolo = 0.85 + 0.15 * Math.sin(2 * Math.PI * breathCycle * t);

    // 微細な揺らぎ（人間味）
    const subtleVariation = 1.0 + 0.02 * Math.sin(2 * Math.PI * 0.05 * t);

    // 最終出力
    sample = sample * tremolo * subtleVariation * envelope;

    audioData.push(sample);
}

// WAVファイルを生成
writeWAV(audioData, outputPath);
console.log(`📁 保存先: ${outputPath}`);
console.log('🌊 ヒーリングBGM完成。リラックスしてお楽しみください。');
