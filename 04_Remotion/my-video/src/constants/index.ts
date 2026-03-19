/**
 * アプリケーション全体で使用する定数を一元管理
 */

// ========================================
// アニメーション定数
// ========================================

export const ANIMATION_CONSTANTS = {
    /** フェードイン・アウトのフレーム数 */
    FADE_DURATION_FRAMES: 6,
    /** Ken Burns エフェクトの時間（秒） */
    KEN_BURNS_DURATION: 5,
    /** Ken Burns 開始スケール */
    KEN_BURNS_START_SCALE: 1,
    /** Ken Burns 終了スケール */
    KEN_BURNS_END_SCALE: 1.15,
    /** アニメーション開始フレーム */
    ANIMATION_START_FRAMES: 0,
    /** アニメーション完了までの時間（秒） */
    ANIMATION_COMPLETE_TIME: 0.3,
    /** バウンスアニメーションの減衰係数 */
    BOUNCE_DAMPING: 15,
    /** バウンスアニメーションのバネ定数 */
    BOUNCE_STIFFNESS: 100,
} as const;

// ========================================
// 字幕定数
// ========================================

export const SUBTITLE_CONSTANTS = {
    /** 1500の法則: 最大文字数 × フォントサイズ */
    RULE_1500: 1500,
    /** 最大フォントサイズ */
    MAX_FONT_SIZE: 180,
    /** 字幕の表示幅（画面幅に対する割合） */
    SUBTITLE_WIDTH_PERCENT: 95,
    /** 字幕の縁取り幅 */
    TEXT_STROKE_WIDTH: "12px",
    /** 字幕の縁取り色 */
    TEXT_STROKE_COLOR: "#000000",
    /** 字幕のドロップシャドウ */
    DROP_SHADOW: "0px 4px 8px rgba(0,0,0,0.8)",
    /** 字幕のフォントファミリー */
    FONT_FAMILY: "'Dela Gothic One', 'system-ui', 'sans-serif'",
    /** 字幕のフォントウェイト */
    FONT_WEIGHT: 900,
    /** 字幕の行間 */
    LINE_HEIGHT: 1.2,
    /** 字幕のテキスト色 */
    TEXT_COLOR: "#FFFFFF",
    /** 字幕のZ-Index */
    Z_INDEX: 100,
} as const;

// ========================================
// キャラクター定数
// ========================================

export const CHARACTER_CONSTANTS = {
    /** キャラクターの高さ（ピクセル） */
    CHARACTER_HEIGHT: 600,
    /** 口パクアニメーションのフレーム間隔 */
    MOUTH_ANIMATION_INTERVAL: 5,
    /** スライドインアニメーションの時間（秒） */
    SLIDE_IN_DURATION: 0.5,
    /** 話している時の上下振動の振幅 */
    BOUNCE_AMPLITUDE: 3,
    /** 話している時の振動速度 */
    BOUNCE_SPEED: 0.3,
    /** プレースホルダーの幅 */
    PLACEHOLDER_WIDTH: 200,
    /** プレースホルダーの高さ */
    PLACEHOLDER_HEIGHT: 300,
    /** プレースホルダーの角丸 */
    PLACEHOLDER_BORDER_RADIUS: 16,
    /** プレースホルダーのボーダー幅 */
    PLACEHOLDER_BORDER_WIDTH: 4,
    /** プレースホルダーの絵文字サイズ */
    PLACEHOLDER_EMOJI_SIZE: 48,
    /** プレースホルダーのテキストサイズ */
    PLACEHOLDER_TEXT_SIZE: 20,
    /** プレースホルダーのテキスト上マージン */
    PLACEHOLDER_TEXT_MARGIN_TOP: 8,
} as const;

// ========================================
// ビジュアル定数
// ========================================

export const VISUAL_CONSTANTS = {
    /** テキストビジュアルのデフォルトフォントサイズ */
    DEFAULT_TEXT_SIZE: 64,
    /** テキストビジュアルのデフォルト色 */
    DEFAULT_TEXT_COLOR: "#FFFFFF",
    /** テキストビジュアルの行間 */
    TEXT_LINE_HEIGHT: 1.4,
    /** テキストビジュアルのシャドウ */
    TEXT_SHADOW: "0px 0px 20px rgba(0,0,0,0.8)",
} as const;

// ========================================
// BGM・オーディオ定数
// ========================================

export const AUDIO_CONSTANTS = {
    /** BGMのデフォルト音量 */
    BGM_DEFAULT_VOLUME: 0.15,
    /** BGMファイル名 */
    BGM_FILE: "Escort.mp3",
    /** BGMをループするか */
    BGM_LOOP: true,
} as const;

// ========================================
// パス定数
// ========================================

export const PATH_CONSTANTS = {
    /** 音声ファイルのベースパス */
    VOICES_PATH: "voices",
    /** BGMのベースパス */
    BGM_PATH: "",
    /** リアリティ画像のパス */
    REALITY_IMAGES_PATH: "images/reality",
    /** コンテンツ画像のパス */
    CONTENT_IMAGES_PATH: "content",
    /** キャラクター画像のベースパス */
    CHARACTER_IMAGES_BASE_PATH: "images",
} as const;

// ========================================
// スクリプト処理定数
// ========================================

export const SCRIPT_CONSTANTS = {
    /** VOICEVOX ホストURL */
    VOICEVOX_HOST: "http://localhost:50021",
    /** デフォルトFPS */
    DEFAULT_FPS: 30,
    /** デフォルト再生速度 */
    DEFAULT_PLAYBACK_RATE: 1.2,
    /** 音声ファイル名のゼロパディング幅 */
    VOICE_FILE_PADDING: 2,
    /** 長さ情報ファイル名 */
    DURATIONS_FILE: "durations.json",
} as const;

// ========================================
// ログメッセージ定数
// ========================================

export const LOG_MESSAGES = {
    // 成功メッセージ
    SUCCESS: {
        VOICEVOX_CONNECTED: "✅ VOICEVOX version:",
        SCRIPT_LOADED: "📖 スクリプトデータを読み込みました:",
        VOICE_GENERATED: "🎙️  音声生成完了:",
        BUILD_COMPLETE: "✅ ビルド完了",
    },
    // エラーメッセージ
    ERROR: {
        VOICEVOX_CONNECTION: "❌ VOICEVOXに接続できません。VOICEVOXを起動してください。",
        SCRIPT_PARSE: "❌ スクリプトファイルの解析に失敗:",
        VOICE_GENERATION: "❌ 音声生成エラー:",
        FILE_NOT_FOUND: "❌ ファイルが見つかりません:",
    },
    // 警告メッセージ
    WARNING: {
        DURATION_NOT_FOUND: "⚠️  音声ファイルの長さ取得に失敗:",
        FILE_NOT_FOUND: "⚠️  ファイルが見つかりません:",
    },
} as const;
