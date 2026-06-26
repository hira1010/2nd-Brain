/**
 * 音声ファイル処理ユーティリティ
 */

import { execSync } from "child_process";

/**
 * WAVファイルの長さを取得（秒）
 * ffprobeを使用して正確な長さを取得
 */
export function getWavDuration(filePath: string): number {
    try {
        const command = `ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "${filePath}"`;
        const result = execSync(command, { encoding: "utf-8" });
        const duration = parseFloat(result.trim());

        if (!isNaN(duration) && duration > 0) {
            return duration;
        }

        throw new Error("Invalid duration value");
    } catch (error) {
        console.error(`⚠️  音声ファイルの長さ取得に失敗: ${filePath}`);
        if (error instanceof Error) {
            console.error(`   エラー詳細: ${error.message}`);
        }
        return 0;
    }
}

/**
 * 秒数をフレーム数に変換（再生速度を考慮）
 */
export function calculateFrames(
    durationSeconds: number,
    fps: number,
    playbackRate: number
): number {
    return Math.ceil(durationSeconds * fps * playbackRate);
}

/**
 * 音声ファイルのフレーム数を計算
 */
export function getAudioFrames(
    filePath: string,
    fps: number,
    playbackRate: number
): number {
    const duration = getWavDuration(filePath);
    return calculateFrames(duration, fps, playbackRate);
}
