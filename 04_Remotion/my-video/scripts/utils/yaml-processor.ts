/**
 * YAML処理ユーティリティ
 */

import * as fs from "fs";
import * as yaml from "yaml";
import type {
    YamlScriptLine,
    CharacterYamlConfig,
    DefaultsYamlConfig,
} from "../types/script-processor.types";

/**
 * YAMLファイルを読み込んでパース
 */
export function loadYamlFile<T>(filePath: string): T {
    try {
        const content = fs.readFileSync(filePath, "utf-8");
        return yaml.parse(content);
    } catch (error) {
        console.error(`❌ YAMLファイルの読み込みに失敗: ${filePath}`);
        if (error instanceof Error) {
            console.error(`   エラー詳細: ${error.message}`);
        }
        throw error;
    }
}

/**
 * 音声ファイルの長さ情報を読み込み
 */
export function loadDurations(filePath: string): Record<string, number> {
    if (!fs.existsSync(filePath)) {
        console.warn(`⚠️  長さ情報ファイルが見つかりません: ${filePath}`);
        return {};
    }

    try {
        const content = fs.readFileSync(filePath, "utf-8");
        return JSON.parse(content);
    } catch (error) {
        console.error(`❌ 長さ情報の読み込みに失敗: ${filePath}`);
        return {};
    }
}

/**
 * スクリプトデータを処理
 */
export function processScriptLines(
    scriptData: YamlScriptLine[],
    durations: Record<string, number>,
    defaults: DefaultsYamlConfig
): Array<YamlScriptLine & { voiceFile: string; durationInFrames: number }> {
    return scriptData.map((line) => {
        const voiceFile = generateVoiceFileName(line.id, line.character);
        const durationInFrames = durations[voiceFile] || defaults.newLine.durationInFrames;

        return {
            ...line,
            voiceFile,
            durationInFrames,
            pauseAfter: line.pauseAfter ?? defaults.newLine.pauseAfter,
        };
    });
}

/**
 * 音声ファイル名を生成
 */
function generateVoiceFileName(id: number, character: string): string {
    return `${String(id).padStart(2, "0")}_${character}.wav`;
}

/**
 * CharacterIdの型文字列を生成
 */
export function generateCharacterIdType(
    characters: Record<string, CharacterYamlConfig>
): string {
    const characterIds = Object.keys(characters);
    return characterIds.map((id) => `"${id}"`).join(" | ");
}
