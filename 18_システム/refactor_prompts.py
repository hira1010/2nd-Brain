
import os
import re
import random
import json

# ターゲットディレクトリ
BASE_DIR = r"c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画"
TARGET_DIRS = [
    "01_投資の基礎知識",
    "02_マインド・哲学",
    "03_戦略・リスク管理",
    "04_未来・テクノロジー"
]

# シーン（背景）のバリエーション
SCENES = [
    "Modern high-rise office with panoramic city view",
    "Stylish cafe with warm lighting and wooden furniture",
    "Luxurious lounge bar with night city view",
    "Bright meeting room with a large whiteboard",
    "Quiet library or study room with bookshelves"
]

# 外部JSONから会話データを読み込む
try:
    with open("dialogues.json", "r", encoding="utf-8") as f:
        RICH_DIALOGUES = json.load(f)
except FileNotFoundError:
    print("Warning: dialogues.json not found. Using defaults.")
    RICH_DIALOGUES = {}

# デフォルトのセリフ生成 (辞書にない場合)
def get_default_dialogue(title, desc):
    return {
        "Intro": f"レミさん、{title}について教えてください！もっと詳しく知りたいです。",
        "Teach": "いい心がけね。でも、ただ知るだけじゃ意味がないわ。",
        "Desc": f"{desc} これが投資の本質よ。しっかり頭に叩き込みなさい。",
        "Action": "なるほど！実践してみます！"
    }

def get_dialogue(no, title, desc):
    if str(no) in RICH_DIALOGUES:
        return RICH_DIALOGUES[str(no)]
    return get_default_dialogue(title, desc)

# テンプレート (講義型・全コマキャラ有)
TEMPLATE = """# No.{NO} {TITLE} 2P漫画生成プロンプト

## TIP情報

| 項目 | 内容 |
| :--- | :--- |
| No | {NO} |
| タイトル | {TITLE} |
| 解説 | {DESC} |
| カテゴリー | {CATEGORY} |

---

## 1ページ目プロンプト

```text
[OUTPUT: 1200x1700 pixels, aspect ratio 12:17, portrait orientation]

MANDATORY IMAGE SPECIFICATIONS:
- Canvas Size: 1200 pixels width x 1700 pixels height
- Aspect Ratio: 12:17 (portrait)
- Resolution: High quality manga illustration

PANEL LAYOUT - PAGE 1:
MANGA PAGE 1 - VERTICAL DYNAMIC PANEL LAYOUT (READING ORDER: RIGHT TO LEFT, TOP TO BOTTOM)
- Panel 1 (TOP 40%): Large horizontal panel (Intro)
- Panel 2 (MIDDLE 30%): Medium horizontal panel (Conversation)
- Panel 3 (BOTTOM-RIGHT 15%): Small vertical panel (Reaction)
- Panel 4 (BOTTOM-LEFT 15%): Small vertical panel (Theme)
READING FLOW: Panel 1 -> Panel 2 -> Panel 3 (Right) -> Panel 4 (Left)

TEXT BOX REQUIREMENT:
In Panel 1, BOTTOM-RIGHT corner: Draw a BLACK rectangular box with WHITE border containing WHITE TEXT:
{TITLE}
Font: Bold, Clear Japanese Gothic font.

STYLE SPECIFICATIONS:
- Japanese manga style
- 6500K neutral white balance
- Clean bright colors with cel shading
- White panel borders with black outlines
- Pure white speech bubbles
- Professional manga quality

SCENE SETTING:
- Location: {SCENE}
- Atmosphere: Professional yet engaging

CHARACTERS (ALWAYS VISIBLE):
- Remi (Woman): Silky SILVER hair, Vibrant RED eyes, Red blazer, Black lace top, Cool & Intelligent.
- Yuto (Boy): Short Black hair, Black GAKURAN school uniform, Energetic & Learner.

Panel 1 - Introduction
Scene: {SCENE}. Yuto looks confused or eager, holding a smartphone or document. Remi looks coolly at him.
Characters: Yuto (leaning forward), Remi (standing with arms crossed)
Speech bubbles:
{DIALOGUE_INTRO}

---

Panel 2 - The Teach
Scene: Close-up of Remi's face. She is pointing a finger or looking sharp. Background has sparkle effects.
Characters: Remi (Silver hair, Red eyes, confident smile). Remi is positioned on the RIGHT side.
Speech bubble:
{DIALOGUE_TEACH}

---

Panel 3 - Shock/Realization
Scene: Yuto's shocked face. He realizes his mistake. Positioned BOTTOM-RIGHT.
Characters: Yuto (Black hair, Gakuran, eyes wide open)
Effects: Shock lines, sweat drop
Speech bubble:
ハッ…！
そうだったのか…

---

Panel 4 - Theme Display
Scene: Remi smiling mysteriously. Positioned BOTTOM-LEFT.
Characters: Remi (Side profile, Silver hair, Red eyes)
Speech bubble:
これが投資の真実よ

```

---

## 2ページ目プロンプト

```text
[OUTPUT: 1200x1700 pixels, aspect ratio 12:17, portrait orientation]

MANDATORY IMAGE SPECIFICATIONS:
- Canvas Size: 1200 pixels width x 1700 pixels height
- Aspect Ratio: 12:17 (portrait)
- Resolution: High quality manga illustration

PANEL LAYOUT - PAGE 2:
MANGA PAGE 2 - LECTURE STYLE SQUAD (READING ORDER: RIGHT TO LEFT, TOP TO BOTTOM)
- Panel 1 (TOP 50%): Large cinematic panel (Lecture with Visual)
- Panel 2 (MIDDLE-RIGHT 25%): Vertical panel (Point 1)
- Panel 3 (MIDDLE-LEFT 25%): Vertical panel (Point 2)
- Panel 4 (BOTTOM 25%): Wide conclusion panel (Action)
READING FLOW: Panel 1 -> Panel 2 (Right) -> Panel 3 (Left) -> Panel 4

STYLE SPECIFICATIONS:
- Japanese manga style
- 6500K neutral white balance
- Rich colors with dynamic contrast
- White panel borders with black outlines
- Pure white speech bubbles
- Luxurious golden and royal purple color scheme

SCENE SETTING:
- Location: {SCENE} (SAME AS PAGE 1)

**IMPORTANT: CHARACTERS MUST BE CONSISTENT WITH PAGE 1**
- Remi: Silky SILVER hair, Red eyes, Red blazer.
- Yuto: Short Black hair, Black GAKURAN uniform.

Panel 1 - Visual Lecture (CRITICAL: Remi must be in the frame)
Scene: Remi standing in front of a large holographic monitor or blackboard showing the concept of "{TITLE}". She is explaining it directly to Yuto.
Characters:
- Remi: Standing on the right, pointing at the visual behind her. (Silver hair, Red blazer)
- Yuto: Sitting or standing on the left, looking at the visual with admiration. (Black Gakuran)
Visual Background: Symbolic representation of {TITLE} (Charts, Coins, Crown, etc.) on the screen.
Speech bubbles: {DIALOGUE_DESC}

---

Panel 2 - Point 1 (Remi Explaining)
Scene: Close up of Remi emphasizing a point. Positioned MIDDLE-RIGHT.
Characters: Remi (Silver hair, Red eyes) raising one finger.
Speech bubbles: ポイント1：{TITLE}の重要性よ！
Effects: Sparkles, Golden background

---

Panel 3 - Point 2 (Yuto Understanding)
Scene: Yuto looking at a chart or visual, nodding. Positioned MIDDLE-LEFT.
Characters: Yuto (Black hair, Gakuran) holding a notebook or tablet.
Speech bubbles: なるほど、ポイント2の「実践」が大事なんだな！
Effects: Upward arrows, Growth symbols

---

Panel 4 - Conclusion/Action
Scene: Back to the main shot. Remi and Yuto facing each other.
Characters:
- Yuto (Left): Determined expression, clenched fist. "I will do it!" pose. (Black Gakuran)
- Remi (Right): Proud/Satisfied smile, hand on hip. (Silver hair, Red blazer)
Speech bubbles:
{DIALOGUE_ACTION}
その意気よ。
一歩一歩着実にね。

```

---

## 生成時の変数一覧

### 1ページ目

| 変数 | 値 |
| :--- | :--- |
| TIP_NUMBER | {NO} |
| TIP_TITLE | {TITLE} |
| DIALOGUE_INTRO | {DIALOGUE_INTRO} |
| DIALOGUE_TEACH | {DIALOGUE_TEACH} |
| SCENE | {SCENE} |

### 2ページ目

| 変数 | 値 |
| :--- | :--- |
| DIALOGUE_DESC | {DIALOGUE_DESC} |
| DIALOGUE_ACTION | {DIALOGUE_ACTION} |

---

## 保存ファイル名

- 1ページ目: No{NO}_{TITLE_SAFE}_p1.png
- 2ページ目: No{NO}_{TITLE_SAFE}_p2.png

---

## generate_imageツール実行用

```text
generate_image(
  ImageName: "remi_investment_no{NO}_p1",
  Prompt: [上記の1ページ目プロンプトのコードブロック内容をそのまま貼り付け]
)
```

```text
generate_image(
  ImageName: "remi_investment_no{NO}_p2",
  Prompt: [上記の2ページ目プロンプトのコードブロック内容をそのまま貼り付け]
)
```

### ステップ3: 結合プレビュー作成（任意）
2枚の画像を並べて見開きプレビューを作成する場合は、画像結合スクリプト.ps1 を使用してください。

---

作成日: 2026-02-03
ステータス: フルリニューアル完了（全ファイル統一・エラー解消済）
"""

def extract_info(content):
    # No抽出
    no_match = re.search(r'\|\s*No\s*\|\s*(\d+)\s*\|', content)
    if not no_match:
        return None
    no = no_match.group(1)
    
    # タイトル抽出
    title_match = re.search(r'\|\s*タイトル\s*\|\s*(.*?)[\s|]*\|', content)
    if not title_match:
        return None
    title = title_match.group(1).strip()
    
    # 解説抽出
    desc_match = re.search(r'\|\s*解説\s*\|\s*(.*?)[\s|]*\|', content)
    desc = ""
    if desc_match:
        desc = desc_match.group(1).strip()
        
    return no, title, desc

def process_files():
    total_processed = 0
    
    for subdir in TARGET_DIRS:
        dir_path = os.path.join(BASE_DIR, subdir)
        if not os.path.exists(dir_path):
            print(f"Directory not found: {dir_path}")
            continue
            
        category_name = subdir
            
        for filename in os.listdir(dir_path):
            if filename.endswith(".md"):
                file_path = os.path.join(dir_path, filename)

                # No.01も例外なく処理するため、スキップ条件を削除
                # 従来: if "No01" in filename ... continue
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    info = extract_info(content)
                    if not info:
                        print(f"Could not extract info from {filename}")
                        continue
                        
                    no, title, desc = info
                    
                    if not desc:
                        desc = title

                    title_safe = re.sub(r'[\\/:*?"<>|]', '', title).replace(' ', '_')

                    dialogue = get_dialogue(no, title, desc)
                    scene = random.choice(SCENES)

                    new_content = TEMPLATE.format(
                        NO=no,
                        TITLE=title,
                        DESC=desc,
                        CATEGORY=category_name,
                        TITLE_SAFE=title_safe,
                        DIALOGUE_INTRO=dialogue["Intro"],
                        DIALOGUE_TEACH=dialogue["Teach"],
                        DIALOGUE_DESC=dialogue["Desc"],
                        DIALOGUE_ACTION=dialogue["Action"],
                        SCENE=scene
                    )
                    
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    
                    print(f"Updated: {filename} (No.{no} {title})")
                    total_processed += 1
                    
                except Exception as e:
                    print(f"Error processing {filename}: {e}")

    print(f"Total processed: {total_processed}")

if __name__ == "__main__":
    process_files()
