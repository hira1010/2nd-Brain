import React from "react";
import {
    AbsoluteFill,
    interpolate,
    spring,
    useCurrentFrame,
    useVideoConfig,
    Img,
    staticFile,
    Easing
} from "remotion";

interface CharacterProps {
    imageSrc: string;
    isBreathing?: boolean;
    isShakingHips?: boolean;
    isClimax?: boolean;
}

export const Character: React.FC<CharacterProps> = ({
    imageSrc,
    isBreathing = true,
    isClimax = false
}) => {
    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();

    // 1. Slow, Intimate Breathing (Pulse scale)
    const breathingSpring = spring({
        frame: frame % (isClimax ? 45 : 90),
        fps,
        config: {
            stiffness: 10,
            damping: 8,
        },
    });

    const breathingScale = isBreathing
        ? interpolate(breathingSpring, [0, 1], [1, isClimax ? 1.05 : 1.02])
        : 1;

    // 2. Ken Burns Effect (Slow zoom for intimacy)
    // Only zoom, no shake
    const kenBurnsScale = interpolate(
        frame,
        [0, 3600],
        [1, 1.3],
        { easing: Easing.bezier(0.33, 1, 0.68, 1) }
    );

    return (
        <AbsoluteFill>
            <div
                style={{
                    width: "100%",
                    height: "100%",
                    transform: `scale(${breathingScale * kenBurnsScale})`,
                    transformOrigin: "center center",
                }}
            >
                <Img
                    src={staticFile(imageSrc)}
                    style={{
                        width: "100%",
                        height: "100%",
                        objectFit: "cover", // Ensures 16:9 coverage
                        // If it's the portrait climax image, align to top-center to show face
                        objectPosition: imageSrc.includes("climax_2") ? "center 25%" : "center center",
                    }}
                />
            </div>
        </AbsoluteFill>
    );
};
