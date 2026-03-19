/**
 * フレーム計算に関するカスタムフック
 */

import { useCallback } from "react";
import type { ScriptLine } from "../types/script.types";
import {
    calculateAccumulatedFrames,
    getAdjustedFrames,
} from "../utils/frameCalculations";

interface UseFrameCalculationProps {
    scriptData: ScriptLine[];
}

interface FrameCalculationResult {
    getLineStartFrame: (index: number) => number;
    getLineDuration: (line: ScriptLine) => number;
}

/**
 * スクリプトデータに基づくフレーム計算関数を提供
 */
export const useFrameCalculation = ({
    scriptData,
}: UseFrameCalculationProps): FrameCalculationResult => {
    const getLineStartFrame = useCallback(
        (index: number) => calculateAccumulatedFrames(scriptData, index),
        [scriptData]
    );

    const getLineDuration = useCallback(
        (line: ScriptLine) => getAdjustedFrames(line.durationInFrames),
        []
    );

    return {
        getLineStartFrame,
        getLineDuration,
    };
};
