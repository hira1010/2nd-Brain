/*:
 * @target MZ
 * @plugindesc [Emergency] 起動スタック調査 ＆ 画像特定 v6.2
 * @author Antigravity
 *
 * @help
 * 起動時のフリーズや真黒な画面を調査し、原因の特定と強制突破を行います。
 * 【v6.2 更新内容】
 * 1. 読み込みが止まっている画像（Bitmap）のファイル名を表示機能。
 * 2. 画面の強制描画（明るさ最大化）の強化。
 */
(() => {
    "use strict";

    //=========================================================================
    // DOM診断オーバーレイ (UI)
    //=========================================================================
    let _overlay = null;
    let _logArea = null;
    let _statusArea = null;
    let _forceStartCount = 0;

    function createOverlay() {
        if (_overlay) return;
        _overlay = document.createElement("div");
        Object.assign(_overlay.style, {
            position:        "absolute",
            top:             "5px",
            right:           "5px",
            zIndex:          "20000",
            backgroundColor: "rgba(10, 10, 40, 0.95)",
            color:           "#00ddff",
            fontFamily:      "Consolas, monospace",
            fontSize:        "11px",
            padding:         "12px",
            borderRadius:    "6px",
            border:          "2px solid #00ddff",
            width:           "360px",
            boxShadow:       "0 0 20px rgba(0,221,255,0.4)"
        });

        _statusArea = document.createElement("div");
        _statusArea.style.borderBottom = "1px solid #333366";
        _statusArea.style.marginBottom = "8px";
        _statusArea.style.paddingBottom = "5px";
        _overlay.appendChild(_statusArea);

        const btn = document.createElement("button");
        btn.textContent = ">>> FORCE START MAP 4 <<<";
        Object.assign(btn.style, {
            width:           "100%",
            padding:         "8px",
            backgroundColor: "#ff4400",
            color:           "white",
            border:          "none",
            borderRadius:    "4px",
            cursor:          "pointer",
            fontWeight:      "bold",
            marginBottom:    "8px",
            pointerEvents:   "auto"
        });
        btn.onclick = () => emergencyForceStart();
        _overlay.appendChild(btn);

        _logArea = document.createElement("div");
        _overlay.appendChild(_logArea);

        document.body.appendChild(_overlay);
    }

    function updateOverlay() {
        if (!_statusArea) return;
        
        const scene   = SceneManager._scene ? SceneManager._scene.constructor.name : "None";
        const frame   = Graphics.frameCount;
        const dbReady = (typeof DataManager !== "undefined") ? DataManager.isDatabaseLoaded() : false;
        const ftReady = (typeof FontManager !== "undefined") ? FontManager.isReady() : false;
        
        let loadingImages = [];
        if (typeof ImageManager !== "undefined" && ImageManager._cache) {
            for (const key in ImageManager._cache) {
                const bitmap = ImageManager._cache[key];
                if (bitmap && !bitmap.isReady()) {
                    // キー（パス）からファイル名だけ抽出
                    const name = key.split('/').pop() || key;
                    loadingImages.push(name);
                }
            }
        }

        const isBoot = (scene === "Scene_Boot");
        if (isBoot) _forceStartCount++;

        _statusArea.innerHTML = 
            `<b>[ NUCLEAR MONITOR v6.2 ]</b><br>` +
            `Scene: <span style="color:#ffffff">${scene}</span> | Frame: ${frame}<br>` +
            `<hr style="border:0; border-top:1px solid #333366;">` +
            `DB Ready: ${dbReady} | Font Ready: ${ftReady}<br>` +
            `Loading: <b style="color:${loadingImages.length > 0 ? '#ff8800' : '#00ff00'}">${loadingImages.length}</b> ` +
            `<small>(${loadingImages.join(", ") || "None"})</small>`;

        if (isBoot && _forceStartCount === 180) {
            addLog("STUCK. Triggering Auto Force-Start...", "#ffaa00");
            emergencyForceStart();
        }
    }

    function emergencyForceStart() {
        addLog("NUCLEAR OPTION: Executing...", "#ff4444");
        try {
            if (typeof DataManager !== "undefined" && DataManager.isDatabaseLoaded()) {
                DataManager.setupNewGame();
                $gamePlayer.reserveTransfer(4, 8, 6, 0, 2);
                SceneManager.goto(Scene_Map);
                addLog("Success: Transitioned to Map 4.", "#00ff00");
            } else {
                addLog("Wait: Database not loaded yet.", "#ffff00");
            }
        } catch (e) {
            addLog(`ERROR: ${e.message}`, "#ff0000");
        }
    }

    function addLog(msg, color = "#00ddff") {
        createOverlay();
        const line = document.createElement("div");
        line.style.color = color;
        line.style.borderLeft = `3px solid ${color}`;
        line.style.paddingLeft = "5px";
        line.style.marginBottom = "3px";
        line.style.fontSize = "10px";
        line.textContent = `[${new Date().toLocaleTimeString().split(" ")[0]}] ${msg}`;
        _logArea.appendChild(line);
        if (_logArea.childNodes.length > 20) _logArea.removeChild(_logArea.firstChild);
    }

    setInterval(() => {
        createOverlay();
        updateOverlay();
    }, 500);

    // 強制描画ガード
    const _Scene_Base_update = Scene_Base.prototype.update;
    Scene_Base.prototype.update = function() {
        _Scene_Base_update.call(this);
        if ($gameScreen && $gameScreen.brightness() < 255) {
            $gameScreen.setBrightness(255);
            $gameScreen.clearFade();
        }
    };

    window.addEventListener("error", (e) => addLog(`JS: ${e.message}`, "#ff4444"));
    addLog("Diagnostic Plugin v6.2 Ready.");
})();






