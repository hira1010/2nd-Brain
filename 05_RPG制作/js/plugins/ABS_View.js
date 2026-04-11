/*:
 * @target MZ
 * @plugindesc ABS_View v2.0 (言霊シューター 強化版ビュー)
 * @author Antigravity
 * 
 * @help 描画とUIを担当するビュープラグインです。
 */

(() => {
    "use strict";

    window.ABS = window.ABS || {};

    // =========================================================================
    // 1. HUD (UI) スプライト
    // =========================================================================
    function Sprite_AbsHud() { this.initialize(...arguments); }
    Sprite_AbsHud.prototype = Object.create(Sprite.prototype);
    Sprite_AbsHud.prototype.constructor = Sprite_AbsHud;
    Sprite_AbsHud.prototype.initialize = function() {
        Sprite.prototype.initialize.call(this);
        this.bitmap = new Bitmap(Graphics.width, 150);
        this.bitmap.fontSize = 20;
        this.y = 20;
    };
    Sprite_AbsHud.prototype.update = function() {
        Sprite.prototype.update.call(this);
        if (!$gamePlayer || !ABS.State) return;
        this.bitmap.clear();
        
        const hp = Math.max(0, $gamePlayer._sHp || 0);
        const sp = Math.max(0, $gamePlayer._spG || 0);
        const lv = ABS.State.level || 1;
        const exp = ABS.State.exp || 0;
        const next = 50 + (lv * 30);
        
        // Background (コンパクト化: 200 -> 140)
        this.bitmap.fillRect(20, 0, 140, 8, "#333"); // HP
        this.bitmap.fillRect(20, 15, 140, 8, "#333"); // SP
        this.bitmap.fillRect(20, 30, 140, 4, "#333"); // EXP
        
        // Bars
        this.bitmap.fillRect(20, 0, 140 * (hp / 100), 8, "red");
        this.bitmap.fillRect(20, 15, 140 * (sp / 100), 8, "cyan");
        this.bitmap.fillRect(20, 30, 140 * (exp / next), 4, "yellow");
        
        // Text
        this.drawBorderedText(`Lv ${lv}`, 20, 40, "white");
        const weaponId = $gameVariables?.value(5) || 1;
        const wName = (ABS.WeaponData && ABS.WeaponData[weaponId]) ? ABS.WeaponData[weaponId].name : "None";
        this.drawBorderedText(`${wName}`, 80, 40, "orange");
    };

    Sprite_AbsHud.prototype.drawBorderedText = function(text, x, y, color) {
        this.bitmap.fontSize = 12; // フォントサイズを 12 に縮小
        this.bitmap.outlineColor = "black";
        this.bitmap.outlineWidth = 2;
        this.bitmap.textColor = color;
        this.bitmap.drawText(text, x, y, 200, 20, "left");
    };

    // =========================================================================
    // 2. シーン統合
    // =========================================================================
    const _Scene_Map_createSpriteset = Scene_Map.prototype.createSpriteset;
    Scene_Map.prototype.createSpriteset = function() {
        _Scene_Map_createSpriteset.call(this);
        this._absS = { p: {}, e: {}, o: {}, d: {} }; // Sprites: player, enemy, onoma, drops
        this._absL = { 
            p: new Sprite(), e: new Sprite(), o: new Sprite(), d: new Sprite() 
        };
        if (this._spriteset) {
            this._spriteset.addChild(this._absL.d); // Drops are bottom
            this._spriteset.addChild(this._absL.e);
            this._spriteset.addChild(this._absL.p);
            this._spriteset.addChild(this._absL.o); // Onomas are top
        }
        this._absHud = new Sprite_AbsHud();
        this.addChild(this._absHud);
    };

    const _Scene_Map_update = Scene_Map.prototype.update;
    Scene_Map.prototype.update = function() {
        _Scene_Map_update.call(this);
        if (!this.isActive() || SceneManager.isSceneChanging() || !ABS.State) return;
        
        ABS.M.update();
        this.renderABS();
        
        if ($gameMap && $gameMap.events) {
            $gameMap.events().forEach(e => {
                if (e && e.note && e.note.includes("<ABS>")) {
                    // 簡易AI
                    if (Math.random() < 0.01) this.enemyFire(e);
                }
            });
        }
    };

    Scene_Map.prototype.enemyFire = function (e) {
        if (!ABS.State || !ABS.State.eS) return;
        const p = $gamePlayer;
        const dist = Math.sqrt(Math.pow(e.x - p.x, 2) + Math.pow(e.y - p.y, 2));
        if (dist < 8) {
            ABS.State.eS.push({
                id: ABS.State.nextId++, x: e.x, y: e.y,
                tx: p.x, ty: p.y, pic: "12.バーン",
                speed: 0.1, power: 1, life: 60, frame: 0,
                curX: e.x, curY: e.y,
                scale: 0.5
            });
        }
    };

    Scene_Map.prototype.renderABS = function () {
        this.renderProj(ABS.State.pS, this._absS.p, this._absL.p);
        this.renderProj(ABS.State.eS, this._absS.e, this._absL.e);
        this.renderO(ABS.State.onomas, this._absS.o, this._absL.o);
        this.renderD(ABS.State.dropItems, this._absS.d, this._absL.d);
    };

    // Projectiles
    Scene_Map.prototype.renderProj = function (list, map, layer) {
        if (!list || !layer) return;
        const active = new Set();
        list.forEach(d => {
            active.add(d.id);
            if (!map[d.id]) {
                const s = new Sprite();
                s.bitmap = ImageManager.loadPicture(d.pic || "12.バーン");
                s.anchor.x = s.anchor.y = 0.5;
                map[d.id] = s; layer.addChild(s);
            }
            const s = map[d.id];
            s.scale.x = s.scale.y = d.scale || 1.0;
            s.x = $gameMap.adjustX(d.curX) * 48 + 24;
            s.y = $gameMap.adjustY(d.curY) * 48 + 24;
        });
        this.cleanup(map, layer, active);
    };

    // Onomatopoeias
    Scene_Map.prototype.renderO = function (list, map, layer) {
        if (!list || !layer) return;
        const active = new Set();
        list.forEach(d => {
            active.add(d.id);
            if (!map[d.id]) {
                const s = new Sprite();
                s.bitmap = new Bitmap(300, 80);
                // フォントサイズを極小の 10 へ縮小 (ナノ調整)
                s.bitmap.fontSize = d.fs || 10;
                s.bitmap.outlineColor = "black";
                s.bitmap.outlineWidth = 4;
                s.bitmap.drawText(d.text, 0, 0, 300, 80, "center");
                map[d.id] = s; layer.addChild(s);
            }
            const s = map[d.id];
            s.x = $gameMap.adjustX(d.x) * 48 - 150 + 24;
            s.y = $gameMap.adjustY(d.y) * 48 - 40 + 24;
            s.y -= (60 - d.life) * 0.8;
            s.opacity = d.life * 5;
        });
        this.cleanup(map, layer, active);
    };

    // Drops
    Scene_Map.prototype.renderD = function (list, map, layer) {
        if (!list || !layer) return;
        const active = new Set();
        list.forEach(d => {
            active.add(d.id);
            if (!map[d.id]) {
                const s = new Sprite();
                s.bitmap = new Bitmap(24, 24);
                const color = d.type === "exp" ? "yellow" : "red";
                s.bitmap.drawCircle(12, 12, 8, color);
                s.anchor.x = s.anchor.y = 0.5;
                map[d.id] = s; layer.addChild(s);
            }
            const s = map[d.id];
            s.x = $gameMap.adjustX(d.x) * 48 + 24;
            s.y = $gameMap.adjustY(d.y) * 48 + 24;
            s.scale.x = s.scale.y = 1.0 + Math.sin(Graphics.frameCount * 0.1) * 0.2;
        });
        this.cleanup(map, layer, active);
    };

    Scene_Map.prototype.cleanup = function (map, layer, active) {
        Object.keys(map).forEach(id => {
            if (!active.has(Number(id))) {
                layer.removeChild(map[id]);
                delete map[id];
            }
        });
    };

})();
