/**
 * スクリプトファイル解析ユーティリティ
 */

import * as fs from "fs";
import type { ScriptLineData } from "../types/script-processor.types";

/**
 * script.ts ファイルからスクリプトデータを抽出
 */
export function parseScriptFile(filePath: string): ScriptLineData[] {
    const scriptData: ScriptLineData[] = [];

    try {
        const scriptContent = fs.readFileSync(filePath, "utf-8");
        const scriptDataMatch = scriptContent.match(
            /export const scriptData: ScriptLine\[\] = (\[[\s\S]*?\]);/
        );

        if (!scriptDataMatch) {
            throw new Error("scriptData の定義が見つかりません");
        }

        const parsed = JSON.parse(scriptDataMatch[1]);

        for (const line of parsed) {
            scriptData.push({
                id: line.id,
                character: line.character,
                text: line.text,
                voiceFile: line.voiceFile,
            });
        }

        console.log(`📖 ${scriptData.length}件のセリフを読み込みました`);
    } catch (error) {
        console.error(`❌ スクリプトファイルの解析に失敗: ${filePath}`);
        if (error instanceof Error) {
            console.error(`   エラー詳細: ${error.message}`);
        }
        throw error;
    }

    return scriptData;
}

/**
 * スクリプトデータの妥当性をチェック
 */
export function validateScriptData(data: ScriptLineData[]): void {
    if (data.length === 0) {
        throw new Error("スクリプトデータが空です");
    }

    for (const line of data) {
        if (!line.id || !line.character || !line.text || !line.voiceFile) {
            throw new Error(
                `不正なスクリプトデータ: ID=${line.id}, Character=${line.character}`
            );
        }
    }

    console.log(`✅ スクリプトデータの妥当性チェック完了`);
}
