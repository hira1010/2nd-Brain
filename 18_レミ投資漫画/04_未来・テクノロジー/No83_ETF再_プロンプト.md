# No.83 ETF再 2P漫画生成プロンプト

## TIP情報

| 項目 | 内容 |
| :--- | :--- |
| No | 83 |
| タイトル | ETF再 |
| 解説 | 個別株より低リスク。初心者の最適解。 |
| カテゴリー | 04_未来・テクノロジー |

---

## 1ページ目プロンプト

```text
【IMAGE_GENERATION_TASK】Generate a high-quality manga illustration BASE ON THE FOLLOWING VISUAL DESCRIPTION. DO NOT OUTPUT ANY TEXT OR CODE. ONLY OUTPUT THE IMAGE.

PAGE 1 LAYOUT: 1200x1697 pixels portrait. Vertical dynamic layout.
Panel 1 (Top 40%): Bright meeting room. Yuto (Black hair, Gakuran) approaches Remi with a question. Remi (Silver hair, Red eyes, Red blazer) arms crossed, listening. Yuto says "レミさん、ETF再について教えてください！もっと詳しく知りたいです。" (In a speech bubble). Title box: BLACK SLENDER box at bottom-left offset (15% from right) with white text "ETF再".
Panel 2 (Middle 30%): Close-up of Remi's face, explaining the core truth. いい心がけね。でも、ただ知るだけじゃ意味がないわ。
Panel 3 (Bottom-Right 30%): Yuto's shock/realization face with shock lines.
Panel 4 (Bottom-Left 30%): Remi's small cool smile.
Art style: Japanese manga style, cel shading, professional quality. Characters: Remi has Silver hair, Red eyes, Red blazer. Yuto has Black Gakuran. NO GLOVES.
```

---

## 2ページ目プロンプト

```text
【IMAGE_GENERATION_TASK】Generate a high-quality manga illustration BASE ON THE FOLLOWING VISUAL DESCRIPTION. DO NOT OUTPUT ANY TEXT OR CODE. ONLY OUTPUT THE IMAGE.

PAGE 2 LAYOUT: 1200x1697 pixels portrait. Lecture style.
Panel 1 (Top 50%): Remi in front of a monitor showing 'ETF再'. Charts and symbolic icons.
Panel 2 (Middle-Right 25%): Vertical panel. Remi emphasizing key points. Speech: "個別株より低リスク。初心者の最適解。 これが投資の本質よ。しっかり頭に叩き込みなさい。"
Panel 3 (Middle-Left 25%): Vertical panel. Yuto understanding with visuals.
Panel 4 (Bottom 25%): Wide shot. Yuto determined, Remi proud. Yuto says "なるほど！実践してみます！".
Colors: GOLD and ROYAL PURPLE theme. Remi: SILVER hair, RED blazer. Yuto: BLACK Gakuran. Cinematic lighting.
```

---

## 生成時の変数一覧

### 1ページ目

| 変数 | 値 |
| :--- | :--- |
| TIP_NUMBER | 83 |
| TIP_TITLE | ETF再 |
| DIALOGUE_INTRO | レミさん、ETF再について教えてください！もっと詳しく知りたいです。 |
| DIALOGUE_TEACH | いい心がけね。でも、ただ知るだけじゃ意味がないわ。 |
| SCENE | Stylish cafe with warm lighting and wooden furniture |

### 2ページ目

| 変数 | 値 |
| :--- | :--- |
| DIALOGUE_DESC | 個別株より低リスク。初心者の最適解。 これが投資の本質よ。しっかり頭に叩き込みなさい。 |
| DIALOGUE_ACTION | なるほど！実践してみます！ |

---

## 保存ファイル名

- 1ページ目: No83_ETF再_p1.png
- 2ページ目: No83_ETF再_p2.png

---

## generate_imageツール実行用

```text
画像生成を行ってください。以下のプロンプトに基づいて、縦長のマンガ画像を生成してください。
generate_image(
  ImageName: "remi_investment_no83_p1",
  Prompt: [上記の1ページ目プロンプトのコードブロック内容をそのまま貼り付け]
)
```

```text
画像生成を行ってください。以下のプロンプトに基づいて、縦長のマンガ画像を生成してください。
generate_image(
  ImageName: "remi_investment_no83_p2",
  Prompt: [上記の2ページ目プロンプトのコードブロック内容をそのまま貼り付け]
)
```

### ステップ3: 結合プレビュー作成（任意）
2枚の画像を並べて見開きプレビューを作成する場合は、画像結合スクリプト.ps1 を使用してください。

---

作成日: 2026-02-03
ステータス: フルリニューアル完了（全ファイル統一・エラー解消済）
