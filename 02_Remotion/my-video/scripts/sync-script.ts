/**
 * config/script.yaml を読み込んで src/data/script.ts に変換するスクリプト（リファクタリング版）
 * config/characters.yaml からキャラクター情報も読み込む
 *
 * 使用方法: npm run sync-script
 */

import * as fs from "fs";
import * as path from "path";
import type {
  YamlScriptLine,
  CharacterYamlConfig,
  DefaultsYamlConfig,
} from "./types/script-processor.types";
import {
  loadYamlFile,
  loadDurations,
  processScriptLines,
  generateCharacterIdType,
} from "./utils/yaml-processor";
import { generateScriptFileContent } from "./utils/code-generator";

// ========================================
// 設定
// ========================================

const ROOT_DIR = process.cwd();
const SCRIPT_YAML_PATH = path.join(ROOT_DIR, "config", "script.yaml");
const CHARACTERS_YAML_PATH = path.join(ROOT_DIR, "config", "characters.yaml");
const DEFAULTS_YAML_PATH = path.join(ROOT_DIR, "config", "defaults.yaml");
const OUTPUT_PATH = path.join(ROOT_DIR, "src", "data", "script.ts");
const DURATIONS_PATH = path.join(ROOT_DIR, "public", "voices", "durations.json");

// ========================================
// メイン処理
// ========================================

function main(): void {
  console.log("📖 スクリプト同期処理開始\n");

  try {
    // 1. YAMLファイル読み込み
    const scriptData = loadYamlFile<YamlScriptLine[]>(SCRIPT_YAML_PATH);
    const characters = loadYamlFile<Record<string, CharacterYamlConfig>>(
      CHARACTERS_YAML_PATH
    );
    const defaults = loadYamlFile<DefaultsYamlConfig>(DEFAULTS_YAML_PATH);

    console.log(`✅ スクリプトYAML読み込み完了 (${scriptData.length}行)`);
    console.log(`✅ キャラクター設定読み込み完了`);
    console.log(`✅ デフォルト設定読み込み完了`);

    // 2. 音声の長さ情報を読み込み
    const durations = loadDurations(DURATIONS_PATH);

    // 3. CharacterIdの型を生成
    const characterIdType = generateCharacterIdType(characters);

    // 4. スクリプトデータを処理
    const processedLines = processScriptLines(scriptData, durations, defaults);

    // 5. TypeScriptコードを生成
    const tsContent = generateScriptFileContent(characterIdType, processedLines);

    // 6. ファイルに書き込み
    fs.writeFileSync(OUTPUT_PATH, tsContent);

    console.log(`\n✅ ${OUTPUT_PATH} を生成しました`);
    console.log(`   ${processedLines.length} 件のセリフ`);
  } catch (error) {
    console.error("\n❌ スクリプト同期処理に失敗しました");
    if (error instanceof Error) {
      console.error(`   エラー: ${error.message}`);
    }
    process.exit(1);
  }
}

// ========================================
// 実行
// ========================================

main();
