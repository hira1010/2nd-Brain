// -----------------------------------------------------
// 深層仮想テスト (Deep Mocking Run)
// ABS_Ultimate.jsやABS_Support.jsに潜むランタイムエラーを
// 事前に強制検知するためのシミュレーター
// -----------------------------------------------------

require('./mock_env.js');

// Pluginファイルの読み込み (順序遵守)
require('../05_RPG制作/js/plugins/ABS_Support.js');
require('../05_RPG制作/js/plugins/ABS_Ultimate.js');

try {
  // 1. SceneManager の初期化 (Mock)
  SceneManager._scene = {
    _mangaCutin: { start: () => {} }
  };

  // 2. マップとプレイヤーの初期状態投入
  ABS.M.init();
  console.log("ABS Initialization Passed.");

  // 3. 仮想の敵イベントを用意
  // Enemy_Slime
  const slime = {
    eventId: () => 2,
    x: 8, y: 8,
    _absHp: 50, _absMaxHp: 50, _absAI: "chase", _absSpeed: 10,
    event: () => ({ note: "<abs_enemy_id: 1>" }),
    enemy: () => ({ params: [0,0,10,5,0,0,0], traits: [] })
  };
  
  // Enemy_Ghost (Shooter)
  const ghost = {
    eventId: () => 3,
    x: 12, y: 3,
    _absHp: 40, _absMaxHp: 40, _absAI: "shoot", _absSpeed: 15,
    event: () => ({ note: "<abs_enemy_id: 2>\n<abs_proj: 12.バーン>" }),
    enemy: () => ({ params: [0,0,20,5,0,0,0], traits: [] })
  };

  $gameMap.events = () => [null, null, slime, ghost];
  
  // 4. ゲーム内時間を進める（Updateループの仮想実行: 300フレーム）
  console.log("Simulating 300 frames of gameplay...");
  for (let i = 0; i < 300; i++) {
    // プレイヤーが動いたことにする
    $gamePlayer._x += 0.05;
    $gamePlayer._y += 0.02;

    // 定期的な攻撃（シミュレーション）
    if (i === 60) {
      $gameVariables.setValue(5, 1); // Weapon: バン！
      ABS.Action.atk(1); // Skill Action Start
    }
    
    // 定期的なシールド（シミュレーション）
    if (i === 120) {
      ABS.Action.guard(); // Guard
    }

    //敵が弾を撃ったことにする（Ghost）
    if (i % 90 === 0) {
      ABS.AI.fire(ghost);
    }

    // プラグイン全体の更新処理を流す
    ABS.M.update();
  }

  console.log("Simulation Result: Math operations, references, and AI survived.");

  // 5. 状態変数の整合性チェック
  if (global.freeze === 2) {
    throw new Error("Simulation resulted in a silent crash (freeze = 2). Check catch blocks in ABS_Ultimate.js.");
  }

  console.log("[QA Passed] The deep mock run completed successfully without runtime crashes.");
  process.exit(0);

} catch (e) {
  console.error("\n[CRITICAL RUNTIME ERROR CAUGHT]");
  console.error("The ABS simulation crashed due to the following runtime error:");
  console.error(e);
  process.exit(1);
}
