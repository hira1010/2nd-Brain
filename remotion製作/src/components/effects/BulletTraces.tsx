import React, { useMemo } from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

const Trace: React.FC<{ seed: number }> = ({ seed }) => {
    const frame = useCurrentFrame();
    const { width, height } = useVideoConfig();

    const y = useMemo(() => Math.random() * height, [seed, height]);
    const speed = useMemo(() => 20 + Math.random() * 30, [seed]);
    const length = useMemo(() => 200 + Math.random() * 400, [seed]);

    const x = (frame * speed + seed * 1000) % (width + length) - length;
    const opacity = interpolate(x, [-length, 0, width, width + length], [0, 0.2, 0.2, 0]);

    return (
        <div
            style={{
                position: "absolute",
                left: x,
                top: y,
                width: length,
                height: "2px",
                background: "linear-gradient(to right, transparent, rgba(0, 255, 255, 0.8), white)",
                boxShadow: "0 0 10px rgba(0, 255, 255, 0.5)",
                opacity,
            }}
        />
    );
};

export const BulletTraces: React.FC = () => {
    const traces = useMemo(() => new Array(15).fill(0).map((_, i) => i), []);

    return (
        <AbsoluteFill>
            {traces.map((i) => (
                <Trace key={i} seed={i} />
            ))}
        </AbsoluteFill>
    );
};
