// RPG Maker MZ Plugin Virtual Test Runner
// このスクリプトはMZプラグインの文法チェックと初期化・更新ループの安全性を検証します。

const fs = require('fs');
const path = require('path');

// 仮想のツクールグローバル環境
global.window = global;
global.Input = { keyMapper: {}, gamepadMapper: {}, isPressed: () => false, isTriggered: () => false };
global.TouchInput = { isTriggered: () => false, isPressed: () => false, x: 0, y: 0 };
global.AudioManager = { playSe: function() {} };
global.ImageManager = { loadPicture: function(){ return { isReady: () => true, width: 100, height: 100 }; }, loadFace: function(){} };
global.Graphics = { width: 816, height: 624 };
global.Bitmap = function() { this.drawText = function(){}; this.blt = function(){}; this.isReady = () => true; this.clear = function(){}; this.fillRect = function(){}; };

global.Sprite = function() { this.scale = {x: 1, y: 1}; this.anchor = {x: 0, y: 0}; this.width = 100; this.height = 100; this.addChild = function(){}; this.removeChild = function(){}; };
global.Sprite.prototype = { initialize: function(){}, update: function(){} };

global.$gamePlayer = { 
    x: 5, y: 5, 
    _realX: 5, _realY: 5, 
    screenX: () => 100, screenY: () => 100, 
    direction: () => 2, setMoveSpeed: () => {} 
};
global.$gameMap = { 
    events: () => [], 
    adjustX: (x)=>x, adjustY: (y)=>y 
};
global.$gameVariables = { value: () => 0, setValue: () => {} };
global.$gameParty = { leader: () => ({ hp: 100, hpRate: () => 1.0, faceName: () => '', faceIndex: () => 0 }), hasItem: () => false, gainItem: () => {} };
global.$gameMessage = { isBusy: () => false, add: () => {} };
global.$gameTemp = { reserveAnimation: function() {} };

global.SceneManager = { _scene: { _mangaCutin: { start: () => {} } }, isSceneChanging: () => false };
global.DataManager = { setupNewGame: function() {} };
global.Scene_Gameover = function() {};

global.Scene_Map = function() { this.addChild = function(){}; };
global.Scene_Map.prototype = { 
    start: function(){}, 
    update: function(){},
    createSpriteset: function(){},
    isActive: function(){ return true; },
    isMenuCalled: function(){ return false; }
};
global.Sprite_Character = function() {};
global.Sprite_Character.prototype = { update: function(){} };

// 5. テスト実行 (プラグインの読み込み)
const pluginsToTest = [
    "ABS_Config.js",
    "ABS_Core.js",
    "ABS_View.js",
    "ABS_Support.js"
];

pluginsToTest.forEach(pluginFile => {
    const pluginPath = path.join(__dirname, "../js/plugins", pluginFile);
    if (fs.existsSync(pluginPath)) {
        console.log(`[Test Runner] Loading plugin: ${pluginFile}`);
        const code = fs.readFileSync(pluginPath, "utf8");
        try {
            eval(code);
        } catch (e) {
            console.error(`[Test Runner] ERROR in ${pluginFile}:`, e);
            throw e;
        }
    } else {
        console.warn(`[Test Runner] Plugin not found: ${pluginFile}`);
    }
});

try {
    console.log(`[Test Runner] Parsing successful. Initializing ABS...`);
    
    // システムの初期化 (DataManager経由または直接)
    if (typeof ABS !== 'undefined' && ABS.M && ABS.M.init) {
        ABS.M.init();
    }
    
    console.log(`[Test Runner] Initialization successful. Let's test Scene_Map injection...`);

    // 2. Scene_Map のモック実行
    const scene = new Scene_Map();
    if (scene.createSpriteset) scene.createSpriteset();
    if (scene.start) scene.start();
    
    // 3. 仮想の update ループを 5回 回す（初期化後のアクセスで undefined が出ないかのストレステスト）
    for (let i = 0; i < 5; i++) {
        scene.update();
    }
    console.log(`[Test Runner] Virtual 5-frame update loop successful. No crashes!`);
    
    process.exit(0);

} catch (e) {
    console.error(`\x1b[31m[Test Runner] CRITICAL ERRORS DETECTED!\x1b[0m`);
    console.error(e.stack);
    process.exit(1);
}
