import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig, Easing } from "remotion";

export const ExplosiveLyrics: React.FC<{ text: string }> = ({ text }) => {
    const frame = useCurrentFrame();
    const { fps, durationInFrames } = useVideoConfig();
    const chars = text.split("");

    // Crossfade duration
    const fadeFrames = 10;

    const spr = spring({
        frame,
        fps,
        config: {
            stiffness: 40, // Reduced from 100 for smoother motion
            damping: 12,
        },
    });

    return (
        <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
            <div style={{ display: "flex", position: "relative" }}>
                {chars.map((char, i) => {
                    const angle = (i / chars.length) * Math.PI * 2;
                    const radius = interpolate(spr, [0, 1], [0, 500], {
                        easing: Easing.out(Easing.exp),
                    });

                    // Smooth fade in and fade out aligned with duration
                    const opacity = interpolate(
                        frame,
                        [0, fadeFrames, durationInFrames - fadeFrames, durationInFrames],
                        [0, 1, 1, 0],
                        {
                            easing: Easing.inOut(Easing.quad),
                            extrapolateLeft: "clamp",
                            extrapolateRight: "clamp",
                        }
                    );

                    const scale = interpolate(spr, [0, 1], [1, 3], {
                        easing: Easing.out(Easing.quad),
                    });

                    const x = Math.cos(angle) * radius;
                    const y = Math.sin(angle) * radius;

                    return (
                        <div
                            key={i}
                            style={{
                                position: "absolute",
                                transform: `translate(${x}px, ${y}px) scale(${scale}) skewX(-15deg)`,
                                fontSize: "150px",
                                color: "white",
                                fontFamily: "RocknRoll One",
                                fontStyle: "italic",
                                textShadow: "0 0 30px rgba(0, 255, 255, 1)",
                                opacity,
                                whiteSpace: "pre",
                            }}
                        >
                            {char}
                        </div>
                    );
                })}
            </div>
        </AbsoluteFill>
    );
};
