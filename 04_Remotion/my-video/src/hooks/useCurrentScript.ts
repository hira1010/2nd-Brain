/**
 * 現在のスクリプト行を計算するカスタムフック
 */

import { useMemo } from "react";
import type { ScriptLine, CurrentScriptState } from "../types/script.types";
import { getAdjustedLineTiming } from "../utils/frameCalculations";

interface UseCurrentScriptProps {
    frame: number;
    scriptData: ScriptLine[];
}

const isFrameInRange = (frame: number, start: number, end: number): boolean =>
    frame >= start && frame < end;

const getFallbackState = (scene: number): CurrentScriptState => ({
    line: null,
    startFrame: 0,
    scene,
    isSpeaking: false,
});

/**
 * 現在のフレームに基づいて、表示すべきスクリプト行を計算
 */
export const useCurrentScript = ({
    frame,
    scriptData,
}: UseCurrentScriptProps): CurrentScriptState => {
    return useMemo(() => {
        let accumulatedFrames = 0;
        let currentScene = 1;

        for (const line of scriptData) {
            const timing = getAdjustedLineTiming(line);
            const lineEndFrame = accumulatedFrames + timing.total;

            if (isFrameInRange(frame, accumulatedFrames, lineEndFrame)) {
                return {
                    line,
                    startFrame: accumulatedFrames,
                    scene: line.scene,
                    isSpeaking: frame < accumulatedFrames + timing.duration,
                };
            }

            accumulatedFrames = lineEndFrame;
            currentScene = line.scene;
        }

        // フレームがすべてのスクリプト行を超えている場合
        return getFallbackState(currentScene);
    }, [frame, scriptData]);
};
