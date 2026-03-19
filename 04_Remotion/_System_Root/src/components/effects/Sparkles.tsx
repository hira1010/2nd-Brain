import { random, useCurrentFrame, useVideoConfig } from "remotion";

export const Sparkles = ({ count = 50 }: { count?: number }) => {
    const frame = useCurrentFrame();
    const { width, height } = useVideoConfig();

    const particles = new Array(count).fill(0).map((_, i) => {
        // Generate deterministic random properties
        const x = random(`x-${i}`) * width;
        const y = random(`y-${i}`) * height;
        const baseSize = random(`size-${i}`) * 20 + 5;
        const speed = random(`speed-${i}`) * 0.5 + 0.1;
        const timeOffset = random(`offset-${i}`) * 100;

        // Animate size and opacity to simulate twinkling
        const opacityWave = Math.sin((frame + timeOffset) * speed * 0.1);
        const opacity = (opacityWave + 1) / 2; // Normalize to 0-1

        // Optional: Make them float slightly
        const yOffset = Math.sin((frame + timeOffset) * 0.05) * 20;

        // Colorful sparkles: White, Gold, and soft Blue
        const colors = ["#ffffff", "#ffd700", "#e0f7fa"];
        const color = colors[i % colors.length];

        return {
            x,
            y: y + yOffset,
            size: baseSize * opacity,
            opacity,
            color,
        };
    });

    return (
        <div style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%", pointerEvents: "none" }}>
            {particles.map((p, i) => (
                <div
                    key={i}
                    style={{
                        position: "absolute",
                        left: p.x,
                        top: p.y,
                        width: p.size,
                        height: p.size,
                        borderRadius: "50%",
                        backgroundColor: p.color,
                        opacity: p.opacity,
                        boxShadow: `0 0 ${p.size / 2}px ${p.color}, 0 0 ${p.size}px rgba(255, 255, 255, 0.3)`,
                        transform: "translate(-50%, -50%)",
                    }}
                />
            ))}
        </div>
    );
};
