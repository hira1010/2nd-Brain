#!/usr/bin/env npx ts-node

/**
 * VOICEVOX音声一括生成スクリプト（リファクタリング版）
 *
 * 使用方法:
 *   npx ts-node scripts/generate-voices.ts
 *
 * 前提条件:
 *   - VOICEVOXがlocalhost:50021で起動していること
 *   - ffprobeがインストールされていること
 */

import * as fs from "fs";
import * as path from "path";
import type {
  VoicevoxConfig,
  CharacterVoiceMap,
  DurationData,
  ScriptLineData,
} from "./types/script-processor.types";
import { checkVoicevoxConnection, generateVoiceFile } from "./utils/voicevox-client";
import { getAudioFrames } from "./utils/audio-processor";
import { parseScriptFile, validateScriptData } from "./utils/script-parser";

// ========================================
// 設定
// ========================================

const ROOT_DIR = process.cwd();
const SCRIPT_PATH = path.join(ROOT_DIR, "src/data/script.ts");
const OUTPUT_DIR = path.join(ROOT_DIR, "public/voices");

const CONFIG: VoicevoxConfig = {
  host: "http://localhost:50021",
  fps: 30,
  playbackRate: 1.2,
};

const CHARACTER_VOICE_MAP: CharacterVoiceMap = {
  zundamon: 3,
  metan: 2,
  ryusei: 13,
};

// ========================================
// メイン処理
// ========================================

async function main(): Promise<void> {
  console.log("🎤 VOICEVOX音声生成スクリプト開始\n");

  // 1. VOICEVOX接続確認
  if (!(await checkVoicevoxConnection(CONFIG.host))) {
    process.exit(1);
  }

  // 2. 出力ディレクトリ作成
  ensureOutputDirectory(OUTPUT_DIR);

  // 3. スクリプトデータ読み込み
  const scriptData = parseScriptFile(SCRIPT_PATH);
  validateScriptData(scriptData);

  // 4. 音声生成
  const durationsArray = await generateAllVoices(scriptData);

  // 5. 結果保存
  saveDurations(durationsArray);

  console.log("\n✅ 音声生成完了！");
}

/**
 * 出力ディレクトリが存在することを確認
 */
function ensureOutputDirectory(dir: string): void {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
    console.log(`📁 出力フォルダを作成: ${dir}`);
  }
}

/**
 * すべての音声を生成
 */
async function generateAllVoices(
  scriptData: ScriptLineData[]
): Promise<DurationData[]> {
  const durationsArray: DurationData[] = [];

  for (const line of scriptData) {
    const speakerId = CHARACTER_VOICE_MAP[line.character];

    if (speakerId === undefined) {
      console.error(`❌ 未知のキャラクター: ${line.character}`);
      continue;
    }

    try {
      const durationData = await generateSingleVoice(line, speakerId);
      durationsArray.push(durationData);
    } catch (error) {
      console.error(`❌ 音声生成エラー [${line.voiceFile}]:`, error);
    }
  }

  return durationsArray;
}

/**
 * 単一の音声を生成
 */
async function generateSingleVoice(
  line: ScriptLineData,
  speakerId: number
): Promise<DurationData> {
  const outputPath = path.join(OUTPUT_DIR, line.voiceFile);
  const displayText = line.text.substring(0, 30) + (line.text.length > 30 ? "..." : "");

  console.log(`🎙️  生成中: ${line.voiceFile} - "${displayText}"`);

  // 音声生成
  await generateVoiceFile(CONFIG, line.text, speakerId, outputPath, fs);

  // 長さ取得
  const frames = getAudioFrames(outputPath, CONFIG.fps, CONFIG.playbackRate);
  const duration = frames / (CONFIG.fps * CONFIG.playbackRate);

  console.log(`   ✓ ${duration.toFixed(2)}s (${frames} frames)`);

  return {
    id: line.id,
    file: line.voiceFile,
    duration,
    frames,
  };
}

/**
 * 音声の長さ情報を保存
 */
function saveDurations(durationsArray: DurationData[]): void {
  const durationsMap: Record<string, number> = {};

  for (const data of durationsArray) {
    durationsMap[data.file] = data.frames;
  }

  const resultPath = path.join(OUTPUT_DIR, "durations.json");
  fs.writeFileSync(resultPath, JSON.stringify(durationsMap, null, 2));

  console.log(`\n💾 長さ情報を保存: ${resultPath}`);
  console.log("\n📊 生成結果:");
  for (const d of durationsArray) {
    console.log(`   ID ${d.id}: ${d.frames} frames (${d.duration.toFixed(2)}s)`);
  }
}

// ========================================
// 実行
// ========================================

main().catch((error) => {
  console.error("\n❌ エラーが発生しました:", error);
  process.exit(1);
});
