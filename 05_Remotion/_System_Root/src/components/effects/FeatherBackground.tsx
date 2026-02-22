import React, { useMemo } from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

const Feather: React.FC<{ seed: number }> = ({ seed }) => {
    const frame = useCurrentFrame();
    const { height, width } = useVideoConfig();

    const initialX = useMemo(() => Math.random() * width, [seed, width]);
    const speed = useMemo(() => 1 + Math.random() * 2, [seed]);
    const drift = useMemo(() => 50 + Math.random() * 100, [seed]);

    const y = (frame * speed + seed * 100) % (height + 200) - 100;
    const x = initialX + Math.sin(frame / 30 + seed) * drift;
    const rotate = frame * speed + seed * 360;
    const opacity = interpolate(y, [-100, 0, height, height + 100], [0, 1, 1, 0]);

    return (
        <div
            style={{
                position: "absolute",
                left: x,
                top: y,
                transform: `rotate(${rotate}deg)`,
                opacity,
            }}
        >
            <svg width="40" height="40" viewBox="0 0 100 100" fill="white" style={{ filter: "drop-shadow(0 0 5px rgba(255,255,255,0.5))" }}>
                <path d="M50 10 C 60 40, 90 50, 50 90 C 10 50, 40 40, 50 10" opacity="0.8" />
            </svg>
        </div>
    );
};

export const FeatherBackground: React.FC = () => {
    const feathers = useMemo(() => new Array(20).fill(0).map((_, i) => i), []);

    return (
        <AbsoluteFill>
            {feathers.map((i) => (
                <Feather key={i} seed={i} />
            ))}
        </AbsoluteFill>
    );
};
