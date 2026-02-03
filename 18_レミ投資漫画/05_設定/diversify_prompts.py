import os
import re

target_dir = r"c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画"

# 1. レミの容姿指示の強化
remi_desc = "Remi (Woman): LONG SHINY SILVER hair (PLATINUM WHITE), Vibrant RED eyes, Red blazer, Black lace top, Cool & Intelligent. BARE HANDS (no gloves)."
yuto_desc = "Yuto (Boy): Short Black hair, Black GAKURAN school uniform, Energetic & Learner. BARE HANDS (no gloves)."

# 2. パリエーション設定
patterns = [
    {
        "name": "A: Standard",
        "scene_setting": "Quiet library or study room with bookshelves",
        "p1_panel3_scene": "Yuto's shocked face. He realizes his mistake. Positioned BOTTOM-RIGHT.",
        "p1_panel3_speech": "ハッ…！\nそうだったのか…",
        "p1_panel3_effects": "Shock lines, sweat drop",
        "p2_p4_scene": "Back to the main shot. Remi and Yuto facing each other. Yuto (Left): Determined expression, clenched fist. Remi (Right): Proud/Satisfied smile.",
        "p2_p4_action_speech": "信頼の重みが違うのか…僕も種銭からコツコツ積み上げます！",
        "style_extra": "MUST: Remi has PLATINUM SILVER hair, never brown."
    },
    {
        "name": "B: Dynamic",
        "scene_setting": "Sunny outdoor cafe terrace with plants and city background",
        "p1_panel3_scene": "Yuto's eyes sparkling with excitement. He's leaning in. Positioned BOTTOM-RIGHT.",
        "p1_panel3_speech": "すごいや！\nそんな秘密があったなんて！",
        "p1_panel3_effects": "Action lines, sparkles, glowing eyes",
        "p2_p4_scene": "Dynamic low-angle shot. Yuto (Left) leaping with joy, Remi (Right) pointing towards the future with a brave smile.",
        "p2_p4_action_speech": "ワクワクしてきました！すぐに行動に移します！",
        "style_extra": "MUST: Remi has PLATINUM SILVER hair, never brown. Use dynamic perspective and diagonal panel borders."
    },
    {
        "name": "C: Serious",
        "scene_setting": "High-rise lounge at sunset, orange and purple sky visible through windows",
        "p1_panel3_scene": "Close-up of Yuto's serious face. He is looking down, then looks up with sharp eyes. Positioned BOTTOM-RIGHT.",
        "p1_panel3_speech": "…なるほど。\n本当の戦いはここからなんですね。",
        "p1_panel3_effects": "Dramatic shadows, floating dust particles, cinematic lighting",
        "p2_p4_scene": "Silhouette or side profile shot. Yuto (Left) looking at his hands, Remi (Right) watching him warmly. Cinematic wide composition.",
        "p2_p4_action_speech": "この教え、一生忘れません。覚悟が決まりました。",
        "style_extra": "MUST: Remi has PLATINUM SILVER hair, never brown. Use cinematic lighting and deep shadows."
    },
    {
        "name": "D: Comedy",
        "scene_setting": "Busy street corner with neon signs and many people passing by",
        "p1_panel3_scene": "Yuto falling over in comedic shock (exaggerated pose). Positioned BOTTOM-RIGHT.",
        "p1_panel3_speech": "ぎえぇー！\n僕の今までのやり方は一体…！",
        "p1_panel3_effects": "Exaggerated emotion marks, '?!' symbols, speed lines",
        "p2_p4_scene": "Yuto (Left) bowing deeply (dogeza style or energetic bow), Remi (Right) looking down with a teasing smile and a fan or pointing.",
        "p2_p4_action_speech": "レミ師匠！一生ついていきます！教えてください！",
        "style_extra": "MUST: Remi has PLATINUM SILVER hair, never brown. Use comedic expressions and Chibi-style reactions for background effects."
    }
]

def update_file(filepath, index):
    pattern = patterns[index % len(patterns)]
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # レミの容姿指示を強化
    remis = re.findall(r"Remi \(Woman\):.*", content)
    for r in remis:
        content = content.replace(r, remi_desc)
    
    # ゆうとの定義も一貫性
    yutos = re.findall(r"Yuto \(Boy\):.*", content)
    for y in yutos:
        content = content.replace(y, yuto_desc)

    # Style Specifications に追記
    if pattern["style_extra"] not in content:
        content = content.replace("- Professional manga quality", f"- Professional manga quality\n- {pattern['style_extra']}")

    # シーン・リアクション・コマ割りの多様化
    # 1ページ目
    content = re.sub(r"SCENE SETTING:\n- Location:.*", f"SCENE SETTING:\n- Location: {pattern['scene_setting']}", content)
    content = re.sub(r"Panel 3 - Shock/Realization\nScene:.*", f"Panel 3 - Reaction\nScene: {pattern['p1_panel3_scene']}", content)
    content = re.sub(r"Characters: Yuto \(Black hair, Gakuran, eyes wide open\)\nEffects:.*", f"Characters: Yuto (Black hair, Gakuran)\nEffects: {pattern['p1_panel3_effects']}", content)
    
    # セリフはTIPごとにユニークな場合があるので、特定の構造のみ置換
    # 汎用的なセリフの場合は置換
    content = content.replace("ハッ…！\nそうだったのか…", pattern["p1_panel3_speech"])

    # 2ページ目
    content = re.sub(r"Panel 4 - Conclusion/Action\nScene:.*", f"Panel 4 - Conclusion/Action\nScene: {pattern['p2_p4_scene']}", content)
    # 2ページ目のDIALOGUE_ACTIONは末尾の「なるほど！実践してみます！」系のみ置換を試みるが、
    # 101個すべて違う可能性があるので、プロンプト本文側のみ置換
    content = content.replace("なるほど！実践してみます！\nその意気よ。\n一歩一歩着実にね。", pattern['p2_p4_action_speech'] + "\nその意気よ。\n一歩一歩着実にね。")

    # 変数一覧のSCENEも更新
    content = re.sub(r"\| SCENE \| .* \|", f"| SCENE | {pattern['scene_setting']} |", content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

# ファイル取得
files = []
for root, dirs, filenames in os.walk(target_dir):
    for filename in filenames:
        if filename.startswith("No") and filename.endswith("_プロンプト.md"):
            files.append(os.path.join(root, filename))

files.sort() # No順に並べる

updated_count = 0
for i, filepath in enumerate(files):
    if update_file(filepath, i):
        updated_count += 1

print(f"Total files: {len(files)}")
print(f"Updated files: {updated_count}")
