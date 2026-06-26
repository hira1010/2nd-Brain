import React, { useMemo } from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { ANIMATION_CONSTANTS, SUBTITLE_CONSTANTS } from "../constants";
import type { SubtitleProps } from "../types/component.types";
import {
  calculateFontSizeByRule1500,
  createSubtitleContainerStyle,
  createSubtitleTextStyle,
} from "../utils/styleHelpers";

export const Subtitle: React.FC<SubtitleProps> = React.memo(({ text }) => {
  const frame = useCurrentFrame();
  const fadeStart = ANIMATION_CONSTANTS.ANIMATION_START_FRAMES;
  const fadeEnd = ANIMATION_CONSTANTS.FADE_DURATION_FRAMES;
  const steadyFrame = 20;

  const opacity = interpolate(frame, [fadeStart, fadeEnd, steadyFrame], [0, 1, 1], {
    extrapolateRight: "clamp",
  });

  const fontSize = useMemo(
    () => calculateFontSizeByRule1500(text, SUBTITLE_CONSTANTS.MAX_FONT_SIZE),
    [text]
  );

  const containerStyle = createSubtitleContainerStyle(opacity);
  const textStyle = useMemo(() => createSubtitleTextStyle(fontSize), [fontSize]);

  return (
    <div style={containerStyle}>
      <span style={textStyle}>{text}</span>
    </div>
  );
});

Subtitle.displayName = "Subtitle";
