/**
 * カスタムエラークラス
 * エラーの種類を明確にし、適切なハンドリングを可能にする
 */

/**
 * ベースエラークラス
 */
export class AppError extends Error {
    constructor(
        message: string,
        public code: string,
        public context?: Record<string, unknown>
    ) {
        super(message);
        this.name = this.constructor.name;
        Error.captureStackTrace(this, this.constructor);
    }
}

/**
 * 設定関連のエラー
 */
export class ConfigError extends AppError {
    constructor(message: string, context?: Record<string, unknown>) {
        super(message, "CONFIG_ERROR", context);
    }
}

/**
 * ファイル関連のエラー
 */
export class FileError extends AppError {
    constructor(message: string, filePath: string, context?: Record<string, unknown>) {
        super(message, "FILE_ERROR", { ...context, filePath });
    }
}

/**
 * VOICEVOX API関連のエラー
 */
export class VoicevoxError extends AppError {
    constructor(message: string, context?: Record<string, unknown>) {
        super(message, "VOICEVOX_ERROR", context);
    }
}

/**
 * スクリプト解析エラー
 */
export class ScriptParseError extends AppError {
    constructor(message: string, context?: Record<string, unknown>) {
        super(message, "SCRIPT_PARSE_ERROR", context);
    }
}

/**
 * バリデーションエラー
 */
export class ValidationError extends AppError {
    constructor(message: string, field: string, context?: Record<string, unknown>) {
        super(message, "VALIDATION_ERROR", { ...context, field });
    }
}

/**
 * 音声生成エラー
 */
export class AudioGenerationError extends AppError {
    constructor(message: string, context?: Record<string, unknown>) {
        super(message, "AUDIO_GENERATION_ERROR", context);
    }
}

/**
 * エラーがAppErrorのインスタンスかチェック
 */
export function isAppError(error: unknown): error is AppError {
    return error instanceof AppError;
}

/**
 * エラーメッセージを整形して返す
 */
export function formatError(error: unknown): string {
    if (isAppError(error)) {
        let message = `[${error.code}] ${error.message}`;
        if (error.context) {
            message += `\nContext: ${JSON.stringify(error.context, null, 2)}`;
        }
        return message;
    }

    if (error instanceof Error) {
        return error.message;
    }

    return String(error);
}
