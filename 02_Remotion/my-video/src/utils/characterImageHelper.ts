/**
 * キャラクター画像ファイル名取得ユーティリティ
 */

import { SETTINGS, AVAILABLE_IMAGES } from "../settings.generated";
import type { EmotionType } from "../types/script.types";

/**
 * 表情と口の状態に応じた画像ファイル名を取得
 * 存在チェックを行い、フォールバック処理も実施
 *
 * @param characterId キャラクターID
 * @param emotion 表情
 * @param mouthOpen 口が開いているか
 * @returns 画像ファイル名
 */
export function getCharacterImageFileName(
    characterId: string,
    emotion: EmotionType,
    mouthOpen: boolean
): string {
    const state = mouthOpen ? "open" : "close";
    const availableFiles = AVAILABLE_IMAGES[characterId] || [];

    // 通常表情またはemotionがない場合
    if (emotion === "normal" || !emotion) {
        return `mouth_${state}.png`;
    }

    // 表情差分を試す: {emotion}_open.png, {emotion}_close.png
    const emotionFile = `${emotion}_${state}.png`;
    if (availableFiles.includes(emotionFile)) {
        return emotionFile;
    }

    // 表情の口開き画像だけある場合（口閉じがない）、口開き画像を使う
    const emotionOpenFile = `${emotion}_open.png`;
    if (availableFiles.includes(emotionOpenFile)) {
        return emotionOpenFile;
    }

    // 表情差分がない場合はデフォルトにフォールバック
    return `mouth_${state}.png`;
}

/**
 * キャラクター画像の完全パスを取得
 *
 * @param characterId キャラクターID
 * @param emotion 表情
 * @param mouthOpen 口が開いているか
 * @returns 画像の完全パス
 */
export function getCharacterImagePath(
    characterId: string,
    emotion: EmotionType,
    mouthOpen: boolean
): string {
    const basePath = SETTINGS.character.imagesBasePath;
    const imageFileName = getCharacterImageFileName(characterId, emotion, mouthOpen);
    return `${basePath}/${characterId}/${imageFileName}`;
}
