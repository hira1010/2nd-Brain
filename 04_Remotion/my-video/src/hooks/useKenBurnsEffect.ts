/**
 * Ken Burns エフェクト（ズーム効果）を提供するカスタムフック
 */

import { useMemo } from "react";
import { interpolate } from "remotion";

interface UseKenBurnsEffectProps {
    frame: number;
    fps: number;
    duration?: number;
    startScale?: number;
    endScale?: number;
}

/**
 * Ken Burns 効果のスケール値を計算
 * @param frame 現在のフレーム
 * @param fps フレームレート
 * @param duration アニメーション時間（秒）
 * @param startScale 開始スケール
 * @param endScale 終了スケール
 * @returns スケール値
 */
export const useKenBurnsEffect = ({
    frame,
    fps,
    duration = 5,
    startScale = 1,
    endScale = 1.15,
}: UseKenBurnsEffectProps): number => {
    return useMemo(() => {
        return interpolate(frame, [0, fps * duration], [startScale, endScale], {
            extrapolateRight: "clamp",
        });
    }, [frame, fps, duration, startScale, endScale]);
};
