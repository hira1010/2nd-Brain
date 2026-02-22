import React from "react";

export type LyricLine = {
    time: number; // 秒 (またはフレーム)
    text: string;
    duration: number;
    type: "lyric" | "title" | "credit";
    effect: "bounce" | "fade" | "glitch" | "typewriter" | "neon" | "explosive" | "stamp"; // Added stamp
    style?: React.CSSProperties; // 個別のスタイル上書き
};

/**
 * ★重要: このファイルが「編集指示書」を兼ねます。
 * コメントで演出意図（サビ、強調、感情など）を記載し、人間が読んで理解できるようにしてください。
 */
export const lyrics: LyricLine[] = [
    {
        time: 0,
        text: "秘密…",
        duration: 1.5,
        type: "lyric",
        effect: "fade",
        style: { fontSize: "100px", color: "#aaa" }
    },
    {
        time: 2,
        text: "地味子？",
        duration: 1.5,
        type: "lyric",
        effect: "neon"
    },
    {
        time: 4,
        text: "本気…？",
        duration: 1,
        type: "lyric",
        effect: "glitch"
    },
    {
        time: 5.5,
        text: "まさか！",
        duration: 1,
        type: "lyric",
        effect: "explosive"
    },
    {
        time: 8,
        text: "覚醒",
        duration: 2,
        type: "lyric",
        effect: "stamp" // Impactful stamp
    },
    {
        time: 10,
        text: "美しい",
        duration: 2,
        type: "lyric",
        effect: "neon"
    },
    {
        time: 12.5,
        text: "最強",
        duration: 2,
        type: "lyric",
        effect: "stamp" // Final impact
    },
];
