/**
 * 
 * 
 */



// 移動可能か否かの判定を行う。特定のアイテムを所持しているときに移動可能になるようなルーチンを組む。
// TODO Game_Player.prototype.canMove


// プレイヤーの向きのみ変更（Shiftキー押下時）
// ミニマップの実装完了


(() => {
    console.log("RogueLike.js: Loading start...");

    // ゲーム内定数とユーティリティ
    const RL = {
        COLLISION_DISTANCE: 1,
        TILESET_ID_DUNGEON: 4,
        VAR_CLOTHING_DAMAGE: 15, // 衣装耐久度（加算値）
        
        getActor: () => $gameActors.actor(1),
        
        playVoice: (category) => {
            let name = "";
            if (category === "damage") {
                const r = Math.random();
                // コピーした音声ファイル名
                name = r < 0.5 ? "v_damage_01" : "v_damage_02";
            } else if (category === "peak") {
                name = "v_peak_01";
            }
            if (name) {
                AudioManager.playSe({ name: name, volume: 90, pitch: 100, pan: 0 });
            }
        },

        log: (text) => {
            if (SceneManager._scene._actionLogWindow) {
                SceneManager._scene._actionLogWindow.pushTextInfo({ 
                    aName: null, aColoer: null, aDamage: 0, tName: null, tColoer: null, tDamage: 0, 
                    text: text, kill: false, guard: false 
                });
                SceneManager._scene._actionLogWindow.drawTextInfomation();
            }
        }
    };

    let Fturn = 1;
    let Eturn = 1;
    const FRIEND = true;
    const ENEMY = false;
    let target = null;
    let guard = false;
    let _onomatopoeias = []; // 追加: 発射中のオノマトペ管理用

    // AI 行動定数
    const ACTION = {
        STOP: 0,
        MOVE: 1,
        TURN: 2,
        ATTACK: 3,
        USE_ITEM: 4,
        USE_SKILL: 5,
        TRACK: 6 // 追跡
    };

    // アクションログ用定数
    const TEXTHEIGHT = 30;
    let TEXTINFO = [];
    const JOINT = "を";
    const ATTACK_TEXT = "攻撃";
    const DAMAGE_TEXT = "ダメージ！";
    const KILL_TEXT = "倒した！";
    const GUARD_TEXT = "防御！";
    const TEXT_JOINT = "：";

    const _Game_Player_initMembers = Game_Player.prototype.initMembers;
    Game_Player.prototype.initMembers = function () {
        _Game_Player_initMembers.call(this);
        this._attackMotion = false;
        this._moving = false;
        this._onomatopoeiaType = 0; // 0: ドカン, 1: スッ, 2: バガン
    };

    const _Game_Event_initMembers = Game_Event.prototype.initMembers;
    Game_Event.prototype.initMembers = function () {
        _Game_Event_initMembers.call(this);
        this._attackMotion = false;
        this._moving = false;
    };

    // ダッシュの禁止
    Game_Player.prototype.isDashRequested = function () {
        return false;
    };

    function consumptionTurn(isFriend) {
        if (isFriend) {
            Fturn += 1;
        } else {
            Eturn += 1;
        }
    };

    class Game_MapEnemy {
        constructor(event) {
            this._event = event;
            const evData = event.event();
            this._isEnemy = evData && evData.name.indexOf("enemy") != -1;
            this._enemyId = evData ? Number(evData.meta.id) : 0;
            this._enemyData = $dataEnemies[this._enemyId];
            this._actionEnd = false;
            this._isBoss = (evData && evData.meta.boss) ? true : false;
            this._sight = (evData && evData.meta.sight) ? Number(evData.meta.sight) : 5;
            
            // 追跡用の最後にプレイヤーを見た座標
            this._lastSeenX = -1;
            this._lastSeenY = -1;

            if (this._enemyData) {
                const mag = Math.max($gameVariables.value(33), 10);
                this._hp = Math.round(this._enemyData.params[0] * mag / 10);
                this._mp = Math.round(this._enemyData.params[1] * mag / 10);
            } else {
                this._hp = 0;
                this._mp = 0;
            }
        }

        isAlive() {
            return this._hp > 0;
        }

        takeDamage(damage) {
            guard = false;
            this._hp -= damage;
        }

        /**
         * 最後にプレイヤーを見た場所へ向かう
         */
        trackToLastSeen() {
            if (this._lastSeenX >= 0) {
                const direction = this._event.findDirectionTo(this._lastSeenX, this._lastSeenY);
                if (direction > 0) {
                    this._event.moveStraight(direction);
                    // 到着したら追跡座標をリセット
                    if (this._event.x === this._lastSeenX && this._event.y === this._lastSeenY) {
                        this._lastSeenX = -1;
                        this._lastSeenY = -1;
                    }
                }
            }
        }
    }

    const _Game_Player_reserveTransfer = Game_Player.prototype.reserveTransfer;
    Game_Player.prototype.reserveTransfer = function (mapId, x, y, d, fadeType) {
        _Game_Player_reserveTransfer.call(this, mapId, x, y, d, fadeType);
        Fturn = 1;
        Eturn = 1;
    };

    const _Game_Map_setupEvents = Game_Map.prototype.setupEvents;
    Game_Map.prototype.setupEvents = function () {
        _Game_Map_setupEvents.call(this);
        if ($gameMap._tilesetId == 4) {
            this.makeEnemy();
        }
        
    };

    Game_Map.prototype.makeEnemy = function () {
        this._enemyMapObjects = this.events().map((event) =>
            new Game_MapEnemy(event)
        );
    };

    const _Game_Player_update_original = Game_Player.prototype.update;
    Game_Player.prototype.update = function (sceneActive) {
        const wasMoving = this.isMoving();
        _Game_Player_update_original.call(this, sceneActive);
        
        // オノマトペの更新（弾道移動と衝突判定）
        this.updateOnomatopoeias();

        if (this._attackMotion && !this._moving) {
            this.attackMotion();
            this._moving = true;
        }
        if (!this.isMoving()) {
            if (wasMoving) {
                this._moving = false;
                this._attackMotion = false;
                this.clearPicture();
                
                // ターン終了時に敵の視界を更新
                if ($gameMap._enemyMapObjects) {
                    $gameMap._enemyMapObjects.forEach(enemy => {
                        if (enemy.isAlive() && enemy._event.canSeeTarget(this)) {
                            enemy._lastSeenX = this.x;
                            enemy._lastSeenY = this.y;
                        }
                    });
                }

                consumptionTurn(FRIEND);
            }
        }

        if (this._moving) {
            return;
        }
        if (this.triggerButtonAction()) {
            return;
        }
        this.updateThrowInput(); // Qキーによる投擲入力
        this.moveByInput();
    };

    /**
     * ダッシュを禁止する
     */
    Game_Player.prototype.updateDashing = function() {
        this._dashing = false;
    };

    /**
     * 入力による移動処理を拡張
     */
    Game_Player.prototype.moveByInput = function() {
        if (!this.isMoving() && this.canMove()) {
            let direction = this.getInputDirection();
            if (direction > 0) {
                $gameTemp.clearDestination();
                // Shiftキーが押されている場合は向き変更のみ
                if (Input.isPressed("shift")) {
                    this.setDirection(direction);
                    return;
                }
            } else if ($gameTemp.isDestinationValid()) {
                // タッチ移動を無効化、または制限（ここでは一応クリアする）
                $gameTemp.clearDestination();
                /*
                const x = $gameTemp.destinationX();
                const y = $gameTemp.destinationY();
                direction = this.findDirectionTo(x, y);
                */
            }
            if (direction > 0) {
                this.executeMove(direction);
            }
        }
    };

    Game_Player.prototype.clearPicture = function () {
        $gameScreen.erasePicture(1);
    };

    // 主に挙動系を書き換える。
    // プレイヤーが特定の行動を行った場合に、敵オブジェクトも特定の行動を取る。

    // プレイヤーのターン消費行動
    // ・移動　・攻撃　・アイテム使用

    // 敵オブジェクトの行動
    // ・移動　・攻撃　・アイテム使用

    // 

    Game_Player.prototype.moveStraight = function (d) {
        if (this.canPass(this.x, this.y, d)) {
            this._followers.updateMove();
        }
        Game_Character.prototype.moveStraight.call(this, d);
    };

    Game_Player.prototype.canMove = function () {
        if ($gameMap.isEventRunning() || $gameMessage.isBusy()) {
            return false;
        }
        if (this.isMoveRouteForcing() || this.areFollowersGathering()) {
            return false;
        }
        if (this._vehicleGettingOn || this._vehicleGettingOff) {
            return false;
        }
        if (this.isInVehicle() && !this.vehicle().canMove()) {
            return false;
        }
        if (this._moving) {
            return false;
        }
        return true;
    };

    Game_Player.prototype.triggerButtonAction = function () {
        if (Input.isTriggered("ok") && this.canMove()) {
            if (this.getOnOffVehicle()) {
                return true;
            }
            this.checkEventTriggerHere([0]);
            if ($gameMap.setupStartingEvent()) {
                return true;
            }
            this.checkEventTriggerThere([0, 1, 2]);
            if ($gameMap.setupStartingEvent()) {
                return true;
            } else {
                if ($gameMap._tilesetId === RL.TILESET_ID_DUNGEON) {
                    this.attack();
                    return true;
                }
            }
        }
        return false;
    };

    Game_Player.prototype.attack = function () {
        const enemyEventIds = this.enemyInSight();
        this.toEnemyDamage(enemyEventIds, 1);
    };

    Game_Player.prototype.extraAction = function () {
        if ($gameMap._tilesetId === RL.TILESET_ID_DUNGEON) {
            console.log("extraActionに入ります。");
            const actor = RL.getActor();
            const armor = actor.equips()[3];
            
            if (armor) {
                const mp = Number(armor.meta.mp || 0);
                if (actor.mp < mp) {
                    RL.log("MPが足りない！");
                } else {
                    actor.gainMp(-mp);
                    const armorId = armor.itemId;
                    let renge = Number(armor.meta.range || 0);
                    const enemyEventIds = this.enemyInSight(renge);

                    switch (armorId) {
                        case 1: // 普通の普通の服
                            break;
                        case 2: // 全裸
                            RL.log("しかしティルティは服を着ていない！");
                            break;
                        case 8: // 魔導士のローブ
                            this.heal(30);
                            break;
                        case 13: // 魔法少女
                            this.toEnemyDamage(enemyEventIds, 2);
                            break;
                        default:
                            this.toEnemyDamage(enemyEventIds, 1);
                            break;
                    };
                }
            }
        }
    };

    Game_Player.prototype.heal = function (recovery) {
        let text = "ティルティはヒールを唱えた！";
        SceneManager._scene._actionLogWindow.pushTextInfo({ aName: null, aColoer: null, aDamage: 0, tName: null, tColoer: null, tDamage: 0, text: text, kill: false, guard: false });
        SceneManager._scene._actionLogWindow.drawTextInfomation();
        text = "体力が" + recovery + "回復した！";
        SceneManager._scene._actionLogWindow.pushTextInfo({ aName: null, aColoer: null, aDamage: 0, tName: null, tColoer: null, tDamage: 0, text: text, kill: false, guard: false });
        SceneManager._scene._actionLogWindow.drawTextInfomation();
        AudioManager.playSe({ "name": "Heal1", "volume": 90, "pitch": 100, "pan": 0 });
        const actor = RL.getActor();
        if (actor) {
            actor.gainHp(recovery);
        }
    };

    Game_Player.prototype.toEnemyDamage = function (enemyEventIds, mag) {
        const enemy = $gameMap._enemyMapObjects.filter(x => enemyEventIds.indexOf(x._event._eventId) != -1);
        SceneManager._scene._actionLogWindow.clearText();
        if (enemy.length != 0) {
            enemy.forEach(e => {
                target = e._event;
                if (e._isEnemy && !e.isErase()) {
                    let buf = 0;
                    const actor = RL.getActor();
                    if (actor && actor.isStateAffected(6)) {
                        buf = 5;
                    }
                    const damage = Math.round(Math.max(((actor.atk * mag) + buf) - e._enemyData.params[3], 1))
                    e.takeDamage(damage);
                    SceneManager._scene._actionLogWindow.showDamage(this, e, damage);
                    if (!e.isAlive()) {
                        SceneManager._scene._actionLogWindow.killEnemy(e);
                        actor.gainExp(e._enemyData.exp);
                        e._event.erase();
                        target = null;
                        Video.play("movies/hq32fpsvid__00005_.mp4");
                    }
                }
            });
        } else {
            target = null;
        }
        if (target == this) {
            target = null;
        }
        this._attackMotion = true;
    };

    // TODO持っている武器や、回避の判定などでアニメーションを変える。
    Game_Character.prototype.attackMotion = function (/*target = null*/) {
        console.log("attackMotion()に入りました。");
        console.log("targetは" + target);
        this.setThrough(true);
        this.moveForward();
        if (!target) {
            AudioManager.playSe({ "name": "Blow1", "volume": 90, "pitch": 100, "pan": 0 });
        } else {
            if (target._erased) {
                AudioManager.playSe({ "name": "Blow1", "volume": 90, "pitch": 100, "pan": 0 });
            } else {
                if (this == $gamePlayer) {
                    const actor = RL.getActor();
                    const equip = actor.equips()[0];
                    const weaponId = (!equip || equip.itemId === 0) ? 6 : equip.itemId;
                    $gameTemp.requestAnimation([target], $dataWeapons[weaponId].animationId);
                } else {
                    if (guard) {
                        AudioManager.playSe({ "name": "Hammer", "volume": 90, "pitch": 100, "pan": 0 });
                    } else {
                        $gameTemp.requestAnimation([target], 6);
                    }
                    
                }
            }
        }
        this.moveBackward();
        this.setThrough(false);
    };

    // プレイヤーの目の前に敵がいるならば、その敵のIDを返す。
    Game_Player.prototype.enemyInSight = function (range = 0) {
        const player = $gamePlayer;
        const direction = player.direction();
        //let range = 0
        //renge = Number($dataArmors[$gameActors._data[1]._equips[3]._itemId].meta.range);
        const aoe = this.getAreaOfEffect(range);
        let aoeWithDirection = [];
        const enemyIds = [];

        switch (direction) {
            case 2: // 下
                aoeWithDirection = aoe._2;
                break;
            case 4: // 左
                aoeWithDirection = aoe._4;
                break;
            case 6: // 右
                aoeWithDirection = aoe._6;
                break;
            case 8: // 上
                aoeWithDirection = aoe._8;
                break;
        }

        for (var i = 0; i < aoeWithDirection.length; i++) {
            $gameMap.eventsXy(aoeWithDirection[i][0], aoeWithDirection[i][1]).forEach(enemy => {//
                if (enemy._pageIndex == 0) {
                    enemyIds.push(enemy._eventId);
                }
            });
        };

        return enemyIds;
    };

    Game_Player.prototype.getAreaOfEffect = function (range) {
        const player = $gamePlayer;
        const px = player.x;
        const py = player.y;
        let aoe = {};
        let _2 = [];
        let _4 = [];
        let _6 = [];
        let _8 = [];

        switch (range) {
            case 0:// デフォルトの通常攻撃の範囲を取得する。
                _2 = [[px, py + 1]];
                _4 = [[px - 1, py]];
                _6 = [[px + 1, py]];
                _8 = [[px, py - 1]];
                break;
            case 1:// 槍のような攻撃範囲。タテ3マス
                _2 = [[px, py + 1], [px, py + 2], [px, py + 3]];
                _4 = [[px - 1, py], [px - 2, py], [px - 3, py]];
                _6 = [[px + 1, py], [px + 2, py], [px + 3, py]];
                _8 = [[px, py - 1], [px, py - 2], [px, py - 3]];
                break;
            case 2:// ドリームソード
                _2 = [[px - 1, py + 1], [px, py + 1], [px + 1, py + 1], [px - 1, py + 2], [px, py + 2], [px + 1, py + 2]];
                _4 = [[px - 2, py - 1], [px - 1, py - 1], [px - 2, py], [px - 1, py], [px - 2, py + 1], [px - 1, py + 1]];
                _6 = [[px + 2, py - 1], [px + 1, py - 1], [px + 2, py], [px + 1, py], [px + 2, py + 1], [px + 1, py + 1]];
                _8 = [[px - 1, py - 2], [px, py - 2], [px + 1, py - 2], [px - 1, py - 1], [px, py - 1], [px + 1, py - 1]];
                break;
            case 3:// 周り8マス
                _2 = [[px + 1, py], [px + 1, py + 1], [px, py + 1], [px - 1, py + 1], [px - 1, py], [px - 1, py - 1], [px, py - 1], [px + 1, py - 1]];
                _4 = [[px + 1, py], [px + 1, py + 1], [px, py + 1], [px - 1, py + 1], [px - 1, py], [px - 1, py - 1], [px, py - 1], [px + 1, py - 1]];
                _6 = [[px + 1, py], [px + 1, py + 1], [px, py + 1], [px - 1, py + 1], [px - 1, py], [px - 1, py - 1], [px, py - 1], [px + 1, py - 1]];
                _8 = [[px + 1, py], [px + 1, py + 1], [px, py + 1], [px - 1, py + 1], [px - 1, py], [px - 1, py - 1], [px, py - 1], [px + 1, py - 1]];
                break;
            default:
                break;


        }
        aoe._2 = _2;
        aoe._4 = _4;
        aoe._6 = _6;
        aoe._8 = _8;
        return aoe;
    };



    Game_Actor.prototype.gainExp = function (exp) {
        const newExp = this.currentExp() + Math.round(exp * this.finalExpRate() * this.armorExpRate());
        this.changeExp(newExp, this.shouldDisplayLevelUp());
    };

    Game_Actor.prototype.armorExpRate = function () {
        let expRate = 1;
        const actor = RL.getActor();
        const armor = actor ? actor.equips()[3] : null;
        if (armor && armor.meta && armor.meta.exp) {
            expRate = Number(armor.meta.exp) || 1;
        }
        return expRate;
    };


    Game_Actor.prototype.displayLevelUp = function (newSkills) {
        const text = TextManager.levelUp.format(
            this._name,
            TextManager.level,
            this._level
        );
        AudioManager.playSe({ "name": "Magic1", "volume": 90, "pitch": 100, "pan": 0 });
        SceneManager._scene._actionLogWindow.pushTextInfo({ aName: null, aColoer: null, aDamage: 0, tName: null, tColoer: null, tDamage: 0, text: text, kill: false, guard: false });
        SceneManager._scene._actionLogWindow.drawTextInfomation();
    };



    // 以下、プレイヤーがダメージを受ける判定
    // マップ上の敵が、プレイヤーに隣接、且つプレイヤーの方向を
    // 向いている場合に true を返す。

    Game_MapEnemy.prototype.isFacingPlayer = function () {
        const player = $gamePlayer;
        const direction = this._event.direction();
        const dx = player.x - this._event.x;
        const dy = player.y - this._event.y;

        switch (direction) {
            case 2: // 下
                return dy > 0 && Math.abs(dx) <= Math.abs(dy);
            case 4: // 左
                return dx < 0 && Math.abs(dx) >= Math.abs(dy);
            case 6: // 右
                return dx > 0 && Math.abs(dx) >= Math.abs(dy);
            case 8: // 上
                return dy < 0 && Math.abs(dx) <= Math.abs(dy);
        }
        return false;
    };

    Game_MapEnemy.prototype.isErase = function () {
        return this._event._erased;
    };

    Game_MapEnemy.prototype.performAction = function (action) {
        if (!this._actionEnd) {
            switch (action) {
                case ACTION.STOP:
                    break;
                case ACTION.MOVE:
                    this._event.moveTypeTowardPlayer();
                    break;
                case ACTION.TURN:
                    this._event.turnTowardPlayer();
                    break;
                case ACTION.ATTACK:
                    this.attack();
                    break;
                case ACTION.USE_ITEM:
                    this.useItem();
                    break;
                case ACTION.USE_SKILL:
                    this.useSkill();
                    break;
                case ACTION.TRACK:
                    this.trackToLastSeen();
                    break;
            }
            this._actionEnd = true;
        }
    };

    Game_MapEnemy.prototype.isAction = function () {
        return this._event.isMoving() // || !$gameMap.isEventRunning()
    };

    Game_Event.prototype.moveTypeTowardPlayer = function () {
        if (this.isNearThePlayer()) {
            switch (Math.randomInt(6)) {
                case 0:
                case 1:
                case 2:
                case 3:
                case 4:
                    this.moveTowardPlayer();
                    break;
                case 5:
                    this.moveRandom();
                    break;
            }
        } else {
            this.moveRandom();
        }
    };

    // TODO 目の前にプレイヤーがいるかどうかの判定ができるとよい
    Game_Event.prototype.checkTowardCharacter = function () {
        const player = $gamePlayer;
        const dx = player.x - this.x;
        const dy = player.y - this.y;

        if (dx == 0 && dy == 0) {
            return true;
        }
        return false;
    };

    const _Game_Event_update = Game_Event.prototype.update;
    Game_Event.prototype.update = function () {
        _Game_Event_update.call(this);
        if ($gameMap._tilesetId == 4) {
            if ((this._erased && !this._through) || this._pageIndex != 0) {
                this._through = true;
            }
            if ($gameMap._enemyMapObjects && Fturn != Eturn) {
                this.performRandomEnemyAction();
                const enemies = $gameMap._enemyMapObjects.filter((enemy) => enemy.isAlive());
                enemies.forEach(enemy => {
                    if (enemy._event._attackMotion) {
                        this.attackMotion();
                        this._moving = true;
                    }
                });
                const endEnemies = $gameMap._enemyMapObjects.filter((enemy) => enemy.isAlive() && !enemy._actionEnd && enemy._event._pageIndex == 0);
                if (endEnemies.length < 1) {
                    consumptionTurn(ENEMY);
                    enemies.forEach(enemy => {
                        enemy._actionEnd = false;
                        enemy._event._moving = false;
                        enemy._event._attackMotion = false;
                    });
                }
            }
        }
    };

    Game_Event.prototype.performRandomEnemyAction = function () {
        const enemies = $gameMap._enemyMapObjects.filter((enemy) => enemy.isAlive() && enemy._event._pageIndex == 0);
        for (const enemy of enemies) {
            const action = this.selectRandomEnemyAction(enemy);
            enemy.performAction(action);
        }
    };

    /**
     * 指定した座標のイベント/タイルが不透明（壁）かどうかを判定
     */
    Game_Map.prototype.isOpaque = function(x, y) {
        return !this.isPassable(x, y, 2) && !this.isPassable(x, y, 4) && !this.isPassable(x, y, 6) && !this.isPassable(x, y, 8);
    };

    /**
     * 簡易的な視界判定 (Line of Sight)
     */
    Game_Character.prototype.canSeeTarget = function(target) {
        if (!target) return false;
        const x1 = this.x;
        const y1 = this.y;
        const x2 = target.x;
        const y2 = target.y;
        const dx = Math.abs(x2 - x1);
        const dy = Math.abs(y2 - y1);
        const sx = (x1 < x2) ? 1 : -1;
        const sy = (y1 < y2) ? 1 : -1;
        let err = dx - dy;

        let currX = x1;
        let currY = y1;

        while (true) {
            if (currX === x2 && currY === y2) return true;
            // 壁などの判定
            if ((currX !== x1 || currY !== y1) && $gameMap.isOpaque(currX, currY)) {
                return false;
            }
            const e2 = 2 * err;
            if (e2 > -dy) {
                err -= dy;
                currX += sx;
            }
            if (e2 < dx) {
                err += dx;
                currY += sy;
            }
        }
    };

    Game_Event.prototype.selectRandomEnemyAction = function (enemy) {
        const player = $gamePlayer;
        const dx = Math.abs(player.x - enemy._event.x);
        const dy = Math.abs(player.y - enemy._event.y);
        const distance = dx + dy;

        // 視界（数値的な距離）と遮蔽物の両方をチェック
        if (distance <= enemy._sight && enemy._event.canSeeTarget(player)) {
            // プレイヤーを確認したので追跡座標を更新
            enemy._lastSeenX = player.x;
            enemy._lastSeenY = player.y;

            if (player.isNearTheEvent(enemy._event)) {
                if (enemy.isFacingPlayer()) {
                    return ACTION.ATTACK;
                } else {
                    enemy._event.turnTowardPlayer();
                    return ACTION.ATTACK;
                }
            } else {
                return ACTION.MOVE;
            }
        } else {
            // 視界外の場合、最後に見た場所があるなら追跡
            if (enemy._lastSeenX >= 0) {
                return ACTION.TRACK;
            }
            // 索敵
            return Math.randomInt(15) === 0 ? ACTION.MOVE : ACTION.STOP;
        }
    };

    Game_MapEnemy.prototype.getAvailableItems = function () {
        // 使用可能なアイテムのリストを返す処理を実装
        return [];
    };

    Game_MapEnemy.prototype.getAvailableSkills = function () {
        // 使用可能なスキルのリストを返す処理を実装
        return [];
    };

    Game_MapEnemy.prototype.attack = function () {
        const player = $gamePlayer;
        const actor = RL.getActor();
        if (!this.isFacingPlayer()) {
            this._event.turnTowardPlayer();
        }
        console.log("enemy attackに入りました。");
        target = player;
        this._event._attackMotion = true;
        var buf = 0;
        if (actor.isStateAffected(7)) {
            buf = 5;
        }
        var mag = Math.max($gameVariables.value(33), 10);
        const damage = Math.round(Math.max((this._enemyData.params[2] * mag / 10) - actor.def + buf, 0));

        player.takeDamage(damage);
        
        const armor = actor.equips()[3];
        if (armor && armor.itemId === 2) { // 全裸
            $gameTemp.reserveCommonEvent(this.getCommonId(this._enemyId));
        } else if (armor && $gameVariables.value(RL.VAR_CLOTHING_DAMAGE) >= Number(armor.meta.shield || 0)) {
            $gameTemp.reserveCommonEvent(21); // 衣装破壊コモンイベント
        }
        SceneManager._scene._actionLogWindow.showDamage(this, $gamePlayer, damage);
    };

    Game_Player.prototype.takeDamage = function (damage) {
        guard = false;
        let guardRate = 0;
        const actor = RL.getActor();
        const armor = actor.equips()[3];
        
        if (armor) {
            guardRate = Number(armor.meta.guard || 0);
        }
        
        const rand = Math.randomInt(100) + 1;
        if (rand > guardRate) {
            actor.gainHp(-damage);
            $gameVariables.setValue(RL.VAR_CLOTHING_DAMAGE, $gameVariables.value(RL.VAR_CLOTHING_DAMAGE) + 1);
            RL.playVoice("damage"); // 成人向けボイス再生
            actor._hp = Math.max(0, actor._hp);
        } else {
            guard = true;
        }

        if (actor.hp === 0) {
            if (actor.isStateAffected(3)) {
                $gameSwitches.setValue(5, true);
            }
            $gameSwitches.setValue(3, true);
        }
    };

    // ダンジョン内でのタッチ移動（目的地設定）を禁止
    Scene_Map.prototype.onMapTouch = function() {
        if ($gameMap._tilesetId === RL.TILESET_ID_DUNGEON) {
            return;
        }
        const x = $gameMap.canvasToMapX(TouchInput.x);
        const y = $gameMap.canvasToMapY(TouchInput.y);
        $gameTemp.setDestination(x, y);
    };

    Game_MapEnemy.prototype.getCommonId = function (enemyId) {//
        switch (enemyId) {
            case 1: // 1層ゴブリン
                return 2
                break;
            case 2: // 1層スライム
                return 1
                break;
            case 3: // 1層あらくれ
                return 3
                break;
            case 4: // 2層ゴブリン
                return 7
                break;
            case 5: // 2層ゴブリン
                return 8
                break;
            case 6: // 1.5層ザコ
                return 41
                break;
            case 7: // 2.5層ザコ
                return 42
                break;
            case 8: // 3.5層ザコ
                return 43
                break;
            case 9: // 4.5層ザコ
                return 44
                break;
            case 33: // 3層スライム
                return 9
                break;
            case 34: // 3層あらくれ
                return 10
                break;
            case 38: // 4層スライム
                return 135
                break;
            case 40: // 4層あらくれ
                return 136
                break;
            case 50: // 5層機械
                return 137
                break;
            default:
                return 20
                break;

        }
        return 1
    };


    Game_MapEnemy.prototype.useItem = function () {
        // アイテム使用処理を実装
    };

    Game_MapEnemy.prototype.useSkill = function () {
        // スキル使用処理を実装
    };

    Game_Player.prototype.isNearTheEvent = function (event) {
        let dx = Math.abs(this.x - event.x);
        let dy = Math.abs(this.y - event.y);
        const direction = this.getInputDirection()
        switch (direction) {
            case 2: // 下
                dx = Math.abs(this.x - event.x);
                dy = Math.abs(this.y + 1 - event.y);
                break;
            case 4: // 左
                dx = Math.abs(this.x - 1 - event.x);
                dy = Math.abs(this.y - event.y);
                break;
            case 6: // 右
                dx = Math.abs(this.x + 1 - event.x);
                dy = Math.abs(this.y - event.y);
                break;
            case 8: // 上
                dx = Math.abs(this.x - event.x);
                dy = Math.abs(this.y - 1 - event.y);
                break;
            case 0:
                break;
        }
        return Math.sqrt(dx * dx + dy * dy) <= RL.COLLISION_DISTANCE;
    };

    Game_Player.prototype.canPass = function (x, y, d) {
        const x2 = $gameMap.roundXWithDirection(x, d);
        const y2 = $gameMap.roundYWithDirection(y, d);
        if (!$gameMap.isValid(x2, y2)) {
            return false;
        }
        if (this.isThrough() || this.isDebugThrough()) {
            return true;
        }
        if (this.isWater(x, y)) {
            return true;
        }
        if (!this.isMapPassable(x, y, d)) {
            if (this.isWater(x2, y2)) {
                return true;
            } else {
                return false;
            }
        }
        if (this.isCollidedWithCharacters(x2, y2)) {
            return false;
        }
        /*if (!this.isWater(x2, y2)) {
            return false;
        }*/
        return true;
    };

    Game_Player.prototype.isWater = function (x, y) {
        if ($gameMap.terrainTag(x, y) == 1) {
                const actor = RL.getActor();
                const armor = actor ? actor.equips()[3] : null;
                if (armor) {
                    const armorId = armor.itemId;
                    if (armorId == 5 || armorId == 9) {
                        return true;
                    } else {
                        return false;
                    }
                }
        } else {
            return false;
        }
    };

    function getRandomInt(min, max) {
        min = Math.ceil(min);
        max = Math.floor(max);
        return Math.floor(Math.random() * (max - min) + min); //The maximum is exclusive and the minimum is inclusive
    };


    function Action_Log() {
        this.initialize.apply(this, arguments);
    }

    Action_Log.prototype = Object.create(Window_Base.prototype);
    Action_Log.prototype.constructor = Action_Log;

    Action_Log.prototype.initialize = function () {
        Window_Base.prototype.initialize.call(this, this.createRectangle());
        this.contents.clear();
        this.opacity = 200;
    };

    Action_Log.prototype.createRectangle = function () {
        const x = 0;
        const h = this.fittingHeight(4);
        const y = Graphics.boxHeight - h - 8; // 画面下部に配置
        const w = Graphics.boxWidth - 250;
        return new Rectangle(x, y, w, h);
    };
    
    Action_Log.prototype.getNameAndColors = function (attacker, target, damage) {
        const attackerName = attacker === $gamePlayer ? $gameActors.actor(1).name() : attacker._enemyData.name;
        const attackerColor = attacker === $gamePlayer ? ColorManager.textColor(3) : ColorManager.textColor(2);
        const targetName = target === $gamePlayer ? $gameActors.actor(1).name() : target._enemyData.name;
        const targetColor = target === $gamePlayer ? ColorManager.textColor(3) : ColorManager.textColor(2);
        return { aName: attackerName, aColoer: attackerColor, aDamage: 0, tName: targetName, tDamage: damage, tColoer: targetColor, text: null, kill: false, guard: guard };
    };
    
    Action_Log.prototype.showDamage = function (attacker, target, damage) {
        const nameAndColor = this.getNameAndColors(attacker, target, damage);
        this.pushTextInfo(nameAndColor);
        this.drawTextInfomation();
    };

    Action_Log.prototype.pushTextInfo = function (data) {
        if (TEXTINFO.length < 4) {
            TEXTINFO.push(data);
        } else {
            for (var i = 0; i < 3; i++) {
                TEXTINFO[i] = TEXTINFO[i + 1];
            }
            TEXTINFO[3] = data;
            SceneManager._scene._actionLogWindow.clearText();
        }
    };

    Action_Log.prototype.drawTextInfomation = function () {
        for (var i = 0; i < TEXTINFO.length; i++) {
            let height = i * TEXTHEIGHT
            if (TEXTINFO[i].text != null) {
                this.drawText(TEXTINFO[i].text, 0, height, this.contentsWidth(), 'left');
            } else if (TEXTINFO[i].kill) {
                this.changeTextColor(TEXTINFO[i].tColoer);
                this.drawText(TEXTINFO[i].tName, 0, height, this.contentsWidth(), 'left');
                this.resetTextColor();
                this.drawText(KILL_TEXT, this.textWidth(TEXTINFO[i].tName), height, this.contentsWidth(), 'left');
            } else if (guard) {
                this.changeTextColor(TEXTINFO[i].aColoer);
                this.drawText(TEXTINFO[i].aName, 0, height, this.contentsWidth(), 'left');
                this.resetTextColor();
                this.drawText(ATTACK_TEXT + JOINT, this.textWidth(TEXTINFO[i].aName), height, this.contentsWidth(), 'left');
                this.changeTextColor(TEXTINFO[i].tColoer);
                this.drawText(TEXTINFO[i].tName, this.textWidth(TEXTINFO[i].aName + ATTACK_TEXT + JOINT), height, this.contentsWidth(), 'left');
                this.resetTextColor();
                this.drawText(GUARD_TEXT, this.textWidth(TEXTINFO[i].aName + ATTACK_TEXT + TEXTINFO[i].tName + JOINT), height, this.contentsWidth(), 'left');
            } else {
                this.changeTextColor(TEXTINFO[i].aColoer);
                this.drawText(TEXTINFO[i].aName, 0, height, this.contentsWidth(), 'left');
                this.resetTextColor();
                this.drawText(ATTACK_TEXT + JOINT, this.textWidth(TEXTINFO[i].aName), height, this.contentsWidth(), 'left');
                this.changeTextColor(TEXTINFO[i].tColoer);
                this.drawText(TEXTINFO[i].tName, this.textWidth(TEXTINFO[i].aName + ATTACK_TEXT + JOINT), height, this.contentsWidth(), 'left');
                this.resetTextColor();
                this.drawText(TEXT_JOINT + TEXTINFO[i].tDamage + DAMAGE_TEXT, this.textWidth(TEXTINFO[i].aName + ATTACK_TEXT + TEXTINFO[i].tName + JOINT), height, this.contentsWidth(), 'left');
            }
        }
    };

    Action_Log.prototype.killEnemy = function (target) {
        /*
        const height = TEXTHEIGHT * (TEXTINFO.length - 1)
        this.changeTextColor(TEXTINFO[TEXTINFO.length - 1].tColoer);
        this.drawText(JOINT + TEXTINFO[TEXTINFO.length - 1].tName, this.textWidth(TEXTINFO[TEXTINFO.length - 1].aName + ATTACK_TEXT + JOINT + TEXTINFO[TEXTINFO.length - 1].tName + TEXT_JOINT + damage + DAMAGE_TEXT), height, this.contentsWidth(), 'left');
        this.resetTextColor();
        this.drawText(KILL_TEXT, this.textWidth(TEXTINFO[TEXTINFO.length - 1].aName + ATTACK_TEXT + JOINT + TEXTINFO[TEXTINFO.length - 1].tName + TEXT_JOINT + damage + DAMAGE_TEXT + JOINT + TEXTINFO[TEXTINFO.length - 1].tName), height, this.contentsWidth(), 'left');
        */
        const targetName = target._enemyData.name;
        const targetColor = ColorManager.textColor(2);

        SceneManager._scene._actionLogWindow.pushTextInfo({ aName: null, aColoer: null, aDamage: 0, tName: targetName, tColoer: targetColor, tDamage: 0, text: null, kill: true, guard: false });
        SceneManager._scene._actionLogWindow.drawTextInfomation();
    };
    
    Action_Log.prototype.clearText = function () {
        TEXTINFO = [];
        this.contents.clear();
    };

    Action_Log.prototype.initializeText = function () {
        TEXTINFO = [];
    };

    Action_Log.prototype.clearWindow = function () {
        //this.opacity = 0;
        //this.x = 10000;
        this.close();
    };

    const _Scene_Map_createAllWindows = Scene_Map.prototype.createAllWindows;
    Scene_Map.prototype.createAllWindows = function () {
        _Scene_Map_createAllWindows.call(this);
        if ($gameSwitches.value(1)) {
            this.createActionLogWindow();
        };
    };

    Scene_Map.prototype.createActionLogWindow = function () {
        this._actionLogWindow = new Action_Log();
        this.addWindow(this._actionLogWindow);
    };

    Action_Log.prototype.openWindow = function () {
        this.open();
    };

    // オノマトペ投擲および更新処理の実装
    Game_Player.prototype.updateThrowInput = function() {
        if (this._onomatopoeiaType === undefined) this._onomatopoeiaType = 0;

        if (Input.isTriggered('pagedown')) { // Wキーで種類切替 (MZ: pagedown = W)
            this._onomatopoeiaType = (this._onomatopoeiaType + 1) % 3;
            const names = ["ドカン！", "スッ…", "バガン！"];
            RL.log("装備オノマトペ：【" + names[this._onomatopoeiaType] + "】");
        }

        if (Input.isTriggered('pageup')) { // Qキーで投擲 (MZ: pageup = Q)
            this.throwOnomatopoeia();
        }
    };

    Game_Player.prototype.throwOnomatopoeia = function() {
        if (!this.canMove()) return;
        
        if (this._onomatopoeiaType === undefined) this._onomatopoeiaType = 0;
        const type = this._onomatopoeiaType;
        const names = ["ドカン！", "スッ…", "バガン！"];
        const text = names[type];
        
        AudioManager.playSe({ name: "Wind7", volume: 90, pitch: 100, pan: 0 }); // 追加: 投擲SE

        const onoma = new Sprite_Onoma(this.x, this.y, this.direction(), text);
        // 発射位置を一歩進める
        switch (this.direction()) {
            case 2: onoma._gridY += 1; break;
            case 4: onoma._gridX -= 1; break;
            case 6: onoma._gridX += 1; break;
            case 8: onoma._gridY -= 1; break;
        }
        onoma._type = type;
        onoma.updatePosition();
        _onomatopoeias.push(onoma);
        
        if (SceneManager._scene._spriteset) {
            SceneManager._scene._spriteset._tilemap.addChild(onoma);
        }
        
        RL.log("ティルティは「" + text + "」と放った！");
        this._moving = true;
        this.attackMotion(null); // モーション再生
        consumptionTurn(FRIEND); // ターン消費
    };

    Game_Player.prototype.updateOnomatopoeias = function() {
        for (let i = _onomatopoeias.length - 1; i >= 0; i--) {
            const onoma = _onomatopoeias[i];
            
            if (onoma._lifespan <= 0) {
                onoma.destroy();
                _onomatopoeias.splice(i, 1);
                continue;
            }

            const gx = Math.round(onoma._gridX);
            const gy = Math.round(onoma._gridY);

            // 壁判定 (スッ… 以外は壁で消滅)
            if (onoma._type !== 1 && $gameMap.isOpaque(gx, gy)) {
                if (onoma._type === 0) { // ドカン！なら爆発処理
                    this.triggerExplosion(gx, gy);
                }
                onoma.destroy();
                _onomatopoeias.splice(i, 1);
                continue;
            }

            // 敵との判定 ($gameMap._enemyMapObjects が未定義のマップでのエラー回避)
            const enemies = $gameMap._enemyMapObjects ? $gameMap._enemyMapObjects.filter(e => e.isAlive() && e._event.x === gx && e._event.y === gy) : [];
            if (enemies.length > 0) {
                enemies.forEach(e => {
                    if (onoma._type === 0) { // ドカン
                        this.triggerExplosion(gx, gy);
                        onoma._lifespan = 0;
                    } else if (onoma._type === 1) { // スッ (貫通)
                        if (!onoma._hitTargets) onoma._hitTargets = [];
                        if (!onoma._hitTargets.includes(e)) {
                            AudioManager.playSe({ name: "Slash1", volume: 90, pitch: 100, pan: 0 }); // 追加: 斬撃SE
                            $gameTemp.requestAnimation([e._event], 6); // アニメーションID: 6 (斬撃)
                            e.takeDamage(15);
                            if (SceneManager._scene._actionLogWindow) SceneManager._scene._actionLogWindow.showDamage(this, e, 15);
                            this.checkEnemyDeath(e);
                            onoma._hitTargets.push(e);
                        }
                    } else if (onoma._type === 2) { // バガン (ノックバック)
                        AudioManager.playSe({ name: "Blow2", volume: 90, pitch: 90, pan: 0 }); // 追加: 打撃SE
                        $gameTemp.requestAnimation([e._event], 12); // アニメーションID: 12 (打撃)
                        e.takeDamage(25);
                        if (SceneManager._scene._actionLogWindow) SceneManager._scene._actionLogWindow.showDamage(this, e, 25);
                        this.checkEnemyDeath(e);
                        // ノックバック処理: 壁がなければ1マス下がる
                        if (e._event.canPass(e._event.x, e._event.y, onoma._direction)) {
                            e._event.moveStraight(onoma._direction);
                        }
                        onoma._lifespan = 0;
                    }
                });

                if (onoma._lifespan === 0) {
                    onoma.destroy();
                    _onomatopoeias.splice(i, 1);
                }
            }
        }
    };

    Game_Player.prototype.triggerExplosion = function(x, y) {
        AudioManager.playSe({ name: "Explosion1", volume: 90, pitch: 100, pan: 0 }); // 爆発SE
        // 周囲9マスの敵に爆発アニメーションとダメージを与える
        if (!$gameMap._enemyMapObjects) return; // 敵データの無いマップでのエラー回避
        for (let dx = -1; dx <= 1; dx++) {
            for (let dy = -1; dy <= 1; dy++) {
                const ex = x + dx;
                const ey = y + dy;
                const enemies = $gameMap._enemyMapObjects.filter(e => e.isAlive() && e._event.x === ex && e._event.y === ey);
                enemies.forEach(e => {
                    $gameTemp.requestAnimation([e._event], 73); // アニメーションID: 73 (爆発1)
                    e.takeDamage(35);
                    if (SceneManager._scene._actionLogWindow) SceneManager._scene._actionLogWindow.showDamage(this, e, 35);
                    this.checkEnemyDeath(e);
                });
            }
        }
    };

    Game_Player.prototype.checkEnemyDeath = function(e) {
        if (!e.isAlive()) {
            SceneManager._scene._actionLogWindow.killEnemy(e);
            RL.getActor().gainExp(e._enemyData.exp);
            e._event.erase();
            Video.play("movies/hq32fpsvid__00005_.mp4");
        }
    };

    // === オノマトペ投擲システム用クラス ===
    class Sprite_Onoma extends Sprite {
        initialize(x, y, d, text) {
            super.initialize();
            this._gridX = x;
            this._gridY = y;
            this._direction = d;
            this._text = text;
            this._speed = 0.2; // 1フレームあたりの移動タイル数
            this._lifespan = 30; // 寿命（フレーム）
            this.createBitmap();
            this.updatePosition();
        }

        createBitmap() {
            this.bitmap = new Bitmap(128, 48);
            this.bitmap.fontSize = 28;
            this.bitmap.outlineColor = 'rgba(0, 0, 0, 0.8)';
            this.bitmap.outlineWidth = 4;
            this.bitmap.drawText(this._text, 0, 0, 128, 48, 'center');
            this.anchor.x = 0.5;
            this.anchor.y = 0.5;
        }

        update() {
            super.update();
            this.move();
            this.updatePosition();
            this._lifespan--;
        }

        move() {
            switch (this._direction) {
                case 2: this._gridY += this._speed; break; // 下
                case 4: this._gridX -= this._speed; break; // 左
                case 6: this._gridX += this._speed; break; // 右
                case 8: this._gridY -= this._speed; break; // 上
            }
        }

        updatePosition() {
            const tw = $gameMap.tileWidth();
            const th = $gameMap.tileHeight();
            // マップのスクロールを考慮した画面座標への変換
            this.x = ($gameMap.adjustX(this._gridX) + 0.5) * tw;
            this.y = ($gameMap.adjustY(this._gridY) + 0.5) * th;
        }

        destroy(options) {
            if (this.parent) {
                this.parent.removeChild(this);
            }
            super.destroy(options);
        }
    }

    console.log("RogueLike.js: Loading complete.");
})();

