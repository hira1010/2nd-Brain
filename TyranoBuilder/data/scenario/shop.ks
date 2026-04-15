; shop.ks - ショップ画面
[cm]
[bg storage="bg_classroom.png" time="500"]

[iscript]
// ショップのタイトルや案内を表示するためのJS
var html = `
    <div id="shop_ui" style="position:absolute; left:100px; top:100px; width:1000px; height:500px; background:rgba(0,0,0,0.8); border:3px solid #ff69b4; border-radius:20px; z-index:9998; padding:20px; color:white; font-family:sans-serif;">
        <h1 style="text-align:center; color:#ff69b4; border-bottom:2px solid #ff69b4; padding-bottom:10px;">秘密のショップ</h1>
        <div style="display:flex; justify-content:space-around; margin-top:30px; flex-wrap:wrap;">
            <!-- バイブ -->
            <div style="text-align:center; width:180px;">
                <img src="data/fgimage/vibrator.png" style="width:120px; height:120px; object-fit:contain; border-radius:10px; background:white;">
                <h3 style="font-size:16px;">低周波バイブ</h3>
                <p style="font-size:12px;">快感UP</p>
                <p style="color:#ffd700; font-weight:bold;">¥ 5,000</p>
                <div id="btn_vibe" class="shop_btn" onclick="tyrano.plugin.kag.ftag.startTag('jump',{target:'*buy_vibrator'})">購入</div>
            </div>
            <!-- 強力バイブ -->
            <div style="text-align:center; width:180px;">
                <img src="data/fgimage/item_super_vibe.png" style="width:120px; height:120px; object-fit:contain; border-radius:10px; background:white;">
                <h3 style="font-size:16px;">強力マッサージ器</h3>
                <p style="font-size:12px;">快感大幅UP</p>
                <p style="color:#ffd700; font-weight:bold;">¥ 20,000</p>
                <div id="btn_super_vibe" class="shop_btn" onclick="tyrano.plugin.kag.ftag.startTag('jump',{target:'*buy_super_vibe'})">購入</div>
            </div>
            <!-- ローション -->
            <div style="text-align:center; width:180px;">
                <img src="data/fgimage/lotion.png" style="width:120px; height:120px; object-fit:contain; border-radius:10px; background:white;">
                <h3 style="font-size:16px;">特製ローション</h3>
                <p style="font-size:12px;">親密度UP</p>
                <p style="color:#ffd700; font-weight:bold;">¥ 3,000</p>
                <div id="btn_lotion" class="shop_btn" onclick="tyrano.plugin.kag.ftag.startTag('jump',{target:'*buy_lotion'})">購入</div>
            </div>
            <!-- アロマオイル -->
            <div style="text-align:center; width:180px;">
                <img src="data/fgimage/item_oil.png" style="width:120px; height:120px; object-fit:contain; border-radius:10px; background:white;">
                <h3 style="font-size:16px;">高級オイル</h3>
                <p style="font-size:12px;">親密度大幅UP</p>
                <p style="color:#ffd700; font-weight:bold;">¥ 15,000</p>
                <div id="btn_oil" class="shop_btn" onclick="tyrano.plugin.kag.ftag.startTag('jump',{target:'*buy_oil'})">購入</div>
            </div>
            <!-- カメラ -->
            <div style="text-align:center; width:180px;">
                <div style="width:120px; height:120px; line-height:120px; background:#444; margin:0 auto; border-radius:10px; font-size:40px;">📸</div>
                <h3 style="font-size:16px;">高性能カメラ</h3>
                <p style="font-size:12px;">売価1.5倍</p>
                <p style="color:#ffd700; font-weight:bold;">¥ 10,000</p>
                <div id="btn_camera" class="shop_btn" onclick="tyrano.plugin.kag.ftag.startTag('jump',{target:'*buy_camera'})">購入</div>
            </div>
        </div>
        <style>
            .shop_btn {
                background:#ff69b4; padding:10px; border-radius:5px; cursor:pointer; font-weight:bold; transition:0.2s;
            }
            .shop_btn:hover { background:#ff1493; transform:scale(1.05); }
            .shop_btn.purchased { background:#888; cursor:default; }
        </style>
    </div>
`;
$('.tyrano_base').append(html);

// 購入済みチェック
if (f.items.vibrator) { $('#btn_vibe').text('所持済み').addClass('purchased').removeAttr('onclick'); }
if (f.items.super_vibe) { $('#btn_super_vibe').text('所持済み').addClass('purchased').removeAttr('onclick'); }
if (f.items.lotion) { $('#btn_lotion').text('所持済み').addClass('purchased').removeAttr('onclick'); }
if (f.items.aroma_oil) { $('#btn_oil').text('所持済み').addClass('purchased').removeAttr('onclick'); }
if (f.items.camera) { $('#btn_camera').text('所持済み').addClass('purchased').removeAttr('onclick'); }
[endscript]

[glink text="戻る" x="550" y="620" width="100" height="40" color="black" target="*exit_shop"]

[s]

*buy_vibrator
[if exp="f.p_money >= 5000"]
    [iscript]
    f.p_money -= 5000;
    f.items.vibrator = true;
    [endscript]
    "バイブを購入しました！クリック時の快感がより高まります。"
[else]
    "お金が足りません…"
[endif]
[jump target="*refresh_shop"]

*buy_lotion
[if exp="f.p_money >= 3000"]
    [iscript]
    f.p_money -= 3000;
    f.items.lotion = true;
    [endscript]
    "ローションを購入しました！ヒロインと仲良くなりやすくなります。"
[else]
    "お金が足りません…"
[endif]
[jump target="*refresh_shop"]

*buy_super_vibe
[if exp="f.p_money >= 20000"]
    [iscript]
    f.p_money -= 20000;
    f.items.super_vibe = true;
    [endscript]
    "強力電動マッサージ器を購入しました！快感が爆発的に高まります。"
[else]
    "お金が足りません…"
[endif]
[jump target="*refresh_shop"]

*buy_oil
[if exp="f.p_money >= 15000"]
    [iscript]
    f.p_money -= 15000;
    f.items.aroma_oil = true;
    [endscript]
    "高級アロマオイルを購入しました！親密度が劇的に上昇します。"
[else]
    "お金が足りません…"
[endif]
[jump target="*refresh_shop"]

*buy_camera
[if exp="f.p_money >= 10000"]
    [iscript]
    f.p_money -= 10000;
    f.items.camera = true;
    [endscript]
    "高性能カメラを購入しました！写真の売価がアップします。"
[else]
    "お金が足りません…"
[endif]
[jump target="*refresh_shop"]

*refresh_shop
[iscript]
$('#shop_ui').remove(); // 一旦消して再表示
updatePleasureGauge(); // 所持金表示を更新
[endscript]
[jump target="shop.ks" storage="shop.ks"]

*exit_shop
[iscript]
$('#shop_ui').remove();
[endscript]
[jump storage="scene1.ks" target="*main_loop"]
