/**
 * メインビデオコンポーネント（完全版）
 *
 * 機能:
 * - スクリプトデータに基づいた動画生成
 * - VOICEVOX音声の同期再生
 * - 字幕の自動表示
 * - キャラクターアニメーション
 * - シーンビジュアルの管理
 * - BGM再生
 *
 * 処理フロー:
 * 1. 現在のフレームから表示すべきスクリプト行を計算
 * 2. 各要素（音声、字幕、キャラクター、ビジュアル）を同期して表示
 * 3. 再生速度を考慮したフレーム調整
 */

import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  Audio,
  Sequence,
  staticFile,
} from "remotion";
import { scriptData } from "./data/script";
import { VIDEO_CONFIG } from "./config";
import { Subtitle } from "./components/Subtitle";
import { Character } from "./components/Character";
import { SceneVisuals } from "./components/SceneVisuals";
import { AudioTrack } from "./components/AudioTrack";
import { useCurrentScript } from "./hooks/useCurrentScript";
import { useFrameCalculation } from "./hooks/useFrameCalculation";
import { getAdjustedFrames } from "./utils/frameCalculations";
import { AUDIO_CONSTANTS } from "./constants";

/**
 * メインビデオコンポーネント
 *
 * Remotionのメインコンポジションとして機能し、
 * すべての視覚要素と音声要素を統合して表示します。
 */
export const Main: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 現在のスクリプト行を取得
  const currentScript = useCurrentScript({ frame, scriptData });
  const { getLineStartFrame, getLineDuration } = useFrameCalculation({
    scriptData,
  });

  // 現在の状態を分解
  const {
    line: currentLine,
    startFrame: currentLineStartFrame,
    scene: currentScene,
    isSpeaking,
  } = currentScript;

  return (
    <AbsoluteFill style={{ background: "#000000" }}>
      {/* 1. 全画面ビジュアル (Reality & Ken Burns) */}
      <SceneVisuals
        scene={currentScene}
        lineId={currentLine?.id ?? null}
        frame={frame - currentLineStartFrame} // シーン内の相対フレーム
        fps={fps}
        visual={currentLine?.visual}
      />

      {/* 2. BGM再生 */}
      <Audio
        src={staticFile(AUDIO_CONSTANTS.BGM_FILE)}
        volume={AUDIO_CONSTANTS.BGM_DEFAULT_VOLUME}
        loop={AUDIO_CONSTANTS.BGM_LOOP}
      />

      {/* 3. 音声トラック (VOICEVOX) */}
      <AudioTrack
        scriptData={scriptData}
        getLineStartFrame={getLineStartFrame}
        getLineDuration={getLineDuration}
      />

      {/* 4. キャラクター表示 (ずんだもん) */}
      <Character
        characterId="zundamon"
        isSpeaking={isSpeaking && currentLine?.character === "zundamon"}
        emotion={currentLine?.emotion ?? "normal"}
      />

      {/* 5. 字幕表示 (1500の法則) */}
      {currentLine && (
        <Sequence
          key={`subtitle-${currentLine.id}`}
          from={currentLineStartFrame}
          durationInFrames={
            getLineDuration(currentLine) +
            getAdjustedFrames(currentLine.pauseAfter)
          }
        >
          <Subtitle text={currentLine.displayText ?? currentLine.text} />
        </Sequence>
      )}
    </AbsoluteFill>
  );
};
