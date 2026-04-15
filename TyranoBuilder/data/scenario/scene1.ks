; scene1.ks - 詳細演出・ロジック移植版 (Ver 8.0)

[cm]
[iscript]
// 1. 変数と計算ロジック (初期化)
f.p_intimacy = 0.0;
f.p_pleasure = 0.0;
f.rank = 1;
f.p_money = 0;       // 所持金
f.items = {};      // 所持アイテム
f.shake_type = ""; // 演出判別用

// 音声ディレクトリの設定 (プロジェクト内相対パスに変更)
f.voice_dir = "data/sound/"; 

// ゲージ更新用の関数
window.updatePleasureGauge = function() {
    var $bar = $('#pleasure_gauge_bar');
    if ($bar.length === 0) {
        // ゲージがなければ作成
        var html = `
            <div id="pleasure_gauge_container" style="position:absolute; left:20px; top:20px; width:300px; height:30px; background:rgba(0,0,0,0.5); border:2px solid #ff69b4; border-radius:15px; overflow:hidden; z-index:9999; box-shadow: 0 0 10px #ff69b4;">
                <div id="pleasure_gauge_bar" style="width:0%; height:100%; background:linear-gradient(90deg, #ff1493, #ff69b4); transition: width 0.3s ease-out; box-shadow: 0 0 15px #ff1493;"></div>
                <div id="pleasure_gauge_text" style="position:absolute; width:100%; text-align:center; top:3px; color:white; font-weight:bold; font-family:sans-serif; text-shadow:1px 1px 2px black;">PLEASURE</div>
            </div>
            <div id="money_display" style="position:absolute; left:20px; top:60px; font-size:24px; color:#ffd700; font-weight:bold; font-family:sans-serif; text-shadow:2px 2px 2px black; z-index:9999;">
                ¥ <span id="money_val">0</span>
            </div>
        `;
        $('.tyrano_base').append(html);
        $bar = $('#pleasure_gauge_bar');
    }
    
    // ゲージの割合計算 (100で最大とする)
    var percent = Math.min(100, f.p_pleasure);
    $bar.css('width', percent + '%');
    
    // 所持金表示の更新
    $('#money_val').text(Math.floor(f.p_money).toLocaleString());
};

// ハート演出用のJavaScript関数 (位置を修正)
window.showHeartEffect = function(x, y) {
    var heartId = "heart_" + Date.now();
    var $heart = $('<img src="data/fgimage/heart.png" id="' + heartId + '">');
    $heart.css({
        position: 'absolute',
        left: (x - 25) + 'px',
        top: (y - 25) + 'px',
        width: '50px', 
        zIndex: 9999,
        pointerEvents: 'none',
        opacity: 1,
        transform: 'scale(0.3)'
    });
    $('.tyrano_base').append($heart);

    $heart.animate({
        top: (y - 150) + 'px',
        opacity: 0
    }, {
        duration: 800,
        step: function(now, fx) {
            if (fx.prop === "top") {
                var scale = 0.3 + (0.2 * (1 - (now - (y-150)) / 150));
                $(this).css("transform", "scale(" + scale + ")");
            }
        },
        complete: function() {
            $(this).remove();
        }
    });
};
[endscript]

; --- 演出の定義 (マクロ) ---

[macro name="show_heroine"]
    ; ランクと快感度に連動した立ち絵の判定
    [iscript]
    var img = "heroine1.png";
    if (f.rank == 2) img = "heroine2.png";
    if (f.rank == 3) img = "heroine3.png";
    
    // 表情（快感度）の上書き
    if (f.p_pleasure >= 70) {
        img = "heroine_rank1_excited.png";
    } else if (f.p_pleasure >= 30) {
        img = "heroine_rank1_blush.png";
    }
    tf.heroine_img = img;
    [endscript]

    ; 演出タイプによってアニメーションを変える
    [if exp="f.shake_type == 'shake'"]
        ; 胸の揺れ (上下に弾む)
        [chara_show name="heroine" storage="&tf.heroine_img" width="450" height="auto" left="415" top="20" time="0"]
        [anim name="heroine" top="+=15" time="50"]
        [anim name="heroine" top="-=15" time="50"]
        [anim name="heroine" top="+=10" time="50"]
        [anim name="heroine" top="-=10" time="50"]
        [iscript] f.shake_type = ""; [endscript]
    [elsif exp="f.shake_type == 'shiver'"]
        ; ビクッとする震え (左右)
        [chara_show name="heroine" storage="&tf.heroine_img" width="450" height="auto" left="415" top="20" time="0"]
        [quake time="150" count="3" hmax="5" wait="false"]
        [iscript] f.shake_type = ""; [endscript]
    [else]
        ; 通常表示
        [chara_show name="heroine" storage="&tf.heroine_img" width="450" height="auto" left="415" top="20" time="0"]
    [endif]
[endmacro]

; --- 初期画面構築 ---

[bg storage="bg_classroom.png" time="500"]
[chara_new name="heroine" storage="heroine1.png" jname="ヒロイン"]

*main_loop
[cm]
[show_heroine]

; ステータス表示 (数値テキスト)
[ptext name="status_rank" layer="1" x="350" y="20" size="30" color="0xff69b4" text="&'Rank: ' + f.rank" overwrite="true"]

; 当たり判定 (提供された座標をベースに clickable で配置)
; 耳 (600, 180)
[clickable x="550" y="130" width="100" height="100" target="*on_click_ear" mouseovertext="耳に触れる"]
; 胸 (550, 320)
[clickable x="500" y="280" width="280" height="180" target="*on_click_chest" mouseovertext="胸に触れる"]
; 股間 (580, 620)
[clickable x="520" y="580" width="220" height="130" target="*on_click_crotch" mouseovertext="体に触れる"]

; ゲージ更新
[iscript] updatePleasureGauge(); [endscript]

; 右下のボタン
[glink text="チェキ撮影" x="1050" y="550" width="150" height="40" color="pink" target="*take_photo"]
[glink text="ショップ" x="1050" y="610" width="150" height="40" color="blue" target="*open_shop"]

[s]

; --- イベントハンドラ ---

*on_click_ear
[iscript]
var inc_int = 1.5;
if (f.items.lotion) inc_int *= 1.5;
if (f.items.aroma_oil) inc_int *= 3.0; // アロマオイルは3倍
f.p_intimacy += inc_int;
f.shake_type = "shiver";
showHeartEffect(600, 180); 
[endscript]
; [playse storage="ear.wav"]
[jump target="*rank_check"]

*on_click_chest
[iscript]
var inc_int = 2.0;
var inc_ple = 5.0;
if (f.items.lotion) inc_int *= 1.5;
if (f.items.aroma_oil) inc_int *= 3.0;
if (f.items.vibrator) inc_ple *= 2.0;
if (f.items.super_vibe) inc_ple *= 4.0; // 強力バイブは4倍
f.p_intimacy += inc_int;
f.p_pleasure += inc_ple;
f.shake_type = "shake";
showHeartEffect(550, 320);
[endscript]
; [playse storage="chest.wav"]
[jump target="*rank_check"]

*on_click_crotch
[iscript]
var inc_int = 5.0;
var inc_ple = 10.0;
if (f.items.lotion) inc_int *= 1.5;
if (f.items.aroma_oil) inc_int *= 3.0;
if (f.items.vibrator) inc_ple *= 3.0;
if (f.items.super_vibe) inc_ple *= 6.0; // 股間+強力バイブは超強力
f.p_intimacy += inc_int;
f.p_pleasure += inc_ple;
f.shake_type = "shiver";
showHeartEffect(580, 620);
[endscript]
; [playse storage="crotch.wav"]
[jump target="*rank_check"]

*rank_check
[iscript]
if (f.p_intimacy > 100) f.rank = 3;
else if (f.p_intimacy > 40) f.rank = 2;
[endscript]
[jump target="*main_loop"]

*take_photo
[cm]
"「これは二人の協力活動（ビジネス）だからね」"
[quake time="300" count="5" hmax="10" wait="true"]
[iscript]
var income = (f.p_intimacy * 50 + f.p_pleasure * 100) * f.rank;
if (f.items.camera) income *= 1.5; // カメラアイテムがあれば1.5倍
f.p_money += income;
f.p_intimacy = 0;
f.p_pleasure = 0;
[endscript]
"（チェキを撮影し、金貨を得ました）"
[jump target="*main_loop"]

*open_shop
[cm]
; ショップ画面へ遷移（shop.ksを呼び出す）
[jump storage="shop.ks"]

[s]
