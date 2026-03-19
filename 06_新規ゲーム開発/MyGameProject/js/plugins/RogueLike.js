/**
 * 
 * 
 */



// 移動可能か否かの判定を行う。特定のアイテムを所持しているときに移動可能になるようなルーチンを組む。
// TODO Game_Player.prototype.canMove


// プレイヤーの向きのみ変更（Shiftキー押下時）
// ミニマップの実装完了


(() => {

    // プレイヤーと敵の衝突判定の距離
    const collisionDistance = 1;
    let Fturn = 1;
    let Eturn = 1;
    const FRIEND = true;
    const ENEMY = false;
    let target = null;
    let guard = false;

    Game_Player.prototype.initMembers = function () {
        Game_Character.prototype.initMembers.call(this);
        this._vehicleType = "walk";
        this._vehicleGettingOn = false;
        this._vehicleGettingOff = false;
        this._dashing = false;
        this._needsMapReload = false;
        this._transferring = false;
        this._newMapId = 0;
        this._newX = 0;
        this._newY = 0;
        this._newDirection = 0;
        this._fadeType = 0;
        this._followers = new Game_Followers();
        this._encounterCount = 0;
        this._attackMotion = false;
        this._moving = false;
    };

    Game_Event.prototype.initMembers = function () {
        Game_Character.prototype.initMembers.call(this);
        this._moveType = 0;
        this._trigger = 0;
        this._starting = false;
        this._erased = false;
        this._pageIndex = -2;
        this._originalPattern = 1;
        this._originalDirection = 2;
        this._prelockDirection = 0;
        this._locked = false;
        this._attackMotion = false;
        this._moving = false;
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
            this._isEnemy = event.event().name.indexOf("enemy") != -1;
            this._enemyId = Number(event.event().meta.id);
            this._enemyData = $dataEnemies[this._enemyId];
            this._actionEnd = false;
            this._isBoss = event.event().meta.boss ? true : false;
            this._sight = Number(event.event().meta.sight) || 5; // 視界のデフォル値は5
            if (this._enemyData) {
                var mag = Math.max($gameVariables.value(33), 10);
                this._hp = Math.round(this._enemyData.params[0] * mag / 10);
                this._mp = Math.round(this._enemyData.params[1] * mag / 10);
            }
            /*
            if (this._event._erased && !this._event._through) {
                this._event._through = true;
            }
            */
        }

        isAlive() {
            return this._hp > 0;
        }

        takeDamage(damage) {
            guard = false;
            this._hp -= damage;
        }
    }

    Game_Player.prototype.reserveTransfer = function (mapId, x, y, d, fadeType) {
        this._transferring = true;
        this._newMapId = mapId;
        this._newX = x;
        this._newY = y;
        this._newDirection = d;
        this._fadeType = fadeType;
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

    Game_Player.prototype.update = function (sceneActive) {
        const lastScrolledX = this.scrolledX();
        const lastScrolledY = this.scrolledY();
        const wasMoving = this.isMoving();
        this.updateDashing();
        if (sceneActive) {
            this.moveByInput();
        }
        Game_Character.prototype.update.call(this);
        this.updateScroll(lastScrolledX, lastScrolledY);
        this.updateVehicle();
        if (this._attackMotion && !this._moving) {
            this.attackMotion();
            this._moving = true;
        }
        if (!this.isMoving()) {
            this.updateNonmoving(wasMoving, sceneActive);
            if (wasMoving) {
                this._moving = false;
                this._attackMotion = false;
                this.clearPicture();
                consumptionTurn(FRIEND);
            }
        }
        this._followers.update();
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

    /**
     * 決定ボタンを押下した時のルーチン
     * @returns
     */
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
                if ($gameMap._tilesetId == 4) {
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
        if ($gameMap._tilesetId == 4) {
            console.log("extraActionに入ります。");
            if (!$dataArmors[$gameActors._data[1]._equips[3]]) {
                const mp = Number($dataArmors[$gameActors._data[1]._equips[3]._itemId].meta.mp);
                if ($gameActors._data[1]._mp < mp) {
                    const text = "MPが足りない！";
                    SceneManager._scene._actionLogWindow.pushTextInfo({ aName: null, aColoer: null, aDamage: 0, tName: null, tColoer: null, tDamage: 0, text: text, kill: false, guard: false });
                    SceneManager._scene._actionLogWindow.drawTextInfomation();
                } else {
                    $gameActors._data[1]._mp -= mp;
                    const armorId = $gameActors._data[1]._equips[3]._itemId;
                    let renge = Number($dataArmors[$gameActors._data[1]._equips[3]._itemId].meta.range);
                    const enemyEventIds = this.enemyInSight(renge);

                    switch (armorId) {
                        case 1: // 普通の普通の服
                            //this.toEnemyDamage(enemyEventIds, 1);
                            break;
                        case 2:
                            const text = "しかしティルティは服を着ていない！";
                            SceneManager._scene._actionLogWindow.pushTextInfo({ aName: null, aColoer: null, aDamage: 0, tName: null, tColoer: null, tDamage: 0, text: text, kill: false, guard: false });
                            SceneManager._scene._actionLogWindow.drawTextInfomation();
                        case 3: // メイド服
                            this.toEnemyDamage(enemyEventIds, 1);
                            break;
                        case 4: // ドレス
                            this.toEnemyDamage(enemyEventIds, 1);
                            break;
                        case 5: // 水着
                            break;
                        case 6: // ウェディングレオタード
                            $gameTemp.reserveCommonEvent(106);
                            break;
                        case 7: // ランジェリー
                            break;
                        case 8: // 魔導士のローブ
                            this.heal(30);
                            break;
                        case 9: // スク水
                            break;
                        case 10: // ビキニアーマー
                            break;
                        case 11: // ゴスロリドレス
                            this.toEnemyDamage(enemyEventIds, 1);
                            break;
                        case 12: // 巫女服
                            $gameTemp.reserveCommonEvent(107);
                            break;
                        case 13: // 魔法少女
                            this.toEnemyDamage(enemyEventIds, 2);
                            break;
                    };
                }

            }
        } else {
            console.log("extraActionに入りました。");
            //$gameTemp.reserveCommonEvent();
        }
    };

    Game_Player.prototype.heal = function (recovery) {
        var text = "ティルティはヒールを唱えた！";
        SceneManager._scene._actionLogWindow.pushTextInfo({ aName: null, aColoer: null, aDamage: 0, tName: null, tColoer: null, tDamage: 0, text: text, kill: false, guard: false });
        SceneManager._scene._actionLogWindow.drawTextInfomation();
        text = "体力が" + recovery + "回復した！";
        SceneManager._scene._actionLogWindow.pushTextInfo({ aName: null, aColoer: null, aDamage: 0, tName: null, tColoer: null, tDamage: 0, text: text, kill: false, guard: false });
        SceneManager._scene._actionLogWindow.drawTextInfomation();
        AudioManager.playSe({ "name": "Heal1", "volume": 90, "pitch": 100, "pan": 0 });
        $gameActors._data[1]._hp += recovery;
    };

    Game_Player.prototype.toEnemyDamage = function (enemyEventIds, mag) {
        const enemy = $gameMap._enemyMapObjects.filter(x => enemyEventIds.indexOf(x._event._eventId) != -1);
        SceneManager._scene._actionLogWindow.clearText();
        if (enemy.length != 0) {
            enemy.forEach(e => {
                target = e._event;
                if (e._isEnemy && !e.isErase()) {
                    var buf = 0;
                    if ($gameActors._data[1]._states.indexOf(6) != -1) {
                        buf = 5;
                    }
                    const damage = Math.round(Math.max((($gameActors._data[1].atk * mag) + buf) - e._enemyData.params[3], 1))
                    e.takeDamage(damage);
                    SceneManager._scene._actionLogWindow.showDamage(this, e, damage);
                    if (!e.isAlive()) {
                        SceneManager._scene._actionLogWindow.killEnemy(e);
                        $gameActors._data[1].gainExp(e._enemyData.exp);
                        e._event.erase();
                        target = null;
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
                    const weapon = $gameActors._data[1]._equips[0]._itemId == 0 ? 6 : $gameActors._data[1]._equips[0]._itemId
                    $gameTemp.requestAnimation([target], $dataWeapons[weapon].animationId);
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
        var expRate = 1;
        if (!$dataArmors[$gameActors._data[1]._equips[3]]) { // 防具を装備していない場合は処理を行わない。本来はあり得ないが
            if (!$dataArmors[$gameActors._data[1]._equips[3]._itemId].meta.exp) {
                Number($dataArmors[$gameActors._data[1]._equips[3]._itemId].meta.exp)
            }
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

    const STOP = 0;
    const MOVE = 1;
    const TURN = 2;
    const ATTACK = 3;
    const USE_ITEM = 4;
    const USE_SKILL = 5;


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
                case STOP:
                    break;
                case MOVE:
                    this._event.moveTypeTowardPlayer();
                    break;
                case TURN:
                    this._event.turnTowardPlayer();
                    break;
                case ATTACK:
                    this.attack();
                    break;
                case USE_ITEM:
                    this.useItem();
                    break;
                case USE_SKILL:
                    this.useSkill();
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

    Game_Event.prototype.update = function () {
        Game_Character.prototype.update.call(this);
        this.checkEventTriggerAuto();
        this.updateParallel();
        if ($gameMap._tilesetId == 4) {
            if ((this._erased && !this._through) || this._pageIndex != 0) {
                this._through = true;
            }
            const enemies = $gameMap._enemyMapObjects.filter((enemy) => enemy.isAlive());
            if (Fturn != Eturn) {
                this.performRandomEnemyAction();
                enemies.forEach(enemy => {
                    if (enemy._event._attackMotion) {
                        console.log("enemy attackMotion");
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
            if (player.isNearTheEvent(enemy._event)) {
                if (enemy.isFacingPlayer()) {
                    return ATTACK;
                } else {
                    enemy._event.turnTowardPlayer();
                    return ATTACK;
                }
            } else {
                return MOVE;
            }
        } else {
            // 視界外の場合は停止するか、たまに周囲をランダム移動（索敵）
            return Math.randomInt(15) === 0 ? MOVE : STOP;
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
        if (!this.isFacingPlayer()) {
            this._event.turnTowardPlayer();
        }
        console.log("enemy attackに入りました。");
        target = player;
        this._event._attackMotion = true;
        var buf = 0;
        if ($gameActors._data[1]._states.indexOf(7) != -1) {
            buf = 5;
        }
        var mag = Math.max($gameVariables.value(33), 10);
        const damage = Math.round(Math.max((this._enemyData.params[2] * mag / 10) - $gameActors._data[1].def + buf, 0));

        player.takeDamage(damage);
        if ($gameActors._data[1]._equips[3]._itemId == 2) {
            $gameTemp.reserveCommonEvent(this.getCommonId(this._enemyId));
        } else if ($gameVariables.value(15) >= ($dataArmors[$gameActors._data[1]._equips[3]._itemId].meta["shield"])) {
            $gameTemp.reserveCommonEvent(21);
            //$gameActors._data[1]._equips[3].setEquip(false, null);
        }
        SceneManager._scene._actionLogWindow.showDamage(this, $gamePlayer, damage);
        
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
        return Math.sqrt(dx * dx + dy * dy) <= collisionDistance;
    };

    Game_Player.prototype.takeDamage = function (damage) {
        guard = false;
        var guardRate = 0;
        var rand = 1;
        console.log("equipは" + $gameActors._data[1]._equips[3]);
        guardRate = Number($dataArmors[$gameActors._data[1]._equips[3]._itemId].meta["guard"]);
        console.log("GuardRate=" + guardRate);
        rand = getRandomInt(1, 101);
        /*if (!$gameActors._data[1]._equips[3]) { // TODO スライムが攻撃をガードするテキストが表示される模様
            guardRate = Number($dataArmors[$gameActors._data[1]._equips[3]._itemId].meta["guard"]);
            console.log("GuardRate=" + guardRate);
            rand = getRandomInt(1, 101);
        }*/
        if (rand > guardRate) {
            $gameActors._data[1]._hp -= damage;
            //$gameVariables.setValue(15, $gameVariables.value(15) + damage);
            $gameVariables.setValue(15, $gameVariables.value(15) + 1);
            $gameActors._data[1]._hp = Math.max(0, $gameActors._data[1]._hp);
        } else {
            guard = true;
        }
        //if ($gameActors._data[1]._hp <= damage) {
        if ($gameActors._data[1]._hp == 0) {
            if ($gameActors._data[1]._states.indexOf(3) != -1) {
                $gameSwitches.setValue(5, true);
            }
            $gameSwitches.setValue(3, true);
        }
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
            if (!$dataArmors[$gameActors._data[1]._equips[3]]) { // 防具を装備していない場合は処理を行わない。本来はあり得ないが
                const armorId = $gameActors._data[1]._equips[3]._itemId
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

    let TEXTINFO = [];
    const TEXTHEIGHT = 36;

    const JOINT = "";
    const ATTACK_TEXT = "の攻撃！";
    const TEXT_JOINT = "に";
    const DAMAGE_TEXT = "ダメージ！";
    const KILL_TEXT = "を倒した！";
    const GUARD_TEXT = "は防いだ！";

    Action_Log.prototype = Object.create(Window_Base.prototype);
    Action_Log.prototype.constructor = Action_Log;

    Action_Log.prototype.initialize = function () {
        Window_Base.prototype.initialize.call(this, this.createRectangle());
        this.contents.clear();
        this.opacity = 200;
    };

    Action_Log.prototype.createRectangle = function () {
        const x = 0;
        const y = Graphics.height - this.itemHeight() * 5;
        const w = Graphics.boxWidth - 250;
        const h = this.fittingHeight(4);
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

    //-----------------------------------------------------------------------------
    // Sprite_Minimap
    //
    // ミニマップを表示するためのスプライトクラス

    function Sprite_Minimap() {
        this.initialize.apply(this, arguments);
    }

    Sprite_Minimap.prototype = Object.create(Sprite.prototype);
    Sprite_Minimap.prototype.constructor = Sprite_Minimap;

    Sprite_Minimap.prototype.initialize = function() {
        Sprite.prototype.initialize.call(this);
        this._size = 4; // 1タイルのピクセルサイズ
        this._mapWidth = 0;
        this._mapHeight = 0;
        this.x = Graphics.boxWidth - 200;
        this.y = 20;
        this.createBitmap();
        this.updateVisibility();
    };

    Sprite_Minimap.prototype.createBitmap = function() {
        if ($gameMap) {
            this._mapWidth = $gameMap.width();
            this._mapHeight = $gameMap.height();
            this.bitmap = new Bitmap(this._mapWidth * this._size, this._mapHeight * this._size);
            this.drawMap();
        }
    };

    Sprite_Minimap.prototype.drawMap = function() {
        if (!this.bitmap) return;
        this.bitmap.clear();
        this.bitmap.fillAll('rgba(0, 0, 0, 0.5)'); // 背景

        for (let x = 0; x < this._mapWidth; x++) {
            for (let y = 0; y < this._mapHeight; y++) {
                if ($gameMap.isOpaque(x, y)) {
                    this.bitmap.fillRect(x * this._size, y * this._size, this._size, this._size, '#666666'); // 壁
                } else {
                    this.bitmap.fillRect(x * this._size, y * this._size, this._size, this._size, '#333333'); // 床
                }
            }
        }
    };

    Sprite_Minimap.prototype.update = function() {
        Sprite.prototype.update.call(this);
        if (this.visible && (Graphics.frameCount % 20 === 0)) { // 負荷軽減のため20フレームに一度更新
            this.drawDynamicObjects();
        }
    };

    Sprite_Minimap.prototype.drawDynamicObjects = function() {
        this.drawMap(); // 基本地形の再描画（タイルが変わる可能性も考慮）
        
        // プレイヤーの描画
        const px = $gamePlayer.x;
        const py = $gamePlayer.y;
        this.bitmap.fillRect(px * this._size, py * this._size, this._size, this._size, '#ffff00'); // プレイヤー（黄）

        // 敵の描画
        if ($gameMap._enemyMapObjects) {
            $gameMap._enemyMapObjects.forEach(enemy => {
                if (enemy.isAlive() && !enemy.isErase()) {
                    const ex = enemy._event.x;
                    const ey = enemy._event.y;
                    this.bitmap.fillRect(ex * this._size, ey * this._size, this._size, this._size, '#ff0000'); // 敵（赤）
                }
            });
        }
    };

    Sprite_Minimap.prototype.updateVisibility = function() {
        this.visible = ($gameMap._tilesetId === 4); // 指定のタイルセットID（ダンジョン）のみ表示
    };

    // Scene_Map への統合
    const _Scene_Map_createSpriteset = Scene_Map.prototype.createSpriteset;
    Scene_Map.prototype.createSpriteset = function() {
        _Scene_Map_createSpriteset.call(this);
        this.createMinimap();
    };

    Scene_Map.prototype.createMinimap = function() {
        this._minimap = new Sprite_Minimap();
        this.addChild(this._minimap);
    };

    const _Scene_Map_onMapLoaded = Scene_Map.prototype.onMapLoaded;
    Scene_Map.prototype.onMapLoaded = function() {
        _Scene_Map_onMapLoaded.call(this);
        if (this._minimap) {
            this._minimap.createBitmap();
            this._minimap.updateVisibility();
        }
    };


})();

