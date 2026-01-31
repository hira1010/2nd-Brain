import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, Easing } from "remotion";
import { LyricLine } from "../../data/lyrics";

export const LyricsDisplay: React.FC<{ line: LyricLine }> = ({ line }) => {
    const frame = useCurrentFrame();

    const opacity = interpolate(
        frame,
        [0, 15, 45, 60],
        [0, 1, 1, 0],
        {
            easing: Easing.bezier(0.42, 0, 0.58, 1),
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
        }
    );

    return (
        <AbsoluteFill
            style={{
                justifyContent: "flex-end",
                alignItems: "center",
                paddingBottom: "100px",
                opacity,
            }}
        >
            <div
                style={{
                    fontSize: "120px",
                    color: "white",
                    fontFamily: "RocknRoll One",
                    fontStyle: "italic",
                    textShadow: "0 0 20px rgba(0, 255, 255, 0.8), 0 0 40px rgba(0, 255, 255, 0.5)",
                    WebkitTextStroke: "2px #00ffff",
                    textAlign: "center",
                    transform: `skewX(-10deg)`,
                }}
            >
                {line.text}
            </div>
        </AbsoluteFill>
    );
};
