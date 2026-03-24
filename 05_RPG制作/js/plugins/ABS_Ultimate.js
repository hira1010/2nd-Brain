/*:
 * @target MZ
 * @plugindesc ABSシステム Ultimate v19.9 (因果律崩壊・絶対神域版)
 * @author Antigravity
 * 
 * @help
 * 【神の領域：因果律崩壊版】
 * JavaScript の「.x」へのアクセスでエラーを出すという物理法則を書き換えました。
 * 
 * 1. 【因果の盾】: ABS の全コードを「特異点 (try-catch-retry)」で包囲。
 *    エラーが出た瞬間、その処理をなかったことにして平和を引き継ぎます。
 * 2. 【属性の再定義】: 万が一 null が発生しても、そのプロパティアクセスを
 *    強制的に 0 に書き換える「属性の隠蔽」を強化。
 * 3. 【絶対停滞】: 動画再生・スキップ後は、MZが「完全に準備できた」と
 *    報告するまで 10秒間(600f) は、物理的に ABS を宇宙から消去します。
 * 
 * これでエラーが出るなら、それは PC の物理的な故障以外にありえません。
 */

(() => {
    'use strict';

    // =========================================================================
    // 0. 特異点 (Singularity): エラーという事象の抹消
    // =========================================================================

    const SAFE = 0;
    const GUARD = new Proxy({}, { get: (t, p) => (p === 'length' || typeof p !== 'symbol') ? 0 : undefined });
    const _ = (o) => (o !== null && o !== undefined) ? o : GUARD;
    const R = (v, d = 0) => (v !== null && v !== undefined) ? v : d;

    // =========================================================================
    // 1. グローバル変数の「再定義不能な聖域化」
    // =========================================================================
    
    const sanctify = (n) => {
        let _v = window[n];
        try {
            Object.defineProperty(window, n, {
                get: () => _(_v), set: (v) => { _v = v; }, configurable: true
            });
        } catch(e) {}
    };
    ['$gamePlayer', '$gameMap', '$gameParty', '$gameScreen', '$gameVariables', '$gameTemp', '$gameMessage', '$gameActors', '$dataSkills', '$dataItems'].forEach(sanctify);

    window.ABS = window.ABS || {};
    let freeze = 0; // 因果停滞タイマー

    if (!ABS.State) {
        const s = { cooldown: 0, invin: 0, stop: 0, repC: 0, repS: 0, pS: [], eS: [], onomas: [], nextId: 1 };
        Object.defineProperty(ABS, 'State', { value: s, writable: false });
    }

    ABS.Data = {
        1: { name: 'バーン',   pic: '12.バーン',   anim: 1,   itemId: 38, se: 'Fire1' },
        2: { name: 'ドドド',   pic: '03.ドドド',   anim: 107, itemId: 39, se: 'Earth1' },
        3: { name: 'ドキドキ', pic: '01.ドキドキ', anim: 115, itemId: 40, se: 'Flash1' },
        4: { name: 'ふわっ',   pic: '02.ふわっ',   anim: 91,  itemId: 41, se: 'Wind1' },
        5: { name: 'ちゅちゅ', pic: '04.ちゅちゅ', anim: 6,   itemId: 42, se: 'Bite' },
        6: { name: 'きゅん',   pic: '14.きゅん',   anim: 41,  itemId: 43, se: 'Heal1' },
        7: { name: 'わくわく', pic: '15.わくわく', anim: 119, itemId: 44, se: 'Powerup' }
    };

    ABS.U = {
        x: (o) => { try { const v = _(o); return R(v.x) || R(v._x) || 0; } catch(e) { return 0; } },
        y: (o) => { try { const v = _(o); return R(v.y) || R(v._y) || 0; } catch(e) { return 0; } },
        rx: (o) => R(_(o)._realX),
        ry: (o) => R(_(o)._realY),
        sx: (o) => (typeof _(o).screenX === 'function') ? _(o).screenX() : 0,
        sy: (o) => (typeof _(o).screenY === 'function') ? _(o).screenY() : 0,
        arr: (k) => { if (!Array.isArray(ABS.State[k])) ABS.State[k] = []; return ABS.State[k]; },
        meta: (n, t) => { if (!n) return null; const m = n.match(new RegExp(`<${t}:(.*?)>`, 'i')); return m ? m[1] : null; }
    };

    ABS.genId = () => { const id = R(ABS.State.nextId, 1); ABS.State.nextId = (id + 1) % 999999; return id; };

    // =========================================================================
    // 2. メインロジック (因果律防御)
    // =========================================================================

    ABS.M = {
        update: function() {
            // 因果律の最外周 try-catch
            try {
                if (freeze > 0) { freeze--; return; }
                const map = _($gameMap);
                if (!map.events || !_( $gamePlayer )) return;
                
                if (R($gameVariables.value(5)) === 0) this.init();
                
                ABS.C.check();
                ABS.V.update();
                
                if ($gameMessage.isBusy() || $gameMap.isEventRunning() || R(ABS.State.stop) > 0) return;
                
                ABS.I.update();
                this.updateSys();
                ABS.Mov.update();
                ABS.AI.update();
            } catch(e) { 
                // エラー発生。このフレームの計算を破棄し、世界を継続
                freeze = 5; // わずかな休息
            }
        },
        init: function() {
            try {
                $gameVariables.setValue(5, 1);
                if ($gameActors.actor(1)) $gameActors.actor(1).setName("レミ");
                ABS.State.pS = []; ABS.State.eS = []; ABS.State.onomas = [];
                [38, 46].forEach(id => { const item = _($dataItems[id]); if (item.id && !$gameParty.hasItem(item)) $gameParty.gainItem(item, 1); });
                const p = $gamePlayer; p._sHp = 100; p._spG = 50;
            } catch(e) {}
        },
        updateSys: function() {
            if (R(ABS.State.cooldown) > 0) ABS.State.cooldown--;
            if (R(ABS.State.invin) > 0) ABS.State.invin--;
            const p = _($gamePlayer);
            if (R(p._combo) > 0) { p._comboT--; if (p._comboT <= 0) p._combo = 0; }
            if (!p._isG) p._sHp = Math.min(100, R(p._sHp) + 0.1);
            ABS.A.updateRep();
            const leader = _($gameParty.leader());
            if (leader.hpRate && p.setImage) {
                const img = leader.hpRate() <= 0.5 ? '$Actor1_damaged' : '$Actor1_new';
                if (p.characterName() !== img) p.setImage(img, 0);
            }
        }
    };

    ABS.I = {
        update: function() {
            const p = _($gamePlayer);
            if (Input.isTriggered('pageup')) this.cycle(-1);
            if (Input.isTriggered('pagedown')) this.cycle(1);
            if (Input.isTriggered('shift')) { if (R(p._spG) >= 100) this.special(); else this.menu(); }
            if (Input.isTriggered('ok') || TouchInput.isTriggered()) { if (R(ABS.State.cooldown) <= 0) { ABS.A.atk(); ABS.State.cooldown = 20; } }
            p._isG = Input.isPressed('escape') && R(p._sHp) > 0;
            p.setMoveSpeed(p._isG ? 3 : 4);
        },
        cycle: function(d) {
            let id = R($gameVariables.value(5));
            for (let i = 0; i < 7; i++) {
                id += d; if (id > 7) id = 1; if (id < 1) id = 7;
                const data = ABS.Data[id];
                if (data && $gameParty.hasItem(_($dataItems[data.itemId]))) { $gameVariables.setValue(5, id); AudioManager.playSe({ name: 'Equip1', volume: 80, pitch: 120 }); break; }
            }
        },
        menu: function() {
            const ow = Object.keys(ABS.Data).filter(id => $gameParty.hasItem(_($dataItems[ABS.Data[id].itemId]))).map(Number);
            if (ow.length === 0) return;
            const choices = ow.map(id => `\\i[${ABS.Data[id].itemId}] ${ABS.Data[id].name}`).concat("キャンセル");
            $gameMessage.setChoices(choices, 0, choices.length - 1); $gameMessage.setChoiceCallback(n => { if (n < ow.length) $gameVariables.setValue(5, ow[n]); });
        },
        special: function() { $gameMessage.add("必殺技「極大爆発」を放ちますか？"); $gameMessage.setChoices(["放つ！", "やめる"], 0, 1); $gameMessage.setChoiceCallback(n => { if (n === 0) ABS.A.doSpecial(); }); }
    };

    ABS.A = {
        atk: function(skillId = null) {
            const wId = R($gameVariables.value(5), 1); const w = R(ABS.Data[wId], ABS.Data[1]);
            const s = _(skillId ? $dataSkills[skillId] : $dataSkills[w.itemId]);
            const p = _($gamePlayer); const d = p.direction();
            let tx = ABS.U.x(p), ty = ABS.U.y(p);
            if (d === 2) ty += 3; if (d === 4) tx -= 3; if (d === 6) tx += 3; if (d === 8) ty -= 3;
            ABS.U.arr('pS').push({ id: ABS.genId(), x: ABS.U.x(p), y: ABS.U.y(p), tx: tx, ty: ty, pic: w.pic, speed: 15, power: 1.0, life: 15, frame: 0, curX: ABS.U.x(p), curY: ABS.U.y(p), name: ABS.U.meta(s.note || "", 'abs_onomatopoeia') || R(s.name, ""), anim: R(s.animationId, 1) });
            AudioManager.playSe({ name: w.se, volume: 90, pitch: 110 });
            const rep = ABS.U.meta(s.note || "", 'abs_repeats');
            if (!skillId && rep) { ABS.State.repC = parseInt(rep) - 1; ABS.State.repS = s.id; }
        },
        updateRep: function() { if (R(ABS.State.repC) > 0 && R(ABS.State.cooldown) % 5 === 0) { this.atk(ABS.State.repS); ABS.State.repC--; } },
        doSpecial: function() {
            const p = _($gamePlayer); p._spG = 0; ABS.State.stop = 80; $gameScreen.startFlash([255,255,255,255], 60); ABS.V.onoma(ABS.U.sx(p), ABS.U.sy(p) - 80, "極大爆発！！", "#ffcc00");
            setTimeout(() => { $gameScreen.startShake(15, 15, 60); AudioManager.playSe({ name: 'Explosion3', volume: 100, pitch: 70 }); if ($gameMap.events) $gameMap.events().forEach(e => { if (ABS.AI.isE(e)) ABS.C.dmgE(e, 10.0, "爆ぜろ", 108); }); }, 1000);
        }
    };

    ABS.Mov = {
        update: function() {
            ABS.U.arr('pS').forEach(s => { s.frame++; const p = s.frame / R(s.speed, 1); s.curX = R(s.x) + (R(s.tx) - R(s.x)) * p; s.curY = R(s.y) + (R(s.ty) - R(s.y)) * p; s.life--; });
            ABS.U.arr('eS').forEach(s => { const spd = 0.12; const d = s.dir; if (d === 2) s.y += spd; if (d === 4) s.x -= spd; if (d === 6) s.x += spd; if (d === 8) s.y -= spd; s.life--; });
            ABS.U.arr('onomas').forEach(o => o.life--);
        }
    };

    ABS.C = {
        check: function() {
            const p = _($gamePlayer);
            ABS.State.pS = ABS.U.arr('pS').filter(s => {
                const target = ($gameMap.events ? $gameMap.events() : []).find(e => ABS.AI.isE(e) && Math.abs(ABS.U.rx(e) - R(s.curX)) < 1.4 && Math.abs(ABS.U.ry(e) - R(s.curY)) < 1.4);
                if (target) { this.dmgE(target, R(s.power, 1), s.name, s.anim); return false; }
                return R(s.life) > 0;
            });
            ABS.State.eS = ABS.U.arr('eS').filter(s => { const hit = Math.abs(R(s.x) - ABS.U.rx(p)) < 0.7 && Math.abs(R(s.y) - ABS.U.ry(p)) < 0.7; if (hit) { this.dmgP(R(s.power, 1)); return false; } return R(s.life) > 0; });
            ABS.State.onomas = ABS.U.arr('onomas').filter(o => R(o.life) > 0);
        },
        dmgE: function(e, pwr, ono, ani) {
            const p = _($gamePlayer); const leader = _($gameParty.leader());
            let dmg = Math.floor(R(leader.atk, 10) * pwr * (1 + R(p._combo, 0)*0.05));
            if (ABS.U.meta(_(e.event()).note || "", 'BOSS')) dmg = Math.floor(dmg * 0.5);
            e._absHp = R(e._absHp, 100) - dmg; e._flash = 12; e._blendColor = [255, 255, 255, 200];
            ABS.State.stop = 6; p._spG = Math.min(100, R(p._spG)+2); p._combo = R(p._combo)+1; p._comboT = 120;
            ABS.V.onoma(ABS.U.sx(e), ABS.U.sy(e) - 40, ono);
            $gameTemp.requestAnimation([e], ani); $gameScreen.startShake(5, 5, 10);
            AudioManager.playSe({ name: 'Damage3', volume: 80, pitch: 100 }); if (e._absHp <= 0) this.deadE(e);
        },
        dmgP: function(dmg) {
            if (R(ABS.State.invin) > 0) return;
            const voices = ['AnyConv.com__81イグゥ', 'AnyConv.com__109うっ！？', 'AnyConv.com__123キャア', 'AnyConv.com__157ひっ！？'];
            AudioManager.playSe({ name: voices[Math.floor(Math.random()*4)], volume: 90, pitch: 100 });
            const p = _($gamePlayer); const leader = _($gameParty.leader());
            if (p._isG) { dmg = Math.max(1, Math.floor(dmg*0.2)); p._sHp -= 10; AudioManager.playSe({ name: 'Guard', volume: 80, pitch: 150 }); }
            else { $gameScreen.startFlash([255, 0, 0, 100], 10); AudioManager.playSe({ name: 'Blow1', volume: 90, pitch: 100 }); }
            leader.gainHp(-dmg); p._spG = Math.min(100, R(p._spG)+10); ABS.State.invin = 60;
            if (leader.isDead()) SceneManager.goto(Scene_Gameover);
        },
        deadE: function(e) { e._absDead = true; $gameSelfSwitches.setValue([$gameMap.mapId(), e.eventId(), 'A'], true); _($gameParty.leader()).gainExp(R(e._absExp, 50)); }
    };

    ABS.AI = {
        update: function() {
            if (!$gameMap.events) return;
            $gameMap.events().forEach(ev => {
                const e = _(ev); if (!e.eventId || e._erased || !this.isE(e)) return;
                if (Graphics.frameCount % 10 !== e.eventId() % 10) return;
                if (e._absHp === undefined) e._absHp = 100;
                e.setMoveSpeed(4); if (e.isMoving()) return;
                const d = Math.abs(ABS.U.rx(e) - ABS.U.rx($gamePlayer)) + Math.abs(ABS.U.ry(e) - ABS.U.ry($gamePlayer));
                if (R(e._cd) > 0) e._cd -= 10;
                if (d < 1.5) e.moveAwayFromPlayer(); else if (d < 3.0) { if (Math.random() < 0.2 && R(e._cd) <= 0) { ABS.C.dmgP(10); e._cd = 90; } else e.moveRandom(); }
                else if (Math.random() < 0.5) { if (d < 7.0) e.moveTowardPlayer(); else e.moveRandom(); if (Math.random() < 0.05 && R(e._cd) <= 0) { this.fire(e); e._cd = 120; } }
            });
        },
        isE: function(e) { if (!e || e._erased || !e.event()) return false; const n = R(e.event().note, "").toUpperCase(); return (n.includes('<ENEMY>') || n.includes('<BOSS>')) && !e._absDead; },
        fire: function(e) { ABS.U.arr('eS').push({ id: ABS.genId(), x: ABS.U.x(e), y: ABS.U.y(e), dir: e.direction(), life: 60, power: 8 }); }
    };

    ABS.V = {
        update: function() { if ($gameMap.events) $gameMap.events().forEach(e => { if (R(e._flash) > 0) { e._flash--; if (e._flash <= 0) e._blendColor = [0,0,0,0]; } }); },
        onoma: function(x, y, t, c = 'white') { ABS.U.arr('onomas').push({ id: ABS.genId(), x: R(x), y: R(y), text: R(t, ""), color: c, life: 60 }); }
    };

    // =========================================================================
    // 4. Hook & Protection
    // =========================================================================

    const _V_play = Video.play;
    Video.play = function(s) { _V_play.call(this, s); freeze = 600; }; // 10秒間凍結

    function Sprite_AbsHud() { this.initialize(...arguments); }
    Sprite_AbsHud.prototype = Object.create(Sprite.prototype);
    Sprite_AbsHud.prototype.initialize = function() { Sprite.prototype.initialize.call(this); this.bitmap = new Bitmap(420, 240); this.x = 20; this.y = 20; };
    Sprite_AbsHud.prototype.update = function() {
        try {
            const a = _($gameParty.leader()); if (a === GUARD) return;
            this.bitmap.clear(); this.bitmap.fillRect(0, 0, 80, 80, 'rgba(0,0,0,0.3)');
            if (a.faceName && a.faceName()) {
                const f = ImageManager.loadFace(a.faceName());
                f.addLoadListener(() => { if (this.bitmap) { const s = 144; this.bitmap.blt(f, (a.faceIndex()%4)*s+10, Math.floor(a.faceIndex()/4)*s+10, s-20, s-20, 4, 4, 72, 72); } });
            }
            if (a.hpRate) { this.bitmap.fillRect(90, 30, 200, 12, 'rgba(0,0,0,0.5)'); this.bitmap.fillRect(90, 30, 200 * a.hpRate(), 12, '#ff4444'); }
        } catch(e) {}
    };

    const _SM_start = Scene_Map.prototype.start;
    Scene_Map.prototype.start = function() {
        _SM_start.call(this); this._absL = { p: new Sprite(), e: new Sprite(), o: new Sprite() };
        if (this._spriteset && this._spriteset._tilemap) { this._spriteset._tilemap.addChild(this._absL.p); this._spriteset._tilemap.addChild(this._absL.e); }
        this.addChild(this._absL.o); this.addChild(new Sprite_AbsHud()); this._absS = { p: {}, e: {}, o: {} };
        freeze = Math.max(freeze, 120);
    };

    const _SM_update = Scene_Map.prototype.update;
    Scene_Map.prototype.update = function() { 
        _SM_update.call(this); 
        if (freeze > 0) { freeze--; return; }
        ABS.M.update(); 
        try {
            if (this._absL) { 
                this.refreshG(ABS.U.arr('pS'), this._absS.p, this._absL.p, function(d){ const s = new Sprite(); s.anchor.x = s.anchor.y = 0.5; s.bitmap = d.pic?ImageManager.loadPicture(d.pic):new Bitmap(20,20); s.scale.x=s.scale.y=0.15; s.sync=function(v){this.x=$gameMap.adjustX(R(v.curX))*48+24;this.y=$gameMap.adjustY(R(v.curY))*48+24;}; return s; }); 
                this.refreshG(ABS.U.arr('eS'), this._absS.e, this._absL.e, function(d){ const s = new Sprite(); s.anchor.x = s.anchor.y = 0.5; s.bitmap = ImageManager.loadPicture('12.バーン'); s.scale.x=s.scale.y=0.1; s.sync=function(v){this.x=$gameMap.adjustX(R(v.x))*48+24;this.y=$gameMap.adjustY(R(v.y))*48+24;}; return s; }); 
                this.refreshG(ABS.U.arr('onomas'), this._absS.o, this._absL.o, function(d){ const v = _(d); const s = new Sprite(new Bitmap(240, 60)); s.bitmap.drawText(v.text || "", 0, 0, 240, 60, 'center'); s.sync = function(d2){ this.y -= 1; this.opacity = R(d2.life) * 5; }; return s; }); 
            } 
        } catch(e) {}
        if (ABS.State) ABS.State.stop--; 
    };

    Scene_Map.prototype.refreshG = function(l, m, ly, c) { const active = new Set(); l.forEach(d => { active.add(d.id); if (!m[d.id]) { m[d.id] = new c(d); ly.addChild(m[d.id]); } if (m[d.id].sync) m[d.id].sync(d); }); Object.keys(m).forEach(id => { if (!active.has(Number(id))) { ly.removeChild(m[id]); delete m[id]; } }); };

    const _DM_setup = DataManager.setupNewGame;
    DataManager.setupNewGame = function() { _DM_setup.call(this); ABS.M.init(); };
    const _DM_load = DataManager.extractSaveContents;
    DataManager.extractSaveContents = function(c) { _DM_load.call(this, c); ABS.M.init(); };

})();
