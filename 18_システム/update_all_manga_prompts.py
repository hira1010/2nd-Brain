#!/usr/bin/env python3
"""全漫画プロンプト修正 - 会話フロー改善版"""

import re
from pathlib import Path

BASE_DIR = Path(r"c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画")

CHARACTER_SETTINGS = """## キャラクター設定（全ページ共通）

### レミ（Remi）- 厳格に固定
- **髪**: 腰まで届く非常に長いストレートなシルバーヘア、前髪はセンター分け
- **目**: 鋭い赤い瞳（ruby red eyes）、長いまつ毛
- **服装**: 深紅のビジネスブレザー（赤いボタン）、白いシャツ、**手袋なし**
- **体型**: スリムで背が高い大人の女性、エレガントな立ち姿
- **表情**: 知的で自信に満ちた微笑み、冷静

### 優斗（Yuto）- 厳格に固定
- **髪**: 短い黒髪、整った髪型
- **目**: 黒い瞳、純粋な表情
- **服装**: 伝統的な黒い学ラン（gakuran）、立襟、**手袋なし**
- **体型**: 標準的な男子高校生の体型
- **表情**: 好奇心旺盛、真剣に学ぶ姿勢

---

"""

def extract_info(content: str) -> dict:
    """TIP情報とセリフを抽出"""
    info = {}
    
    info['no'] = re.search(r'\| No \| (\d+)', content).group(1) if re.search(r'\| No \| (\d+)', content) else ''
    info['title'] = re.search(r'\| タイトル \| ([^\|]+)', content).group(1).strip() if re.search(r'\| タイトル \| ([^\|]+)', content) else ''
    info['description'] = re.search(r'\| 解説 \| ([^\|]+)', content).group(1).strip() if re.search(r'\| 解説 \| ([^\|]+)', content) else ''
    info['category'] = re.search(r'\| カテゴリー \| ([^\|]+)', content).group(1).strip() if re.search(r'\| カテゴリー \| ([^\|]+)', content) else ''
    
    # セリフ抽出
    intro = re.search(r'DIALOGUE_INTRO.*?\| ([^\|]+)', content)
    info['dialogue_intro'] = intro.group(1).strip() if intro else f"「優斗君、今日は『{info['title']}』について教えるわよ。」"
    
    teach = re.search(r'DIALOGUE_TEACH.*?\| ([^\|]+)', content)
    info['dialogue_teach'] = teach.group(1).strip() if teach else f"「いい心がけね。でも、ただ知るだけじゃ意味がないわ。つまり、{info.get('description', '')}」"
    
    desc = re.search(r'DIALOGUE_DESC.*?\| ([^\|]+)', content)
    info['dialogue_desc'] = desc.group(1).strip() if desc else f"「{info.get('description', '')} これが投資の本質よ。しっかり頭に叩き込みなさい。」"
    
    action = re.search(r'DIALOGUE_ACTION.*?\| ([^\|]+)', content)
    info['dialogue_action'] = action.group(1).strip() if action else f"「そうか…{info['title']}の本質はここにあったんですね。」"
    
    return info


def create_prompt(info):
    """改善プロンプト生成（会話フロー修正版）"""
    no, title, desc, cat = info['no'], info['title'], info['description'], info['category']
    d_intro, d_teach, d_desc, d_action = info['dialogue_intro'], info['dialogue_teach'], info['dialogue_desc'], info['dialogue_action']
    
    return f"""# No.{no} {title} 2P漫画生成プロンプト

## TIP情報

| 項目 | 内容 |
| :--- | :--- |
| No | {no} |
| タイトル | {title} |
| 解説 | {desc} |
| カテゴリー | {cat} |

---

{CHARACTER_SETTINGS}

## 1ページ目プロンプト

```text
Create a SINGLE-PAGE vertical Japanese manga illustration. CRITICAL: Output must be PORTRAIT orientation, TALL format (width 1280 pixels × height 1810 pixels). This is ONE page only, not multiple pages combined.

**MANDATORY CHARACTER CONSISTENCY:**

Remi: Adult woman with waist-length straight silver hair with center-parted bangs, sharp ruby-red eyes with long eyelashes, wearing deep crimson business blazer with red buttons over white shirt, NO gloves, tall slim elegant figure, confident intelligent smile.

Yuto: Male high school student with short neat black hair, black eyes, wearing traditional black gakuran uniform with stand-up collar, NO gloves, standard teenage boy build, curious earnest expression.

**PAGE 1 VERTICAL LAYOUT (1280w × 1810h portrait):**

Top 40%: Modern office. Remi stands beside holographic display showing "{title}" in Japanese. Yuto looks curious. Speech bubble (Remi): {d_intro} Title card: Black box "{title}" bottom-left.

Middle 30%: DIALOGUE FLOW. Yuto responds eagerly: "はい！もっと詳しく知りたいです！" Then Remi explains with SYMBOLIC METAPHOR visual - LEFT: chaos/confusion labeled "混乱" in cold dark tones. RIGHT: order/wisdom labeled "{title}" in golden warm tones. Remi points to golden side. Speech bubble (Remi): {d_teach}

Bottom 30%: Panel 3 right - Yuto nodding with understanding "なるほど…そういうことなんですね". Panel 4 left - Remi's profile, gentle smile.

**FORMAT:** PORTRAIT VERTICAL 1280×1810. Page 1 of 2 ONLY. Professional manga style, cel shading, vibrant colors. Characters MUST match descriptions exactly.
```

---

## 2ページ目プロンプト

```text
Create a SINGLE-PAGE vertical Japanese manga, CONTINUING from page 1 with IDENTICAL characters. CRITICAL: PORTRAIT orientation 1280×1810 pixels. Page 2 of 2.

**MANDATORY - SAME AS PAGE 1:**

Remi: Waist-length straight silver hair, center-parted bangs, ruby-red eyes, deep crimson blazer over white shirt, NO gloves, tall elegant figure.

Yuto: Short black hair, black eyes, black gakuran uniform, stand-up collar, NO gloves, teenage build.

**PAGE 2 VERTICAL LAYOUT (1280w × 1810h portrait):**

Top 40%: Close-up of Remi holding glowing golden sphere (symbolizing '{title}'), face illuminated, wise expression. Speech bubble (Remi): {d_desc}

Middle 30%: Remi in split-world. LEFT: dark storm/chaos (purple/red). RIGHT: golden garden/peace (representing '{title}'). She points to golden side decisively.

Bottom 30%: Panel 3 right - Yuto with golden bubbles showing happy future. Panel 4 left - Yuto enlightened. Speech bubble: {d_action} Remi watching warmly (no speech).

**FORMAT:** PORTRAIT VERTICAL 1280×1810. Page 2 ONLY. Characters IDENTICAL to page 1. Cinematic lighting, gold/purple theme.
```

---

## 重要な生成手順

### ステップ1: 1ページ目を生成

```
generate_image(
  ImageName: "remi_no{no}_page1",
  Prompt: [上記1ページ目プロンプトを完全にコピペ]
)
```

### ステップ2: 2ページ目を生成（1ページ目確認後）

```
generate_image(
  ImageName: "remi_no{no}_page2",
  Prompt: [上記2ページ目プロンプトを完全にコピペ]
)
```

---

作成日: 2026-02-05
ステータス: A4縦・複数ページ・キャラ一貫性・会話フロー対応完了
"""


def main():
    print("="*70)
    print("全漫画プロンプト修正（会話フロー改善版）")
    print("="*70 + "\n")
    
    files = sorted(BASE_DIR.rglob("*プロンプト.md"))
    print(f"対象: {len(files)}ファイル\n")
    
    ok = 0
    for f in files:
        try:
            content = f.read_text(encoding='utf-8')
            info = extract_info(content)
            
            if not info['no'] or not info['title']:
                print(f"⚠ {f.name} (情報不足)")
                continue
            
            new = create_prompt(info)
            f.write_text(new, encoding='utf-8', newline='\n')
            print(f"✓ {f.name}")
            ok += 1
        except Exception as e:
            print(f"✗ {f.name}: {e}")
    
    print(f"\n{'='*70}\n完了: {ok}/{len(files)} ファイル\n{'='*70}")

if __name__ == "__main__":
    main()
