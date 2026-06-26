/**
 * VOICEVOX API クライアント
 */

import type {
    AudioQueryResponse,
    VoicevoxConfig,
} from "../types/script-processor.types";

/**
 * VOICEVOXが起動しているか確認
 */
export async function checkVoicevoxConnection(
    host: string
): Promise<boolean> {
    try {
        const response = await fetch(`${host}/version`);
        if (response.ok) {
            const version = await response.text();
            console.log(`✅ VOICEVOX version: ${version}`);
            return true;
        }
    } catch (error) {
        console.error("❌ VOICEVOXに接続できません。VOICEVOXを起動してください。");
        if (error instanceof Error) {
            console.error(`   エラー詳細: ${error.message}`);
        }
    }
    return false;
}

/**
 * 音声クエリを取得
 */
export async function getAudioQuery(
    host: string,
    text: string,
    speakerId: number
): Promise<AudioQueryResponse> {
    const encodedText = encodeURIComponent(text);
    const url = `${host}/audio_query?speaker=${speakerId}&text=${encodedText}`;

    const response = await fetch(url, { method: "POST" });

    if (!response.ok) {
        throw new Error(
            `音声クエリの取得に失敗しました: ${response.status} ${response.statusText}`
        );
    }

    return response.json();
}

/**
 * 音声を合成
 */
export async function synthesizeAudio(
    host: string,
    query: AudioQueryResponse,
    speakerId: number
): Promise<ArrayBuffer> {
    const url = `${host}/synthesis?speaker=${speakerId}`;

    const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(query),
    });

    if (!response.ok) {
        throw new Error(
            `音声合成に失敗しました: ${response.status} ${response.statusText}`
        );
    }

    return response.arrayBuffer();
}

/**
 * 音声を生成してファイルに保存
 */
export async function generateVoiceFile(
    config: VoicevoxConfig,
    text: string,
    speakerId: number,
    outputPath: string,
    fs: any
): Promise<void> {
    const query = await getAudioQuery(config.host, text, speakerId);
    const audio = await synthesizeAudio(config.host, query, speakerId);
    fs.writeFileSync(outputPath, Buffer.from(audio));
}
