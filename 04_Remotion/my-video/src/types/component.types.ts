/**
 * コンポーネントプロパティの型定義
 */

import type { CharacterId, EmotionType, VisualContent } from "./script.types";

export interface CharacterProps {
    characterId: CharacterId;
    isSpeaking: boolean;
    emotion?: EmotionType;
}

export interface SubtitleProps {
    text: string;
}

export interface SceneVisualsProps {
    scene: number;
    lineId: number | null;
    frame: number;
    fps: number;
    visual?: VisualContent;
}

export interface AnimationStyle {
    opacity?: number;
    transform?: string;
}
