/**
 * キャラクターアニメーション関連の計算ユーティリティ
 */

import { interpolate } from "remotion";
import { CHARACTER_CONSTANTS } from "../constants";

/**
 * 口パクアニメーションの状態を計算
 *
 * @param frame 現在のフレーム
 * @param isSpeaking 話しているか
 * @returns 口が開いているか
 */
export function calculateMouthState(frame: number, isSpeaking: boolean): boolean {
    if (!isSpeaking) return false;
    return Math.floor(frame / CHARACTER_CONSTANTS.MOUTH_ANIMATION_INTERVAL) % 2 === 0;
}

/**
 * 話している時の上下振動を計算
 *
 * @param frame 現在のフレーム
 * @param isSpeaking 話しているか
 * @returns Y軸のオフセット（ピクセル）
 */
export function calculateBounceY(frame: number, isSpeaking: boolean): number {
    if (!isSpeaking) return 0;
    return interpolate(
        Math.sin(frame * CHARACTER_CONSTANTS.BOUNCE_SPEED),
        [-1, 1],
        [-CHARACTER_CONSTANTS.BOUNCE_AMPLITUDE, CHARACTER_CONSTANTS.BOUNCE_AMPLITUDE]
    );
}

/**
 * スライドインアニメーションを計算
 *
 * @param frame 現在のフレーム
 * @param fps フレームレート
 * @param isLeft 左側から登場するか
 * @returns X軸のオフセット（ピクセル）
 */
export function calculateSlideIn(
    frame: number,
    fps: number,
    isLeft: boolean
): number {
    const distance = 200;
    return interpolate(
        frame,
        [0, fps * CHARACTER_CONSTANTS.SLIDE_IN_DURATION],
        [isLeft ? -distance : distance, 0],
        { extrapolateRight: "clamp" }
    );
}
