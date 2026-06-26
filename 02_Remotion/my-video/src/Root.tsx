import React from "react";
import { Composition } from "remotion";
import { VIDEO_CONFIG } from "./config";
import { scriptData } from "./data/script";
import { Main } from "./Main";
import { calculateTotalVideoFrames } from "./utils/frameCalculations";

export const RemotionRoot: React.FC = () => {
  const { fps, width, height, playbackRate } = VIDEO_CONFIG;
  const durationInFrames = calculateTotalVideoFrames(scriptData, playbackRate);

  return (
    <Composition
      id="Main"
      component={Main}
      durationInFrames={durationInFrames}
      fps={fps}
      width={width}
      height={height}
    />
  );
};
