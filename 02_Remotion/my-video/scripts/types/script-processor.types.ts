/**
 * スクリプト用の型定義
 */

export interface VoicevoxConfig {
    host: string;
    fps: number;
    playbackRate: number;
}

export interface ScriptLineData {
    id: number;
    character: string;
    text: string;
    voiceFile: string;
}

export interface CharacterVoiceMap {
    [key: string]: number;
}

export interface DurationData {
    id: number;
    file: string;
    duration: number;
    frames: number;
}

export interface AudioQueryResponse {
    [key: string]: unknown;
}

export interface YamlScriptLine {
    id: number;
    character: string;
    text: string;
    displayText?: string;
    scene: number;
    pauseAfter?: number;
    emotion?: string;
    visual?: {
        type: string;
        src?: string;
        text?: string;
        fontSize?: number;
        color?: string;
        animation?: string;
    };
    se?: {
        src: string;
        volume?: number;
    };
}

export interface CharacterYamlConfig {
    name: string;
    speakerId: number | null;
    position: string;
    color: string;
    defaultPauseAfter: number;
}

export interface DefaultsYamlConfig {
    newLine: {
        character: string;
        pauseAfter: number;
        durationInFrames: number;
        scene: number;
        emotion: string | null;
    };
    automation: {
        voiceOnSave: boolean;
        autoVoiceFileName: boolean;
    };
}
