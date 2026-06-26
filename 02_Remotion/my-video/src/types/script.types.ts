/**
 * スクリプトデータに関する型定義
 */

export type CharacterId = "zundamon" | "metan" | "ryusei";

export type AnimationType = "none" | "fadeIn" | "slideUp" | "slideLeft" | "zoomIn" | "bounce";

export type EmotionType = "normal" | "happy" | "surprised" | "thinking" | "sad";

export interface VisualContent {
    type: "image" | "text" | "none";
    src?: string;
    text?: string;
    fontSize?: number;
    color?: string;
    animation?: AnimationType;
}

export interface SoundEffect {
    src: string;
    volume?: number;
}

export interface BGMConfig {
    src: string;
    volume?: number;
    loop?: boolean;
}

export interface ScriptLine {
    id: number;
    character: CharacterId;
    text: string;
    displayText?: string;
    scene: number;
    voiceFile: string;
    durationInFrames: number;
    pauseAfter: number;
    emotion?: EmotionType;
    visual?: VisualContent;
    se?: SoundEffect;
}

export interface SceneInfo {
    id: number;
    title: string;
    background: string;
}

export interface CurrentScriptState {
    line: ScriptLine | null;
    startFrame: number;
    scene: number;
    isSpeaking: boolean;
}
