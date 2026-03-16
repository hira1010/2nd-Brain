import { VIDEO_CONFIG } from "../config";
import type { ScriptLine } from "../types/script.types";

type FrameAdjustable = {
    durationInFrames: number;
    pauseAfter: number;
};

interface AdjustedLineTiming {
    duration: number;
    pause: number;
    total: number;
}

const OPENING_FRAMES = 60;
const ENDING_FRAMES = 60;

export const getAdjustedFrames = (frames: number): number => {
    return Math.ceil(frames / VIDEO_CONFIG.playbackRate);
};

export const getAdjustedLineTiming = (
    line: FrameAdjustable
): AdjustedLineTiming => {
    const duration = getAdjustedFrames(line.durationInFrames);
    const pause = getAdjustedFrames(line.pauseAfter);

    return {
        duration,
        pause,
        total: duration + pause,
    };
};

export const secondsToFrames = (seconds: number, fps: number): number => {
    return Math.ceil(seconds * fps);
};

export const framesToSeconds = (frames: number, fps: number): number => {
    return frames / fps;
};

export const calculateAccumulatedFrames = (
    scriptData: FrameAdjustable[],
    targetIndex: number
): number => {
    let accumulated = 0;
    for (let i = 0; i < targetIndex; i++) {
        accumulated += getAdjustedLineTiming(scriptData[i]).total;
    }
    return accumulated;
};

export const calculateTotalVideoFrames = (
    scriptData: ScriptLine[],
    playbackRate: number
): number => {
    if (!scriptData || scriptData.length === 0) {
        return OPENING_FRAMES;
    }

    const adjustedBodyFrames = scriptData.reduce((acc, line) => {
        const adjustedDuration = Math.ceil(line.durationInFrames / playbackRate);
        const adjustedPause = Math.ceil(line.pauseAfter / playbackRate);
        return acc + adjustedDuration + adjustedPause;
    }, 0);

    const total = OPENING_FRAMES + adjustedBodyFrames + ENDING_FRAMES;
    return Math.max(1, total);
};
