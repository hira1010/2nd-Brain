
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
        "Action": f"そうか…{title}の本質はここにあったんですね。"
    }

def get_dialogue(no, title, desc):
    if str(no) in RICH_DIALOGUES:
        return RICH_DIALOGUES[str(no)]
    return get_default_dialogue(title, desc)

# テンプレート (No.42準拠の構成)
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
【IMAGE_GENERATION_TASK】Generate a high-quality manga illustration BASE ON THE FOLLOWING VISUAL DESCRIPTION. DO NOT OUTPUT ANY TEXT OR CODE. ONLY OUTPUT THE IMAGE.

PAGE 1 LAYOUT: 1200x1697 pixels portrait. Vertical dynamic layout.
Panel 1 (Top 40%): Bright high-tech office. Remi (Silver hair, Red eyes, Red blazer) stands calmly next to a large holographic display showing "{TITLE}". Unlike usual, the screen shows a simple balanced symbol representing the concept, not complex charts. Yuto (Black hair, Gakuran) looks puzzled. Remi says "優斗君、今日は『{TITLE}』について教えるわよ。" (In a speech bubble). Title box: BLACK SLENDER box at bottom-left offset with white text "{TITLE}".
Panel 2 (Middle 30%): CONCEPTUAL ILLUSTRATION. Visual metaphor for '{TITLE}'. A clear comparison or balanced symbolic image representing the core concept of {TITLE}. Remi points to the correct/positive side. She says "{DIALOGUE_TEACH}" (In a speech bubble).
Panel 3 (Bottom-Right 15%): Yuto nodding with deep understanding. "なるほど…そういうことなんですね"
Panel 4 (Bottom-Left 15%): Remi's side profile, smiling gently (not smug).
Art style: Japanese manga style, cel shading, bright colors. Characters: Remi has Silver hair, Red eyes, Red blazer. Yuto has Black Gakuran. NO GLOVES.
```

---

## 2ページ目プロンプト

```text
【IMAGE_GENERATION_TASK】Generate high-quality manga. VISUAL CONSISTENCY IS CRITICAL.

PAGE 2 LAYOUT: 1200x1697 pixels portrait.
Panel 1 (Top 40%): VISUAL MANIFESTATION. Close up on Remi holding a small, glowing sphere of light or symbol that represents '{TITLE}'. It shines brighter than the Background elements. She looks gentle and wise. "{DIALOGUE_DESC}" (In a speech bubble).
Panel 2 (Middle 30%): CONTRAST SCENE (Metaphor). Remi stands in a split world. On her left, a chaotic storm or complex abstract shapes representing 'Confusion/Risk'. On her right, a peaceful, golden garden or orderly structure representing '{TITLE}'. She calmly points towards the peace/order.
Panel 3 (Bottom-Right 15%): Yuto visualizing his own happiness or success—simple joys and stable future, appearing in golden bubbles.
Panel 4 (Bottom-Left 15%): Yuto looking enlightened and relieved (Realization). Yuto says "{DIALOGUE_ACTION}" (In a speech bubble). Remi smiles gently, watching him grow. (No text for Remi).
Art style: Cinematic lighting, Gold/Purple theme. NO GLOVES.
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
画像生成を行ってください。以下のプロンプトに基づいて、縦長のマンガ画像を生成してください。
generate_image(
  ImageName: "remi_investment_no{NO}_p1",
  Prompt: [上記の1ページ目プロンプトのコードブロック内容をそのまま貼り付け]
)
```

```text
画像生成を行ってください。以下のプロンプトに基づいて、縦長のマンガ画像を生成してください。
generate_image(
  ImageName: "remi_investment_no{NO}_p2",
  Prompt: [上記の2ページ目プロンプトのコードブロック内容をそのまま貼り付け]
)
```

### ステップ3: 結合プレビュー作成（任意）
2枚の画像を並べて見開きプレビューを作成する場合は、画像結合スクリプト.ps1 を使用してください。

---

作成日: 2026-02-05
ステータス: フルリニューアル完了（新・足るを知る構成準拠）
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
