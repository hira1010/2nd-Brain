
import os
import re
import random
import argparse

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

# 新しいテンプレート (No.42/V2準拠)
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
Panel 1 (Top 40%): Bright high-tech office. Remi (Silver hair, Red eyes, Red blazer) stands calmly next to a large holographic display showing "{TITLE}". Unlike usual, the screen shows a simple balanced symbol representing the concept, not complex charts. Yuto (Black hair, Gakuran) looks puzzled. Remi says "{DIALOGUE_INTRO}" (In a speech bubble). Title box: BLACK SLENDER box at bottom-left offset with white text "{TITLE}".
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
ステータス: フルリニューアル完了（スマートリファクタリング適用済み）
"""

def clean_text(text):
    if text:
        return text.strip().replace('"', "'")
    return text

def extract_variable(content, key):
    # Try filtering by variable definition style "- **KEY**: Value"
    pattern = r'- \*\*' + re.escape(key) + r'\*\*:\s*(.*)'
    match = re.search(pattern, content)
    if match:
        return clean_text(match.group(1))
    return None

def extract_info(content):
    # No抽出
    no_match = re.search(r'\|\s*No\s*\|\s*(\d+)\s*\|', content)
    no = no_match.group(1) if no_match else "00"
    
    # タイトル抽出
    title_match = re.search(r'\|\s*タイトル\s*\|\s*(.*?)[\s|]*\|', content)
    title = title_match.group(1).strip() if title_match else "Unknown"
    
    # 解説抽出
    desc_match = re.search(r'\|\s*解説\s*\|\s*(.*?)[\s|]*\|', content)
    desc = desc_match.group(1).strip() if desc_match else title
        
    return no, title, desc

def extract_dialogues(content, title, desc):
    # Extract dialogues from existing file content
    
    # 1. Intro (Theme)
    intro = extract_variable(content, "DIALOGUE_THEME")
    if not intro:
        # Fallback default
        intro = f"優斗君、今日は『{title}』について教えるわよ。"

    # 2. Teach (Teach_1)
    teach = extract_variable(content, "DIALOGUE_TEACH_1")
    if not teach:
         # Try DIALOGUE_TEACH just in case
        teach = extract_variable(content, "DIALOGUE_TEACH")
    if not teach:
        teach = "いい心がけね。でも、ただ知るだけじゃ意味がないわ。"

    # 3. Desc (Summary)
    desc_dialogue = extract_variable(content, "DIALOGUE_SUMMARY")
    if not desc_dialogue:
        desc_dialogue = extract_variable(content, "DIALOGUE_DESC")
    if not desc_dialogue:
         desc_dialogue = f"{desc} これが投資の本質よ。しっかり頭に叩き込みなさい。"

    # 4. Action (Action_2 > Action_1 > Action)
    action = extract_variable(content, "DIALOGUE_ACTION_2")
    if not action:
        action = extract_variable(content, "DIALOGUE_ACTION_1")
    if not action:
        action = extract_variable(content, "DIALOGUE_ACTION")
    if not action:
        action = f"そうか…{title}の本質はここにあったんですね。"

    return {
        "Intro": intro,
        "Teach": teach,
        "Desc": desc_dialogue,
        "Action": action
    }

def process_single_file(file_path):
    print(f"Processing: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        no, title, desc = extract_info(content)
        dialogues = extract_dialogues(content, title, desc)
        
        # Determine Category from path
        category = "未分類"
        parent_dir = os.path.basename(os.path.dirname(file_path))
        if parent_dir in TARGET_DIRS:
            category = parent_dir
        
        title_safe = re.sub(r'[\\/:*?"<>|]', '', title).replace(' ', '_')
        scene = random.choice(SCENES)
        
        new_content = TEMPLATE.format(
            NO=no,
            TITLE=title,
            DESC=desc,
            CATEGORY=category,
            TITLE_SAFE=title_safe,
            DIALOGUE_INTRO=dialogues["Intro"],
            DIALOGUE_TEACH=dialogues["Teach"],
            DIALOGUE_DESC=dialogues["Desc"],
            DIALOGUE_ACTION=dialogues["Action"],
            SCENE=scene
        )
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
            
        print(f"Successfully refactored: {file_path}")
        print(f"  - No: {no}")
        print(f"  - Title: {title}")
        print(f"  - Intro: {dialogues['Intro'][:30]}...")
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smart refactor manga prompts")
    parser.add_argument("--target", help="Specific file to process")
    parser.add_argument("--all", action="store_true", help="Process all files in target directories")
    args = parser.parse_args()
    
    if args.target:
        process_single_file(args.target)
    elif args.all:
        for subdir in TARGET_DIRS:
            dir_path = os.path.join(BASE_DIR, subdir)
            if not os.path.exists(dir_path):
                continue
            for filename in os.listdir(dir_path):
                if filename.endswith(".md"):
                    process_single_file(os.path.join(dir_path, filename))
    else:
        print("Please specify --target <file> or --all")
