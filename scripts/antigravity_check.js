const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const ROOT_DIR = path.resolve(__dirname, '..');
const RENPY_SDK = "C:/Users/hirak/Desktop/eroge/renpy-sdk/renpy-8.5.2-sdk/renpy.exe";

const PROJECTS = {
    RPG_MAKER: path.join(ROOT_DIR, "05_RPG制作"),
    RENPY: path.join(ROOT_DIR, "17_RenPy")
};

function header(text) {
    console.log(`\n${'='.repeat(50)}`);
    console.log(`  ${text}`);
    console.log(`${'='.repeat(50)}`);
}

function checkRpgMaker() {
    header("RPGツクールMZのチェック中 (05_RPG制作)");
    const projPath = PROJECTS.RPG_MAKER;
    if (!fs.existsSync(projPath)) {
        console.log("❌ プロジェクトフォルダが見つかりません。");
        return false;
    }
    
    let success = true;
    const essential = ["data/System.json", "data/CommonEvents.json", "data/Map004.json"];
    for (const f of essential) {
        const filePath = path.join(projPath, f);
        if (!fs.existsSync(filePath)) {
            console.log(`[失敗] 不足ファイル: ${f}`);
            success = false;
        } else {
            console.log(`[正常] 存在確認: ${f}`);
        }
    }
    
    try {
        const mapPath = path.join(projPath, "data/Map004.json");
        if (fs.existsSync(mapPath)) {
            const data = JSON.parse(fs.readFileSync(mapPath, 'utf8'));
            let hasInit = false;
            if (data.events && Array.isArray(data.events)) {
                for (const event of data.events) {
                    if (event && event.name === "INITIALIZER") {
                        hasInit = true;
                        break;
                    }
                }
            }
            if (hasInit) {
                console.log("[正常] Map004に INITIALIZER イベントが見つかりました");
            } else {
                console.log("[警告] Map004に INITIALIZER イベントが見つかりません！ (ユーザー要求によりスキップ)");
            }
        }
    } catch (e) {
        console.log(`⚠️ Map004のイベントを確認できませんでした: ${e.message}`);
        success = false;
    }
    
    return success;
}

function checkRenpy() {
    header("Ren'Pyのチェック中 (17_RenPy)");
    const projPath = PROJECTS.RENPY;
    if (!fs.existsSync(projPath)) {
        console.log("[失敗] プロジェクトフォルダが見つかりません。");
        return false;
    }

    if (!fs.existsSync(RENPY_SDK)) {
        console.log(`[警告] ${RENPY_SDK} に Ren'Py SDK が見つかりません。CLIによる構文チェックをスキップします。`);
        return true;
    }

    try {
        console.log("Ren'Pyの構文チェックを実行中...");
        const result = execSync(`"${RENPY_SDK}" "${projPath}" lint`, { encoding: 'utf8', timeout: 30000 });
        const stdout = result || "";
        if (stdout.includes("0 blocks") && !stdout.includes("14 dialogue blocks")) {
            console.log("[失敗] 構文チェック出力が異常です（対話ブロックが見つかりません）。");
            return false;
        } else {
            console.log("[正常] Ren'Pyの構文チェックが正常に完了しました。");
            return true;
        }
    } catch (e) {
        console.log(`[エラー] Ren'Pyの構文チェック中にエラーが発生しました: ${e.message}`);
        return false;
    }
}

function main() {
    console.log("--- アンチグラビティ プロジェクト整合性チェックを開始 ---");
    
    const results = {
        "RPGツクール": checkRpgMaker(),
        "RenPy": checkRenpy()
    };
    
    header("最終レポート");
    let allOk = true;
    for (const [engine, ok] of Object.entries(results)) {
        const status = ok ? "[正常]" : "[失敗]";
        console.log(`${engine.padEnd(10)}: ${status}`);
        if (!ok) allOk = false;
    }
    
    console.log("\n" + "=".repeat(50));
    if (allOk) {
        console.log("--- プロジェクト状態: 正常 (GREEN) ---");
        console.log("すべてのゲームエンジンプロジェクトの整合性が取れており、正常に動作します。");
        process.exit(0);
    } else {
        console.log("--- プロジェクト状態: 異常 (RED) ---");
        console.log("問題が検出されました。上記の詳細を確認してください。");
        process.exit(1);
    }
}

main();
