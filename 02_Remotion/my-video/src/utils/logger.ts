/**
 * 統一的なロガーモジュール
 * すべてのログ出力を一元管理し、フォーマットとログレベルを統一
 */

export enum LogLevel {
    DEBUG = 0,
    INFO = 1,
    WARN = 2,
    ERROR = 3,
    SILENT = 4,
}

class Logger {
    private level: LogLevel = LogLevel.INFO;

    /**
     * ログレベルを設定
     */
    setLevel(level: LogLevel): void {
        this.level = level;
    }

    /**
     * デバッグログ（開発時のみ）
     */
    debug(message: string, ...args: unknown[]): void {
        if (this.level <= LogLevel.DEBUG) {
            console.log(`🔍 [DEBUG] ${message}`, ...args);
        }
    }

    /**
     * 情報ログ
     */
    info(message: string, ...args: unknown[]): void {
        if (this.level <= LogLevel.INFO) {
            console.log(`ℹ️  [INFO] ${message}`, ...args);
        }
    }

    /**
     * 成功ログ
     */
    success(message: string, ...args: unknown[]): void {
        if (this.level <= LogLevel.INFO) {
            console.log(`✅ [SUCCESS] ${message}`, ...args);
        }
    }

    /**
     * 警告ログ
     */
    warn(message: string, ...args: unknown[]): void {
        if (this.level <= LogLevel.WARN) {
            console.warn(`⚠️  [WARN] ${message}`, ...args);
        }
    }

    /**
     * エラーログ
     */
    error(message: string, error?: unknown): void {
        if (this.level <= LogLevel.ERROR) {
            console.error(`❌ [ERROR] ${message}`);
            if (error instanceof Error) {
                console.error(`   詳細: ${error.message}`);
                if (this.level === LogLevel.DEBUG) {
                    console.error(error.stack);
                }
            } else if (error) {
                console.error(`   詳細:`, error);
            }
        }
    }

    /**
     * 進捗ログ
     */
    progress(current: number, total: number, message: string): void {
        if (this.level <= LogLevel.INFO) {
            const percentage = Math.round((current / total) * 100);
            const bar = this.createProgressBar(current, total);
            console.log(`📊 [${bar}] ${percentage}% ${message}`);
        }
    }

    /**
     * プログレスバーを生成
     */
    private createProgressBar(current: number, total: number, width = 20): string {
        const filled = Math.round((current / total) * width);
        const empty = width - filled;
        return "█".repeat(filled) + "░".repeat(empty);
    }

    /**
     * セクション開始ログ
     */
    section(title: string): void {
        if (this.level <= LogLevel.INFO) {
            console.log(`\n${"=".repeat(50)}`);
            console.log(`  ${title}`);
            console.log(`${"=".repeat(50)}\n`);
        }
    }

    /**
     * グループ開始
     */
    group(title: string): void {
        if (this.level <= LogLevel.INFO) {
            console.group(`📁 ${title}`);
        }
    }

    /**
     * グループ終了
     */
    groupEnd(): void {
        if (this.level <= LogLevel.INFO) {
            console.groupEnd();
        }
    }
}

// シングルトンインスタンス
export const logger = new Logger();

// 環境変数からログレベルを設定
const envLogLevel = process.env.LOG_LEVEL;
if (envLogLevel) {
    const level = LogLevel[envLogLevel.toUpperCase() as keyof typeof LogLevel];
    if (level !== undefined) {
        logger.setLevel(level);
    }
}
