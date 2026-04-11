/*:
 * @target MZ
 * @plugindesc ABS_Config v1.0 [言霊シューター 設定データ]
 * @author Antigravity
 * 
 * @help 言霊（武器）や敵のパラメータを定義する設定ファイルです。
 */

(() => {
    "use strict";

    window.ABS = window.ABS || {};
    
    // 言霊（武器）データの定義
    // pwr: 威力, range: 射程, cd: クールダウン(フレーム), scale: 言霊の初期サイズ
    ABS.WeaponData = {
        1: { name: "バーン", text: "バーン！", pic: "12.バーン", pwr: 2.0, range: 2.0, spd: 12, cd: 30, itemId: 31, scale: 0.5, se: "Fire1", info: "【標準】火属性のバランス弾。" },
        2: { name: "ドドド", text: "ドドド！", pic: "03.ドドド", pwr: 4.0, range: 1.0, spd: 20, cd: 45, itemId: 32, scale: 0.8, se: "Earth1", info: "【重撃】土属性の超威力弾。" },
        3: { name: "ドキドキ", text: "ドキドキ", pic: "01.ドキドキ", pwr: 1.2, range: 4.0, spd: 8, cd: 15, itemId: 33, scale: 0.4, se: "Flash1", info: "【射抜き】高速・長射程の光弾。" },
        4: { name: "ふわっ", text: "ふわっ", pic: "02.ふわっ", pwr: 0.8, range: 3.0, spd: 40, cd: 20, itemId: 34, scale: 0.6, se: "Wind1", info: "【浮遊】風属性のゆっくり飛ぶ弾。" },
        5: { name: "ちゅちゅ", text: "ちゅちゅ", pic: "04.ちゅちゅ", pwr: 1.5, range: 1.0, spd: 10, cd: 10, itemId: 35, scale: 0.3, se: "Bite", info: "【至近】体力を奪うような鋭い一撃。" },
        6: { name: "きゅん", text: "きゅん", pic: "14.きゅん", pwr: 1.0, range: 2.0, spd: 15, cd: 25, itemId: 36, scale: 0.5, se: "Heal1", info: "【衝撃】強い閃光で撃破する。" },
        7: { name: "わくわく", text: "わくわく", pic: "15.わくわく", pwr: 1.2, range: 3.0, spd: 15, cd: 20, itemId: 37, scale: 0.5, se: "Powerup", info: "【拡散】不思議な光の弾。" },
        8: { name: "ギュンギュン", text: "ギュンギュン！", pic: "06.ああっ", pwr: 2.5, range: 2.5, spd: 15, cd: 30, itemId: 45, scale: 0.6, se: "Piston1", info: "【重圧】ピストン運動で押し込む弾。" },
        9: { name: "シュトッ", text: "シュトッ", pic: "02.ふわっ", pwr: 1.8, range: 3.5, spd: 20, cd: 20, itemId: 46, scale: 0.5, se: "Piston2", info: "【貫通】鋭い突き出しの音弾。" },
        10: { name: "ズドドド", text: "ズドドド！！", pic: "03.ドドド", pwr: 3.5, range: 1.5, spd: 10, cd: 40, itemId: 47, scale: 0.8, se: "Piston3", info: "【連打】連続したピストン攻撃。" },
        11: { name: "ぬぷっ", text: "ぬぷっ…", pic: "08.ぐちゅっ", pwr: 1.5, range: 2.0, spd: 12, cd: 25, itemId: 48, scale: 0.7, se: "Piston4", info: "【浸透】ねっとりとした言葉の力。" },
        12: { name: "ズキュン！", text: "ズキュン！", pic: "12.バーン", pwr: 5.0, range: 5.0, spd: 30, cd: 60, itemId: 49, scale: 1.0, se: "Piston5", info: "【極致】究極のピストン言霊。" }
    };

    // 敵データの追加設定（必要に応じて）
    ABS.EnemyData = {
        1: { hp: 3, speed: 0.02, exp: 10 },
        2: { hp: 5, speed: 0.03, exp: 20 },
        3: { hp: 15, speed: 0.01, exp: 50, boss: true }
    };

})();
