/**
 * アニメーションスタイルを計算するカスタムフック
 */

import { useMemo } from "react";
import { interpolate, spring } from "remotion";
import type { AnimationType } from "../types/script.types";
import type { AnimationStyle } from "../types/component.types";

interface UseAnimationStyleProps {
    frame: number;
    fps: number;
    animation?: AnimationType;
}

/**
 * アニメーションタイプに基づいてスタイルを計算
 */
export const useAnimationStyle = ({
    frame,
    fps,
    animation = "fadeIn",
}: UseAnimationStyleProps): AnimationStyle => {
    return useMemo(() => {
        const progress = interpolate(frame, [0, fps * 0.3], [0, 1], {
            extrapolateRight: "clamp",
        });

        const springProgress = spring({
            frame,
            fps,
            config: { damping: 15, stiffness: 100 },
        });

        switch (animation) {
            case "none":
                return { opacity: 1 };

            case "fadeIn":
                return { opacity: progress };

            case "slideUp":
                return {
                    opacity: progress,
                    transform: `translateY(${interpolate(progress, [0, 1], [50, 0])}px)`,
                };

            case "slideLeft":
                return {
                    opacity: progress,
                    transform: `translateX(${interpolate(progress, [0, 1], [100, 0])}px)`,
                };

            case "zoomIn":
                return {
                    opacity: progress,
                    transform: `scale(${interpolate(progress, [0, 1], [0.8, 1])})`,
                };

            case "bounce":
                return {
                    opacity: Math.min(1, frame / (fps * 0.1)),
                    transform: `scale(${springProgress})`,
                };

            default:
                return { opacity: progress };
        }
    }, [frame, fps, animation]);
};
