/*:
 * @target MZ
 * @plugindesc クリッカーエンジン EXTRA (Stealth Edition) - 精神・ささやき・オノマトペ・ステルス
 * @author Antigravity
 *
 * @param PleasureVariable
 * @text 快感度変数ID
 * @type variable
 * @default 9
 *
 * @param MaxPleasureVariable
 * @text 最大快感度変数ID
 * @type variable
 * @default 10
 *
 * @param LustVariable
 * @text 淫乱度変数ID
 * @type variable
 * @default 17
 *
 * @param ShameVariable
 * @text 羞恥心変数ID
 * @type variable
 * @default 16
 *
 * @param SuspicionVariable
 * @text 警戒度変数ID
 * @type variable
 * @default 19
 *
 * @help KyokoClickerEngine.js
 *
 * 【ステルス機能】
 * スイッチ10番がONの間は「足音警戒中」となります。
 * この間にクリックすると、快感の代わりに「警戒度（Variable 19）」が上昇します。
 * 警戒度が100に達すると、コモンイベント31番（発見イベント）が呼び出されます。
 */

(() => {
    "use strict";

    const pluginName = "KyokoClickerEngine";
    const parameters = PluginManager.parameters(pluginName);

    const VAR_PLEASURE = Number(parameters["PleasureVariable"] || 9);
    const VAR_MAX_PLEASURE = Number(parameters["MaxPleasureVariable"] || 10);
    const VAR_LUST = Number(parameters["LustVariable"] || 17);
    const VAR_SHAME = Number(parameters["ShameVariable"] || 16);
    const VAR_SUSPICION = Number(parameters["SuspicionVariable"] || 19);
    const VAR_TARGET_PART = Number(parameters["TargetPartVariable"] || 15);
    
    const SW_MODE = 9;
    const SW_STEALTH = 10;
    const CE_BUSTED = 31;

    //-----------------------------------------------------------------------------
    // Sprite_KyokoClicker (ステルス拡張版)
    //-----------------------------------------------------------------------------

    function Sprite_KyokoClicker() {
        this.initialize(...arguments);
    }

    Sprite_KyokoClicker.prototype = Object.create(Sprite.prototype);
    Sprite_KyokoClicker.prototype.constructor = Sprite_KyokoClicker;

    Sprite_KyokoClicker.prototype.initialize = function() {
        Sprite.prototype.initialize.call(this);
        // ボタン類
        this._whisperButton = new Sprite_Clickable();
        this._whisperButton.x = 200;
        this._whisperButton.y = 150;
        this._whisperButton.onClick = () => $gameTemp.reserveCommonEvent(26);
        this.addChild(this._whisperButton);

        this.anchor.x = 0.5;
        this.anchor.y = 0;
        this.x = Graphics.width / 2;
        this.y = 50;
        this.scale.x = 0.75;
        this.scale.y = 0.75;
        this._shake = 0;
        this._currentLevel = -1; // 現在表示中のレベルを記憶
    };

    Sprite_KyokoClicker.prototype.update = function() {
        Sprite.prototype.update.call(this);
        
        if ($gameSwitches.value(SW_CLICKER_MODE)) {
            this.visible = true;
            this.updateClicker();
            this.processTouch();
        } else {
            this.visible = false;
        }
    };

    Sprite_KyokoClicker.prototype.updateClicker = function() {
        const ple = $gameVariables.value(VAR_PLEASURE);
        const max = $gameVariables.value(VAR_MAX_PLEASURE) || 100;
        const rate = ple / max;
        
        let level = 1;
        if (rate > 0.8) level = 4;
        else if (rate > 0.5) level = 3;
        else if (rate > 0.2) level = 2;
        
        // レベルが変わった時だけ画像をロードする
        if (this._currentLevel !== level) {
            this._currentLevel = level;
            const files = ["", "kyoko_1_normal", "kyoko_2_blush", "kyoko_3_disheveled", "kyoko_4_undress"];
            const file = files[level];
            if (file) {
                this.bitmap = ImageManager.loadPicture(file);
            }
        }
    };

    Sprite_KyokoClicker.prototype.processTouch = function() {
        if (TouchInput.isTriggered()) {
            const tx = TouchInput.x;
            const ty = TouchInput.y;

            // --- 精密部位判定 (弱点システム) ---
            let partId = 0;
            let isWeakPoint = false;

            // 耳 (Ear)
            if (ty >= 120 && ty <= 180 && (Math.abs(tx - 408) > 30 && Math.abs(tx - 408) < 80)) {
                partId = 1;
                isWeakPoint = true;
            }
            // 胸 (Chest)
            else if (ty >= 280 && ty <= 360 && Math.abs(tx - 408) < 60) {
                partId = 2;
                isWeakPoint = true;
            }
            // 股間 (Crotch)
            else if (ty >= 460 && ty <= 540 && Math.abs(tx - 408) < 50) {
                partId = 3;
                isWeakPoint = true;
            }
            else if (ty < 220) partId = 1;
            else if (ty < 420) partId = 2;
            else partId = 3;

            $gameVariables.setValue(VAR_TARGET_PART, partId);

            if ($gameSwitches.value(SW_STEALTH)) {
                this.processBusted(tx, ty);
            } else {
                this.processPleasure(tx, ty, isWeakPoint);
                $gameTemp.reserveCommonEvent(25);
            }
        }

        if (this._shake > 0) {
            this.x = (Graphics.width / 2) + Math.randomInt(10) - 5;
            this._shake--;
            if (this._shake === 0) this.x = Graphics.width / 2;
        }
    };

    Sprite_KyokoClicker.prototype.processPleasure = function(x, y, isWeakPoint) {
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

        this.showOnomato(x, y, false);
        this.playMoan(false, isWeakPoint);
        this._shake = isWeakPoint ? 10 : 5;
    };

    Sprite_KyokoClicker.prototype.processBusted = function(x, y) {
        const currentSuspicion = $gameVariables.value(VAR_SUSPICION);
        $gameVariables.setValue(VAR_SUSPICION, currentSuspicion + 15);
        this.showOnomato(x, y, true);
        this.playMoan(true, false);
        this._shake = 20;

        if ($gameVariables.value(VAR_SUSPICION) >= 100) {
            $gameTemp.reserveCommonEvent(CE_BUSTED);
        }
    };

    Sprite_KyokoClicker.prototype.showOnomato = function(x, y, isPanic) {
        const sprite = new Sprite();
        let files = ["05.ん", "06.ああっ", "08.ぐちゅっ", "09.んっんっ", "10.ああん"];
        if (isPanic) files = ["03.ドドド", "07.ドキ", "02.ふわっ"];
        
        const file = files[Math.randomInt(files.length)];
        sprite.bitmap = ImageManager.loadPicture(file);
        sprite.x = x;
        sprite.y = y;
        sprite.anchor.x = 0.5;
        sprite.anchor.y = 0.5;
        sprite.scale.x = isPanic ? 1.5 : 1.0;
        sprite.scale.y = isPanic ? 1.5 : 1.0;
        sprite.opacity = 255;
        
        // MZ Sprite update
        sprite.update = function() {
             this.y -= 2;
             this.opacity -= 5;
             if (this.opacity <= 0 && this.parent) {
                 this.parent.removeChild(this);
             }
        };
        
        SceneManager._scene.addChild(sprite);
    };

    Sprite_KyokoClicker.prototype.playMoan = function(isPanic, isWeakPoint) {
        let seName = "";
        if (isPanic) {
            seName = "vo_kyoko_surprise";
        } else {
            const part = $gameVariables.value(VAR_TARGET_PART);
            
            // 部位と弱点判定による分岐
            if (part === 1) { // 頭/耳
                seName = isWeakPoint ? "vo_kyoko_moan_ear" : "vo_kyoko_moan_head";
            } else if (part === 2) { // 胸
                seName = isWeakPoint ? "vo_kyoko_moan_chest" : "vo_kyoko_moan_there";
            } else { // 下半身/股間
                seName = isWeakPoint ? "vo_kyoko_moan_long" : "vo_kyoko_moan_low";
            }
        }
        
        if (seName) {
            try {
                // ロードエラー対策: 確実にオーディオが存在するかチェックし、エラーなら無視する
                AudioManager.playSe({ name: seName, volume: 90, pitch: 100, pan: 0 });
            } catch (e) {
                console.warn("SE Playback failed:", seName);
            }
        }
    };

    //-----------------------------------------------------------------------------
    // Window_ArousalStatus (ステルス対応リファクタ)
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

        this.changeTextColor("#ff8c00");
        this.drawText("淫乱:", 0, 0, 60);
        this.drawCustomGauge(60, 0, 120, lust / 100, "#ff0000", "#ff8c00");

        this.changeTextColor("#ff69b4");
        this.drawText("羞恥:", 0, 40, 60);
        this.drawCustomGauge(60, 40, 120, shame / 100, "#800080", "#ff69b4");

        this.changeTextColor("#00ffff");
        this.drawText("警戒:", 0, 80, 60);
        this.drawCustomGauge(60, 80, 120, suspicion / 100, "#0000ff", "#00ffff");
        
        if ($gameSwitches.value(SW_STEALTH)) {
            if (Graphics.frameCount % 40 < 20) {
                this.changeTextColor("#ff0000");
                this.drawText("！警戒中！", 10, 110, 140, "center");
                // 画面端にも大きな警告を表示するためのフラグや演出を足せる
            }
        }
    };

    // 画面中央付近に警告アイコンを表示する追加スプライト
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
        this.x = Graphics.width / 2 - 100;
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

    Window_ArousalStatus.prototype.drawCustomGauge = function(x, y, w, rate, c1, c2) {
        const bg = ColorManager.gaugeBackColor();
        this.contents.fillRect(x, y + 14, w, 10, bg);
        const fillW = Math.max(0, Math.min(w, Math.floor(w * (rate || 0))));
        this.contents.gradientFillRect(x, y + 14, fillW, 10, c1, c2);
    };

    // Scene_Map への追加 (安全な初期化)
    const _Scene_Map_createAllWindows = Scene_Map.prototype.createAllWindows;
    Scene_Map.prototype.createAllWindows = function() {
        _Scene_Map_createAllWindows.call(this);
        this.createArousalWindow();
    };

    Scene_Map.prototype.createArousalWindow = function() {
        const w = 220;
        const h = 160;
        const x = Graphics.width - w - 20;
        const y = 60;
        const rect = new Rectangle(x, y, w, h);
        this._arousalStatusWindow = new Window_ArousalStatus(rect);
        this.addWindow(this._arousalStatusWindow);
    };

    const _Scene_Map_onMapLoaded = Scene_Map.prototype.onMapLoaded;
    Scene_Map.prototype.onMapLoaded = function() {
        _Scene_Map_onMapLoaded.call(this);
        if ($gameSwitches.value(SW_MODE)) {
            $gameScreen.startFadeIn(1);
        }
    };

    // Sprite登録
    const _Scene_Map_createSpriteset = Scene_Map.prototype.createSpriteset;
    Scene_Map.prototype.createSpriteset = function() {
        _Scene_Map_createSpriteset.call(this);
        this._clickerSprite = new Sprite_KyokoClicker();
        this.addChild(this._clickerSprite);
        
        // 足音警告スプライトを追加
        this._stealthWarning = new Sprite_StealthWarning();
        this.addChild(this._stealthWarning);
    };

})();
