import React from "react";
import { AbsoluteFill, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const Stamp: React.FC<{ text: string; color?: string; rotation?: number }> = ({
    text,
    color = "#ff0055", // Deep pink/red for impact 
    rotation = -15
}) => {
    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();

    const spr = spring({
        frame,
        fps,
        config: {
            damping: 12,
            stiffness: 200,
        },
    });

    // Impact scale: Starts huge (3x) and slams down to 1x
    const scale = 3 - 2 * spr;

    // Fade in very quickly
    const opacity = Math.min(1, frame / 3);

    return (
        <AbsoluteFill
            style={{
                justifyContent: "center",
                alignItems: "center",
                paddingTop: "40%", // Position towards bottom
            }}
        >
            <div
                style={{
                    fontFamily: "RocknRoll One",
                    fontSize: "180px",
                    fontWeight: "bold",
                    color: color,
                    border: `12px solid ${color}`,
                    padding: "20px 60px",
                    borderRadius: "30px",
                    transform: `scale(${scale}) rotate(${rotation}deg)`,
                    opacity,
                    whiteSpace: "pre-wrap",
                    textAlign: "center",
                    boxShadow: `0 0 0 10px white, 0 10px 30px rgba(0,0,0,0.3)`,
                    backgroundColor: "rgba(255, 255, 255, 0.9)", // Slight background for readability
                    textShadow: "4px 4px 0px rgba(0,0,0,0.1)",
                }}
            >
                {text}
            </div>
        </AbsoluteFill>
    );
};
