; title.ks - タイトル画面
[cm]
[bg storage="bg_classroom.png" time="500"]

[ptext layer="1" x="200" y="200" size="80" color="0xff69b4" text="HEROINE CLICKER" edge="0xffffff"]
[ptext layer="1" x="200" y="300" size="30" color="white" text="3-Engine Unified Edition"]

[glink text="最初から" x="550" y="450" width="200" height="40" color="pink" target="*start_game"]
[glink text="つづきから" x="550" y="510" width="200" height="40" color="blue" target="*load_game"]

[s]

*start_game
[cm]
[jump storage="scene1.ks"]

*load_game
[showload]
[jump target="*main_loop" storage="title.ks"]
