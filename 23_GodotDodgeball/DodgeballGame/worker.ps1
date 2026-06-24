$Path = "c:\Users\hirak\Desktop\2nd-Brain\23_GodotDodgeball\DodgeballGame\Scripts\Player.gd"
$StatusFile = "c:\Users\hirak\Desktop\2nd-Brain\23_GodotDodgeball\DodgeballGame\agent_status.txt"

function Update-Status($msg) {
    Set-Content -Path $StatusFile -Value $msg -Encoding UTF8
}

Update-Status "状況: 必殺技の仕組み（ボールを投げる機能）を準備中..."
Start-Sleep -Seconds 4

$Content = Get-Content -Path $Path -Raw -Encoding UTF8
$Content = $Content -replace "extends CharacterBody2D", "extends CharacterBody2D`n`nconst BALL_SCENE = preload(`"res://Scenes/Ball.tscn`")"

$OldText = '(?s)func use_special_move\(\) -> void:.*?# （ここに後ほど、炎をまとったボールなどを生成する処理を追加予定）'
$NewText = "func use_special_move() -> void:`n    special_gauge = 0.0 # ゲージを空にする`n    print(`"必殺技発動！！超高速ボールを投げる！！`")`n`n    # 新しいボールを作り出す`n    var ball = BALL_SCENE.instantiate()`n    # プレイヤーの少し右側から投げる`n    ball.position = self.position + Vector2(50, 0)`n    # ボールの飛ぶ方向を「右」に設定する`n    ball.direction = Vector2.RIGHT`n    # ゲームの世界にボールを登場させる`n    get_parent().add_child(ball)"

$Content = $Content -replace $OldText, $NewText
Set-Content -Path $Path -Value $Content -Encoding UTF8

Update-Status "状況: プログラムを書き換えました！安全確認を行っています..."
Start-Sleep -Seconds 4

Update-Status "状況: 完了しました！"
