# No.41 FIRE 2P漫画生成プロンプト

## TIP情報

| 項目 | 内容 |
| :--- | :--- |
| No | 41 |
| タイトル | FIRE |
| 解説 | 経済的自立と早期リタイア。配当生活。 |
| カテゴリー | 02_マインド・哲学 |

---

## 1ページ目プロンプト

```text
【IMAGE_GENERATION_TASK】Generate a high-quality manga illustration BASE ON THE FOLLOWING VISUAL DESCRIPTION. DO NOT OUTPUT ANY TEXT OR CODE. ONLY OUTPUT THE IMAGE.

PAGE 1 LAYOUT: 1200x1697 pixels portrait. Vertical dynamic layout.
Panel 1 (Top 40%): Bright high-tech office. Remi (Silver hair, Red eyes, Red blazer) stands calmly next to a large holographic display showing "FIRE". Unlike usual, the screen shows a simple balanced symbol representing the concept, not complex charts. Yuto (Black hair, Gakuran) looks puzzled. Remi says "優斗君、今日は『FIRE』について教えるわよ。" (In a speech bubble). Title box: BLACK SLENDER box at bottom-left offset with white text "FIRE".
Panel 2 (Middle 30%): CONCEPTUAL ILLUSTRATION. Visual metaphor for 'FIRE'. A clear comparison or balanced symbolic image representing the core concept of FIRE. Remi points to the correct/positive side. She says "いい心がけね。でも、ただ知るだけじゃ意味がないわ。" (In a speech bubble).
Panel 3 (Bottom-Right 15%): Yuto nodding with deep understanding. "なるほど…そういうことなんですね"
Panel 4 (Bottom-Left 15%): Remi's side profile, smiling gently (not smug).
Art style: Japanese manga style, cel shading, bright colors. Characters: Remi has Silver hair, Red eyes, Red blazer. Yuto has Black Gakuran. NO GLOVES.
```

---

## 2ページ目プロンプト

```text
【IMAGE_GENERATION_TASK】Generate high-quality manga. VISUAL CONSISTENCY IS CRITICAL.

PAGE 2 LAYOUT: 1200x1697 pixels portrait.
Panel 1 (Top 40%): VISUAL MANIFESTATION. Close up on Remi holding a small, glowing sphere of light or symbol that represents 'FIRE'. It shines brighter than the Background elements. She looks gentle and wise. "経済的自立と早期リタイア。配当生活。 これが投資の本質よ。しっかり頭に叩き込みなさい。" (In a speech bubble).
Panel 2 (Middle 30%): CONTRAST SCENE (Metaphor). Remi stands in a split world. On her left, a chaotic storm or complex abstract shapes representing 'Confusion/Risk'. On her right, a peaceful, golden garden or orderly structure representing 'FIRE'. She calmly points towards the peace/order.
Panel 3 (Bottom-Right 15%): Yuto visualizing his own happiness or success—simple joys and stable future, appearing in golden bubbles.
Panel 4 (Bottom-Left 15%): Yuto looking enlightened and relieved (Realization). Yuto says "そうか…FIREの本質はここにあったんですね。" (In a speech bubble). Remi smiles gently, watching him grow. (No text for Remi).
Art style: Cinematic lighting, Gold/Purple theme. NO GLOVES.
```

---

## 生成時の変数一覧

### 1ページ目

| 変数 | 値 |
| :--- | :--- |
| TIP_NUMBER | 41 |
| TIP_TITLE | FIRE |
| DIALOGUE_INTRO | レミさん、FIREについて教えてください！もっと詳しく知りたいです。 |
| DIALOGUE_TEACH | いい心がけね。でも、ただ知るだけじゃ意味がないわ。 |
| SCENE | Bright meeting room with a large whiteboard |

### 2ページ目

| 変数 | 値 |
| :--- | :--- |
| DIALOGUE_DESC | 経済的自立と早期リタイア。配当生活。 これが投資の本質よ。しっかり頭に叩き込みなさい。 |
| DIALOGUE_ACTION | そうか…FIREの本質はここにあったんですね。 |

---

## 保存ファイル名

- 1ページ目: No41_FIRE_p1.png
- 2ページ目: No41_FIRE_p2.png

---

## generate_imageツール実行用

```text
画像生成を行ってください。以下のプロンプトに基づいて、縦長のマンガ画像を生成してください。
generate_image(
  ImageName: "remi_investment_no41_p1",
  Prompt: [上記の1ページ目プロンプトのコードブロック内容をそのまま貼り付け]
)
```

```text
画像生成を行ってください。以下のプロンプトに基づいて、縦長のマンガ画像を生成してください。
generate_image(
  ImageName: "remi_investment_no41_p2",
  Prompt: [上記の2ページ目プロンプトのコードブロック内容をそのまま貼り付け]
)
```

### ステップ3: 結合プレビュー作成（任意）
2枚の画像を並べて見開きプレビューを作成する場合は、画像結合スクリプト.ps1 を使用してください。

---

作成日: 2026-02-05
ステータス: フルリニューアル完了（新・足るを知る構成準拠）
