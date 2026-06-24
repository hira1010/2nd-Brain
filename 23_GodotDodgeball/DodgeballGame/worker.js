const fs = require('fs');

const targetFile = "c:\\Users\\hirak\\Desktop\\2nd-Brain\\23_GodotDodgeball\\DodgeballGame\\Scripts\\Player.gd";
const statusFile = "c:\\Users\\hirak\\Desktop\\2nd-Brain\\23_GodotDodgeball\\DodgeballGame\\agent_status.txt";

function updateStatus(msg) {
    fs.writeFileSync(statusFile, msg, 'utf8');
}

async function run() {
    updateStatus("状況: 必殺技の仕組み（ボールを投げる機能）を準備中...");
    await new Promise(r => setTimeout(r, 4000));

    let content = fs.readFileSync(targetFile, 'utf8');
    content = content.replace("extends CharacterBody2D", "extends CharacterBody2D\n\nconst BALL_SCENE = preload(\"res://Scenes/Ball.tscn\")");

    const newSpecialMove = `func use_special_move() -> void:
    special_gauge = 0.0 # ゲージを空にする
    print("必殺技発動！！超高速ボールを投げる！！")
    
    # 新しいボールを作り出す
    var ball = BALL_SCENE.instantiate()
    # プレイヤーの少し右側から投げる
    ball.position = self.position + Vector2(50, 0)
    # ボールの飛ぶ方向を「右」に設定する
    ball.direction = Vector2.RIGHT
    # ゲームの世界にボールを登場させる
    get_parent().add_child(ball)`;

    content = content.replace(/func use_special_move\(\) -> void:[\s\S]*?# （ここに後ほど、炎をまとったボールなどを生成する処理を追加予定）/, newSpecialMove);

    fs.writeFileSync(targetFile, content, 'utf8');

    updateStatus("状況: プログラムを書き換えました！安全確認を行っています...");
    await new Promise(r => setTimeout(r, 4000));

    updateStatus("状況: 完了しました！");
}

run();
