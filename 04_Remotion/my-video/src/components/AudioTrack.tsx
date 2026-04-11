/**
 * 音声トラック表示コンポーネント
 */

import React from "react";
import { Audio, Sequence, staticFile } from "remotion";
import type { ScriptLine } from "../types/script.types";
import { getVoicePath } from "../utils/path";
import { VIDEO_CONFIG } from "../config";

interface AudioTrackProps {
  scriptData: ScriptLine[];
  getLineStartFrame: (index: number) => number;
  getLineDuration: (line: ScriptLine) => number;
}

/**
 * スクリプトデータに基づいた全音声シーケンスを管理
 */
export const AudioTrack: React.FC<AudioTrackProps> = ({
  scriptData,
  getLineStartFrame,
  getLineDuration,
}) => {
  return (
    <>
      {scriptData.map((line, index) => {
        const startFrame = getLineStartFrame(index);
        const voicePath = getVoicePath(line.voiceFile);

        return (
          <Sequence
            key={`audio-${line.id}`}
            from={startFrame}
            durationInFrames={getLineDuration(line)}
          >
            <Audio
              src={staticFile(voicePath)}
              playbackRate={VIDEO_CONFIG.playbackRate}
            />
          </Sequence>
        );
      })}
    </>
  );
};
