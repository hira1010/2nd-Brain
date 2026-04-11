/*:
 * @target MZ
 * @plugindesc ABS_Core v2.0 (言霊シューター 強化版コア)
 * @author Antigravity
 * 
 * @help ロジックとステート管理を担当するコアプラグインです。
 */

(() => {
    "use strict";

    window.ABS = window.ABS || {};
    
    // =========================================================================
    // 1. ステート管理
    // =========================================================================
    ABS.M = {
        init: function () {
            ABS.State = {
                nextId: 1, 
                cooldown: 0, 
                invin: 0, 
                pS: [], // Player Projectiles
                eS: [], // Enemy Projectiles
                onomas: [], 
                dropItems: [], // Drop Items [NEW]
                stop: 0,
                exp: 0, 
                level: 1,
                wordPower: 1.0 // 言葉の力
            };
            const p = $gamePlayer;
            if (p) {
                p._sHp = 100; p._spG = 0; p._isG = false;
            }
        },

        update: function () {
            if (!$gameMap || !$gamePlayer || !ABS.State) return;
            if (ABS.State.stop > 0) return;

            if (ABS.State.cooldown > 0) ABS.State.cooldown--;
            if (ABS.State.invin > 0) ABS.State.invin--;
            
            this.updateProjectiles(ABS.State.pS);
            this.updateProjectiles(ABS.State.eS);
            this.updateOnomas();
            this.updateDrops(); 
            this.updateInput();
            
            // 衝突判定
            ABS.Collision.check();
        },

        // 入力処理
        updateInput: function () {
            const p = $gamePlayer;
            if (!p) return;
            if (!p._isG) {
                if (Input.isTriggered("ok") || TouchInput.isTriggered()) this.atk();
                if (Input.isTriggered("escape")) this.ultimate(); // [NEW] 必殺技
                if (Input.isTriggered("prevW")) this.changeW(-1);
                if (Input.isTriggered("nextW")) this.changeW(1);
            }
            p._isG = (Input.isPressed("shield") && (p._spG || 0) > 0);
            if (p._isG) {
                p._spG = Math.max(0, (p._spG || 0) - 0.5);
            } else {
                p._spG = Math.min(100, (p._spG || 0) + 0.1); // 自動回復を少し抑える
            }
        },

        // 必殺技：極大爆発 [NEW]
        ultimate: function() {
            const p = $gamePlayer;
            if ((p._spG || 0) < 100) {
                AudioManager.playSe({ name: "Buzzer1", volume: 80, pitch: 100, pan: 0 });
                return;
            }
            p._spG = 0;
            // 演出
            $gameScreen.startFlash([255, 255, 255, 255], 60);
            AudioManager.playSe({ name: "Explosion2", volume: 100, pitch: 70, pan: 0 });
            ABS.onoma(p.x, p.y - 1, "極大爆発！！", "yellow", "ウニフラ", 30);
            
            // 全敵撃破
            $gameMap.events().forEach(e => {
                if (e && e.note && e.note.includes("<ABS>") && !e._erased) {
                    const dist = Math.sqrt(Math.pow(p.x - e.x, 2) + Math.pow(p.y - e.y, 2));
                    if (dist < 15) { // 画面内程度
                        e._hp = 0;
                        ABS.Collision.hitEnemy({ power: 999, anim: 107, name: "消滅" }, e, true);
                    }
                }
            });
        },

        // 攻撃処理
        atk: function () {
            if (ABS.State.cooldown > 0) return;
            const p = $gamePlayer;
            const weaponId = $gameVariables?.value(5) || 1;
            const weaponData = ABS.WeaponData[weaponId] || ABS.WeaponData[1];
            
            const d = p.direction();
            const range = (weaponData.range || 6) + (ABS.State.level * 0.2);
            const power = (weaponData.pwr || 1) * ABS.State.wordPower;
            // サイズの上限を 0.5倍（マスの 1/4）に極限まで制限し、成長も停止 (ナノ・スケール調整)
            const scale = Math.min(0.5, (weaponData.scale || 0.2) + (ABS.State.level * 0.0));
            
            if (weaponData.type === "triple") {
                this.createProjectile(p.x, p.y, d, range, weaponData.pic, power, scale, weaponData.text, weaponData.itemId);
                // 左右15度くらいの方向に飛ばす（簡易的に座標調整）
                if (d === 2 || d === 8) {
                    this.createProjectile(p.x - 0.5, p.y, d, range, weaponData.pic, power, scale, weaponData.text, weaponData.itemId);
                    this.createProjectile(p.x + 0.5, p.y, d, range, weaponData.pic, power, scale, weaponData.text, weaponData.itemId);
                } else {
                    this.createProjectile(p.x, p.y - 0.5, d, range, weaponData.pic, power, scale, weaponData.text, weaponData.itemId);
                    this.createProjectile(p.x, p.y + 0.5, d, range, weaponData.pic, power, scale, weaponData.text, weaponData.itemId);
                }
            } else if (weaponData.type === "explode") {
                this.createProjectile(p.x, p.y, d, range * 0.5, weaponData.pic, power * 2, scale * 2, weaponData.text, weaponData.itemId);
            } else {
                this.createProjectile(p.x, p.y, d, range, weaponData.pic, power, scale, weaponData.text, weaponData.itemId);
            }
            
            ABS.State.cooldown = weaponData.cd || 12;
            if (weaponData.se) {
                AudioManager.playSe({ name: weaponData.se, volume: 90, pitch: 110, pan: 0 });
            }
        },

        createProjectile: function (x, y, dir, range, pic, power, scale, text, anim) {
            let tx = x, ty = y;
            if (dir === 2) ty += range;
            if (dir === 4) tx -= range;
            if (dir === 6) tx += range;
            if (dir === 8) ty -= range;

            ABS.State.pS.push({
                id: ABS.State.nextId++, x: x, y: y,
                tx: tx, ty: ty, pic: pic, power: power, life: 60, frame: 0,
                curX: x, curY: y, name: text, anim: anim || 1,
                hits: [], scale: scale
            });
        },

        changeW: function (n) {
            let id = $gameVariables?.value(5) || 1;
            id += n;
            if (id < 1) id = 12; // 12種類に増加
            if (id > 12) id = 1;
            $gameVariables?.setValue(5, id);
            AudioManager.playSe({ name: "Equip1", volume: 80, pitch: 120, pan: 0 });
        },

        updateProjectiles: function (list) {
            if (!list) return;
            for (let i = list.length - 1; i >= 0; i--) {
                const d = list[i];
                d.frame++;
                const rate = d.frame / 60;
                d.curX = d.x + (d.tx - d.x) * rate;
                d.curY = d.y + (d.ty - d.y) * rate;
                if (d.frame >= 60) list.splice(i, 1);
            }
        },

        updateOnomas: function () {
            const list = ABS.State.onomas;
            if (!list) return;
            for (let i = list.length - 1; i >= 0; i--) {
                list[i].life--;
                if (list[i].life <= 0) list.splice(i, 1);
            }
        },

        updateDrops: function () {
           const list = ABS.State.dropItems;
           if (!list) return;
           const p = $gamePlayer;
           for (let i = list.length - 1; i >= 0; i--) {
               const item = list[i];
               const dist = Math.sqrt(Math.pow(item.x - p.x, 2) + Math.pow(item.y - p.y, 2));
               if (dist < 0.6) {
                   this.collectDrop(item);
                   list.splice(i, 1);
               } else if (dist < 3.0) { // マジックハンド（吸い寄せ）
                    item.x += (p.x - item.x) * 0.1;
                    item.y += (p.y - item.y) * 0.1;
               }
           }
        },

        collectDrop: function (item) {
            if (item.type === "exp") {
                this.gainExp(item.val);
                AudioManager.playSe({ name: "Item1", volume: 100, pitch: 150, pan: 0 });
            } else if (item.type === "hp") {
                $gamePlayer._sHp = Math.min(100, ($gamePlayer._sHp || 100) + 10);
                AudioManager.playSe({ name: "Heal1", volume: 100, pitch: 150, pan: 0 });
            }
        },

        gainExp: function (v) {
            ABS.State.exp += v;
            const needed = 50 + (ABS.State.level * 30);
            if (ABS.State.exp >= needed) {
                ABS.State.exp -= needed;
                ABS.State.level++;
                ABS.State.wordPower += 0.2;
                AudioManager.playSe({ name: "LevelUp", volume: 100, pitch: 100, pan: 0 });
                ABS.onoma($gamePlayer.x, $gamePlayer.y, "言葉の力が上昇！！", "yellow", "ウニフラ", 22);
            }
        }
    };

    // =========================================================================
    // 2. 衝突判定クラス
    // =========================================================================
    ABS.Collision = {
        check: function () {
            const p = $gamePlayer;
            if (!p || !ABS.State) return;

            // プレイヤー弾 -> 敵
            ABS.State.pS.forEach(d => {
                $gameMap.events().forEach(e => {
                    if (e && e.note && e.note.includes("<ABS>") && !e._erased && !d.hits.includes(e.eventId())) {
                        const dist = Math.sqrt(Math.pow(d.curX - e._realX, 2) + Math.pow(d.curY - e._realY, 2));
                        // 半径を基本 1.0とし、スケール(scale)の半分を加味する (すり抜け防止・大型弾対応)
                        const radius = 1.0 + (d.scale || 0) * 0.5;
                        if (dist < radius) {
                            this.hitEnemy(d, e);
                            d.hits.push(e.eventId());
                        }
                    }
                });
            });

            // 敵弾 -> プレイヤー
            ABS.State.eS.forEach((d, i, arr) => {
                const dist = Math.sqrt(Math.pow(d.curX - p.x, 2) + Math.pow(d.curY - p.y, 2));
                // 敵弾判定も 0.8マスへ拡大
                if (dist < 0.8) {
                    this.hitPlayer(d);
                    arr.splice(i, 1);
                }
            });
        },

        hitEnemy: function (d, e, isUltimate = false) {
            const enemyId = Number(e.note.match(/<EnemyId:\s*(\d+)>/)?.[1] || 1);
            const enemyBase = ABS.EnemyData[enemyId] || { hp: 3, exp: 10 };
            
            e._hp = (e._hp === undefined ? enemyBase.hp : e._hp) - (d.power || 1);
            $gameTemp?.reserveAnimation(e, d.anim || 1);
            ABS.onoma(e.x, e.y - 0.5, d.name, "red");
            
            // SP上昇 [NEW]
            if (!isUltimate) {
                $gamePlayer._spG = Math.min(100, ($gamePlayer._spG || 0) + 5);
            }
            
            if (e._hp <= 0) {
                e.erase();
                ABS.onoma(e.x, e.y, "撃破！！", "yellow", "ウニフラ");
                // ドロップ生成
                ABS.State.dropItems.push({ id: ABS.State.nextId++, x: e.x, y: e.y, type: "exp", val: enemyBase.exp || 10 });
                if (Math.random() < 0.3) {
                    ABS.State.dropItems.push({ id: ABS.State.nextId++, x: e.x, y: e.y + 0.2, type: "hp", val: 10 });
                }
            }
        },

        hitPlayer: function (d) {
            const p = $gamePlayer;
            if (p._isG) {
                p._spG = Math.max(0, (p._spG || 0) - 10);
                AudioManager.playSe({ name: "Shield1", volume: 100, pitch: 150, pan: 0 });
                return;
            }
            p._sHp = (p._sHp || 100) - 10;
            if (p._sHp <= 0) {
                SceneManager.goto(Scene_Gameover);
            }
        }
    };

    // ヘルパー: オンマトペ生成
    ABS.onoma = function (x, y, t, c, p, fs) { 
        if (ABS.State && ABS.State.onomas) {
            ABS.State.onomas.push({ id: ABS.State.nextId++, x: x, y: y, text: t, color: c, pic: p, life: 60, fs: fs }); 
        }
    };

    // DataManager hooks
    const _DM_setup = DataManager.setupNewGame;
    DataManager.setupNewGame = function () {
        _DM_setup.call(this);
        ABS.M.init();
    };

})();
