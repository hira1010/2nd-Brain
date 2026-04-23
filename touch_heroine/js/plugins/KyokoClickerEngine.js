/*:
 * @target MZ
 * @plugindesc [CLI] クリッカーエンジン EXTRA v2.0 - リファクタリング版
 * @author Antigravity
 *
 * @param VariableSettings
 * @text 【変数設定】
 *
 * @param PleasureVariable
 * @parent VariableSettings
 * @text [CLI] 現在の快感 (Variable ID)
 * @type variable
 * @default 9
 *
 * @param MaxPleasureVariable
 * @parent VariableSettings
 * @text [CLI] 目標快感 (Variable ID)
 * @type variable
 * @default 10
 *
 * @param TimeVariable
 * @parent VariableSettings
 * @text [CLI] 残り時間 (Variable ID)
 * @type variable
 * @default 11
 *
 * @param LustVariable
 * @parent VariableSettings
 * @text [CLI] 快楽許容 (Variable ID)
 * @type variable
 * @default 17
 *
 * @param ShameVariable
 * @parent VariableSettings
 * @text [CLI] 羞恥心 (Variable ID)
 * @type variable
 * @default 16
 *
 * @param SuspicionVariable
 * @parent VariableSettings
 * @text [CLI] 警戒度 (Variable ID)
 * @type variable
 * @default 19
 *
 * @param TargetPartVariable
 * @parent VariableSettings
 * @text [CLI] 判定部位ID (Variable ID)
 * @type variable
 * @default 15
 *
 * @param SwitchSettings
 * @text 【スイッチ設定】
 *
 * @param ModeSwitch
 * @parent SwitchSettings
 * @text [CLI] 実行中フラグ (Switch ID)
 * @type switch
 * @default 9
 *
 * @param StealthSwitch
 * @parent SwitchSettings
 * @text [CLI] 足音警戒中 (Switch ID)
 * @type switch
 * @default 10
 *
 * @param EventSettings
 * @text 【イベント設定】
 *
 * @param BustedCommonEvent
 * @parent EventSettings
 * @text 発見時コモンイベント (Common Event ID)
 * @type common_event
 * @default 31
 *
 * @help KyokoClickerEngine.js (v2.0)
 *
 * クリッカーパートの主要ロジックを管理します。
 * 今回のリファクタリングで、全てのIDをプラグインパラメーターから設定可能にしました。
 */

(() => {
    "use strict";

    const pluginName = "KyokoClickerEngine";
    const params = PluginManager.parameters(pluginName);

    // パラメーターの取得と定数化
    const VAR_PLEASURE = Number(params["PleasureVariable"] || 9);
    const VAR_MAX_PLEASURE = Number(params["MaxPleasureVariable"] || 10);
    const VAR_TIME = Number(params["TimeVariable"] || 11);
    const VAR_LUST = Number(params["LustVariable"] || 17);
    const VAR_SHAME = Number(params["ShameVariable"] || 16);
    const VAR_SUSPICION = Number(params["SuspicionVariable"] || 19);
    const VAR_TARGET_PART = Number(params["TargetPartVariable"] || 15);
    
    const SW_MODE = Number(params["ModeSwitch"] || 9);
    const SW_STEALTH = Number(params["StealthSwitch"] || 10);
    const CE_BUSTED = Number(params["BustedCommonEvent"] || 31);

    //-----------------------------------------------------------------------------
    // Sprite_KyokoClicker
    // クリッカー画面の立ち絵とタッチ判定を管理するクラス
    //-----------------------------------------------------------------------------

    function Sprite_KyokoClicker() {
        this.initialize(...arguments);
    }

    Sprite_KyokoClicker.prototype = Object.create(Sprite.prototype);
    Sprite_KyokoClicker.prototype.constructor = Sprite_KyokoClicker;

    Sprite_KyokoClicker.prototype.initialize = function() {
        Sprite.prototype.initialize.call(this);
        this.setupHierarchy();
        this.resetState();
    };

    Sprite_KyokoClicker.prototype.setupHierarchy = function() {
        this.anchor.x = 0.5;
        this.anchor.y = 0;
        this.x = Graphics.width / 2;
        this.y = 50;
        this.scale.x = 0.75;
        this.scale.y = 0.75;
    };

    Sprite_KyokoClicker.prototype.resetState = function() {
        this._shake = 0;
        this._currentLevel = -1;
    };

    Sprite_KyokoClicker.prototype.update = function() {
        Sprite.prototype.update.call(this);
        if ($gameSwitches.value(SW_MODE)) {
            this.visible = true;
            this.updateAppearance();
            this.processTouch();
            this.updateShake();
        } else {
            this.visible = false;
        }
    };

    Sprite_KyokoClicker.prototype.updateAppearance = function() {
        const ple = $gameVariables.value(VAR_PLEASURE);
        const max = $gameVariables.value(VAR_MAX_PLEASURE) || 100;
        const rate = ple / max;
        
        let level = 1;
        if (rate > 0.8) level = 4;
        else if (rate > 0.5) level = 3;
        else if (rate > 0.2) level = 2;
        
        if (this._currentLevel !== level) {
            this._currentLevel = level;
            const filenames = [
                "", 
                "kyoko_1_normal", 
                "kyoko_2_blush", 
                "kyoko_3_disheveled", 
                "kyoko_4_undress"
            ];
            const file = filenames[level];
            if (file) {
                this.bitmap = ImageManager.loadPicture(file);
            }
        }
    };

    Sprite_KyokoClicker.prototype.processTouch = function() {
        if (!TouchInput.isTriggered()) return;

        const { partId, isWeakPoint } = this.determineHitPart(TouchInput.x, TouchInput.y);
        $gameVariables.setValue(VAR_TARGET_PART, partId);

        if ($gameSwitches.value(SW_STEALTH)) {
            this.applySuspicion(TouchInput.x, TouchInput.y);
        } else {
            this.applyPleasure(TouchInput.x, TouchInput.y, isWeakPoint);
            $gameTemp.reserveCommonEvent(25); // 汎用演出イベント
        }
    };

    Sprite_KyokoClicker.prototype.determineHitPart = function(x, y) {
        // 部位判定ロジック（中心x=408想定）
        const centerX = 408; 
        const dx = Math.abs(x - centerX);
        
        let partId = 0;
        let isWeakPoint = false;

        // 耳の判定
        const isEar = (y >= 120 && y <= 180 && dx > 30 && dx < 80);
        // 胸の判定
        const isChest = (y >= 280 && y <= 360 && dx < 60);
        // 股間の判定
        const isCrotch = (y >= 460 && y <= 540 && dx < 50);

        if (isEar) {
            partId = 1;
            isWeakPoint = true;
        } else if (isChest) {
            partId = 2;
            isWeakPoint = true;
        } else if (isCrotch) {
            partId = 3;
            isWeakPoint = true;
        } else {
            // 弱点以外のエリア判定
            if (y < 220) partId = 1;
            else if (y < 420) partId = 2;
            else partId = 3;
        }
        
        return { partId, isWeakPoint };
    };

    Sprite_KyokoClicker.prototype.applyPleasure = function(x, y, isWeakPoint) {
        const lust = $gameVariables.value(VAR_LUST);
        const boost = 1 + (lust / 50);
        let baseGain = (2 + Math.randomInt(3));
        
        if (isWeakPoint) {
            baseGain *= 2;
            $gameScreen.startFlash([255, 255, 255, 150], 10);
        }

        const gain = Math.floor(baseGain * boost);
        $gameVariables.setValue(VAR_PLEASURE, $gameVariables.value(VAR_PLEASURE) + gain);
        $gameVariables.setValue(VAR_SHAME, $gameVariables.value(VAR_SHAME) + 1);

        this.spawnOnomato(x, y, false);
        this.playContextSE(false, isWeakPoint);
        this._shake = isWeakPoint ? 10 : 5;
    };

    Sprite_KyokoClicker.prototype.applySuspicion = function(x, y) {
        const current = $gameVariables.value(VAR_SUSPICION);
        $gameVariables.setValue(VAR_SUSPICION, current + 15);
        this.spawnOnomato(x, y, true);
        this.playContextSE(true, false);
        this._shake = 20;

        if ($gameVariables.value(VAR_SUSPICION) >= 100) {
            $gameTemp.reserveCommonEvent(CE_BUSTED);
        }
    };

    Sprite_KyokoClicker.prototype.updateShake = function() {
        if (this._shake > 0) {
            this.x = (Graphics.width / 2) + Math.randomInt(10) - 5;
            this._shake--;
            if (this._shake === 0) this.x = Graphics.width / 2;
        }
    };

    Sprite_KyokoClicker.prototype.spawnOnomato = function(x, y, isPanic) {
        const sprite = new Sprite_Onomato(x, y, isPanic);
        SceneManager._scene.addChild(sprite);
    };

    Sprite_KyokoClicker.prototype.playContextSE = function(isPanic, isWeakPoint) {
        let seName = "";
        if (isPanic) {
            seName = "vo_kyoko_surprise";
        } else {
            const part = $gameVariables.value(VAR_TARGET_PART);
            if (part === 1) seName = isWeakPoint ? "vo_kyoko_moan_ear" : "vo_kyoko_moan_head";
            else if (part === 2) seName = isWeakPoint ? "vo_kyoko_moan_chest" : "vo_kyoko_moan_there";
            else seName = isWeakPoint ? "vo_kyoko_moan_long" : "vo_kyoko_moan_low";
        }
        
        if (seName) {
            AudioManager.playSe({ name: seName, volume: 90, pitch: 100, pan: 0 });
        }
    };

    //-----------------------------------------------------------------------------
    // Sprite_Onomato
    // オノマトペ（擬音）をフェードアウトさせながら上昇させるスプライト
    //-----------------------------------------------------------------------------

    function Sprite_Onomato() {
        this.initialize(...arguments);
    }
    Sprite_Onomato.prototype = Object.create(Sprite.prototype);
    Sprite_Onomato.prototype.constructor = Sprite_Onomato;

    Sprite_Onomato.prototype.initialize = function(x, y, isPanic) {
        Sprite.prototype.initialize.call(this);
        let files = ["05.ん", "06.ああっ", "08.ぐちゅっ", "09.んっんっ", "10.ああん"];
        if (isPanic) files = ["03.ドドド", "07.ドキ", "02.ふわっ"];
        
        const file = files[Math.randomInt(files.length)];
        this.bitmap = ImageManager.loadPicture(file);
        this.x = x;
        this.y = y;
        this.anchor.x = 0.5;
        this.anchor.y = 0.5;
        this.scale.x = isPanic ? 1.5 : 1.0;
        this.scale.y = this.scale.x;
    };

    Sprite_Onomato.prototype.update = function() {
        Sprite.prototype.update.call(this);
        this.y -= 2;
        this.opacity -= 5;
        if (this.opacity <= 0 && this.parent) {
            this.parent.removeChild(this);
        }
    };

    //-----------------------------------------------------------------------------
    // Window_ArousalStatus
    // 快感度や警戒度を表示するウィンドウ
    //-----------------------------------------------------------------------------

    function Window_ArousalStatus() {
        this.initialize(...arguments);
    }
    Window_ArousalStatus.prototype = Object.create(Window_Base.prototype);
    Window_ArousalStatus.prototype.constructor = Window_ArousalStatus;

    Window_ArousalStatus.prototype.initialize = function(rect) {
        Window_Base.prototype.initialize.call(this, rect);
        this.opacity = 0;
    };

    Window_ArousalStatus.prototype.update = function() {
        Window_Base.prototype.update.call(this);
        if ($gameSwitches.value(SW_MODE)) {
            this.visible = true;
            this.refresh();
        } else {
            this.visible = false;
        }
    };

    Window_ArousalStatus.prototype.refresh = function() {
        this.contents.clear();
        this.contents.fontSize = 18;
        
        const lust = $gameVariables.value(VAR_LUST);
        const shame = $gameVariables.value(VAR_SHAME);
        const suspicion = $gameVariables.value(VAR_SUSPICION);

        this.drawConditionGauge(0, "快楽:", lust / 100, "#ff0000", "#ff8c00");
        this.drawConditionGauge(40, "羞恥:", shame / 100, "#800080", "#ff69b4");
        this.drawConditionGauge(80, "警戒:", suspicion / 100, "#0000ff", "#00ffff");
        
        if ($gameSwitches.value(SW_STEALTH)) {
            if (Graphics.frameCount % 40 < 20) {
                this.changeTextColor("#ff0000");
                this.drawText("！警戒中！", 10, 110, 140, "center");
            }
        }
    };

    Window_ArousalStatus.prototype.drawConditionGauge = function(y, label, rate, c1, c2) {
        this.changeTextColor(c2);
        this.drawText(label, 0, y, 60);
        const bg = ColorManager.gaugeBackColor();
        this.contents.fillRect(60, y + 14, 120, 10, bg);
        const fillW = Math.max(0, Math.min(120, Math.floor(120 * (rate || 0))));
        this.contents.gradientFillRect(60, y + 14, fillW, 10, c1, c2);
    };

    //-----------------------------------------------------------------------------
    // Sprite_StealthWarning
    // ステルスモード時の警告表示スプライト
    //-----------------------------------------------------------------------------

    function Sprite_StealthWarning() {
        this.initialize(...arguments);
    }
    Sprite_StealthWarning.prototype = Object.create(Sprite.prototype);
    Sprite_StealthWarning.prototype.constructor = Sprite_StealthWarning;

    Sprite_StealthWarning.prototype.initialize = function() {
        Sprite.prototype.initialize.call(this);
        this.bitmap = new Bitmap(200, 100);
        this.bitmap.fontSize = 48;
        this.bitmap.textColor = "#ff0000";
        this.bitmap.outlineColor = "#ffffff";
        this.bitmap.outlineWidth = 6;
        this.bitmap.drawText("！足音！", 0, 0, 200, 100, "center");
        this.x = Graphics.width / 2;
        this.y = 80;
        this.anchor.x = 0.5;
        this.anchor.y = 0.5;
        this.visible = false;
    };

    Sprite_StealthWarning.prototype.update = function() {
        Sprite.prototype.update.call(this);
        const dangerous = $gameSwitches.value(SW_STEALTH);
        this.visible = dangerous;
        if (dangerous) {
            this.opacity = 150 + Math.sin(Graphics.frameCount * 0.2) * 105;
            this.scale.x = 1.0 + Math.sin(Graphics.frameCount * 0.1) * 0.1;
            this.scale.y = this.scale.x;
        }
    };

    //-----------------------------------------------------------------------------
    // Scene_Map への統合
    //-----------------------------------------------------------------------------

    const _Scene_Map_createAllWindows = Scene_Map.prototype.createAllWindows;
    Scene_Map.prototype.createAllWindows = function() {
        _Scene_Map_createAllWindows.call(this);
        this.createClickerStatusWindow();
    };

    Scene_Map.prototype.createClickerStatusWindow = function() {
        const rect = new Rectangle(Graphics.width - 240, 60, 220, 160);
        this._arousalStatusWindow = new Window_ArousalStatus(rect);
        this.addWindow(this._arousalStatusWindow);
    };

    const _Scene_Map_createSpriteset = Scene_Map.prototype.createSpriteset;
    Scene_Map.prototype.createSpriteset = function() {
        _Scene_Map_createSpriteset.call(this);
        this._clickerSprite = new Sprite_KyokoClicker();
        this.addChild(this._clickerSprite);
        this._stealthWarning = new Sprite_StealthWarning();
        this.addChild(this._stealthWarning);
    };

})();
