/**
 * スタイル計算に関するユーティリティ関数
 */

import React from "react";
import { SUBTITLE_CONSTANTS } from "../constants";

const sanitizeSubtitleText = (text: string): string => text.replace(/\n/g, "");

/**
 * 1500の法則に基づいてフォントサイズを計算
 * @param text テキスト（改行を含む可能性あり）
 * @param maxSize 最大フォントサイズ
 * @returns 計算されたフォントサイズ
 */
export const calculateFontSizeByRule1500 = (
    text: string,
    maxSize: number = SUBTITLE_CONSTANTS.MAX_FONT_SIZE
): number => {
    const textLength = sanitizeSubtitleText(text).length;
    if (textLength === 0) {
        return maxSize;
    }
    return Math.min(maxSize, SUBTITLE_CONSTANTS.RULE_1500 / textLength);
};

/**
 * 字幕用のコンテナスタイルを生成
 * @param opacity 透明度
 * @returns CSSプロパティ
 */
export const createSubtitleContainerStyle = (
    opacity: number
): React.CSSProperties => ({
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    width: `${SUBTITLE_CONSTANTS.SUBTITLE_WIDTH_PERCENT}%`,
    textAlign: "center",
    opacity,
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    zIndex: SUBTITLE_CONSTANTS.Z_INDEX,
});

/**
 * 字幕テキストのスタイルを生成
 * @param fontSize フォントサイズ
 * @returns CSSプロパティ
 */
export const createSubtitleTextStyle = (
    fontSize: number
): React.CSSProperties => ({
    fontSize,
    fontFamily: SUBTITLE_CONSTANTS.FONT_FAMILY,
    fontWeight: SUBTITLE_CONSTANTS.FONT_WEIGHT,
    color: SUBTITLE_CONSTANTS.TEXT_COLOR,
    lineHeight: SUBTITLE_CONSTANTS.LINE_HEIGHT,
    WebkitTextStroke: `${SUBTITLE_CONSTANTS.TEXT_STROKE_WIDTH} ${SUBTITLE_CONSTANTS.TEXT_STROKE_COLOR}`,
    paintOrder: "stroke fill",
    filter: `drop-shadow(${SUBTITLE_CONSTANTS.DROP_SHADOW})`,
    whiteSpace: "pre-wrap",
});
