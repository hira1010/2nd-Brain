/*:
 * @target MZ
 * @plugindesc [SYS] 緊急デバッグ・オーバーレイ v2.0 - リファクタリング版
 * @author Antigravity
 *
 * @param DebugSwitch
 * @text デバッグ表示有効スイッチ
 * @type switch
 * @default 0
 * @desc 0の場合は常に有効（開発用）。
 *
 * @help EmergencyDebug.js (v2.0)
 *
 * 開発中の変数の動きをリアルタイムで監視するためのオーバーレイです。
 * F6キーでパーティの全回復を行うショートカット機能も含まれています。
 */

(() => {
    "use strict";

    const pluginName = "EmergencyDebug";
    const params = PluginManager.parameters(pluginName);
    const SW_DEBUG = Number(params["DebugSwitch"] || 0);

    //-----------------------------------------------------------------------------
    // Window_DebugOverlay
    // 画面左上に主要な変数情報を常駐表示するウィンドウ
    //-----------------------------------------------------------------------------

    function Window_DebugOverlay() {
        this.initialize(...arguments);
    }
    Window_DebugOverlay.prototype = Object.create(Window_Base.prototype);
    Window_DebugOverlay.prototype.constructor = Window_DebugOverlay;

    Window_DebugOverlay.prototype.initialize = function(rect) {
        Window_Base.prototype.initialize.call(this, rect);
        this.opacity = 0;
        this.contents.fontSize = 14;
    };

    Window_DebugOverlay.prototype.update = function() {
        Window_Base.prototype.update.call(this);
        if (this.shouldShow()) {
            this.visible = true;
            if (Graphics.frameCount % 10 === 0) {
                this.refresh();
            }
        } else {
            this.visible = false;
        }
    };

    Window_DebugOverlay.prototype.shouldShow = function() {
        if (SW_DEBUG === 0) return true;
        return $gameSwitches.value(SW_DEBUG);
    };

    Window_DebugOverlay.prototype.refresh = function() {
        this.contents.clear();
        this.drawBackground();
        
        let y = 0;
        const lineH = 20;

        this.changeTextColor(ColorManager.systemColor());
        this.drawText("--- DEBUG MONITOR ---", 0, y, this.innerWidth, "center");
        y += lineH;

        this.resetTextColor();
        
        // 監視対象の変数リスト（リファクタリング後のIDに対応）
        const watchList = [
            { id: 9, label: "[CLI] 快感" },
            { id: 11, label: "[CLI] 時間" },
            { id: 19, label: "[CLI] 警戒" },
            { id: 12, label: "[SEA] 発見" },
            { id: 15, label: "[CLI] 部位" }
        ];

        watchList.forEach(item => {
            const val = $gameVariables.value(item.id);
            this.drawText(`${item.label}(V${item.id}):`, 5, y, 120);
            this.drawText(val, 130, y, 40, "right");
            y += lineH;
        });

        y += 5;
        this.changeTextColor("#ffff00");
        const sceneName = SceneManager._scene ? SceneManager._scene.constructor.name : "None";
        this.drawText("Scene: " + sceneName, 5, y, this.innerWidth);
    };

    Window_DebugOverlay.prototype.drawBackground = function() {
        this.contents.paintOpacity = 100;
        this.contents.fillRect(0, 0, this.innerWidth, this.innerHeight, "#000000");
        this.contents.paintOpacity = 255;
    };

    //-----------------------------------------------------------------------------
    // Scene_Base への統合
    //-----------------------------------------------------------------------------

    const _Scene_Base_createWindowLayer = Scene_Base.prototype.createWindowLayer;
    Scene_Base.prototype.createWindowLayer = function() {
        _Scene_Base_createWindowLayer.call(this);
        if (this instanceof Scene_Map || this instanceof Scene_Battle) {
            this.createDebugOverlay();
        }
    };

    Scene_Base.prototype.createDebugOverlay = function() {
        const rect = new Rectangle(10, 10, 200, 180);
        this._debugOverlayWindow = new Window_DebugOverlay(rect);
        this.addWindow(this._debugOverlayWindow);
    };

    //-----------------------------------------------------------------------------
    // デバッグ用ショートカット (F6: 全快など)
    //-----------------------------------------------------------------------------

    const _Input_onKeyDown = Input._onKeyDown;
    Input._onKeyDown = function(event) {
        _Input_onKeyDown.call(this, event);
        if (event.keyCode === 117) { // F6
            if ($gameParty) {
                $gameParty.members().forEach(actor => actor.recoverAll());
                SoundManager.playRecovery();
                console.log("[SYS] Emergency Heal Executed.");
            }
        }
    };

})();
