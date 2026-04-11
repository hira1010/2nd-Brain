/**
 * パス計算に関するユーティリティ
 */

import { PATH_CONSTANTS } from "../constants";

/**
 * 画像パスを取得
 * リアリティ画像かどうかを判定して適切なパスを返す
 *
 * @param src - 画像ファイル名
 * @returns 画像の完全パス
 */
export const getImagePath = (src: string): string => {
  const isReality = src.includes("stock_market_pro");
  return isReality
    ? `${PATH_CONSTANTS.REALITY_IMAGES_PATH}/${src}`
    : `${PATH_CONSTANTS.CONTENT_IMAGES_PATH}/${src}`;
};

/**
 * 音声パスを取得
 * 
 * @param voiceFile - 音声ファイル名
 * @returns 音声の完全パス
 */
export const getVoicePath = (voiceFile: string): string => {
  return `${PATH_CONSTANTS.VOICES_PATH}/${voiceFile}`;
};
