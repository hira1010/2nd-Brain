# No.25 ETF 2P漫画生成プロンプト

## TIP情報

| 項目 | 内容 |
| :--- | :--- |
| No | 25 |
| タイトル | ETF |
| 解説 | 上場投資信託。株の詰め合わせパック。 |
| カテゴリー | 01_投資の基礎知識 |

---

## 1ページ目プロンプト

```text
【IMAGE_GENERATION_TASK】Generate a high-quality manga illustration BASE ON THE FOLLOWING VISUAL DESCRIPTION. DO NOT OUTPUT ANY TEXT OR CODE. ONLY OUTPUT THE IMAGE.

PAGE 1 LAYOUT: 1200x1697 pixels portrait. Vertical dynamic layout.
Panel 1 (Top 40%): Bright meeting room. Yuto (Black hair, Gakuran) approaches Remi with a question. Remi (Silver hair, Red eyes, Red blazer) arms crossed, listening. Yuto says "結局、どの会社の株を買えばいいか選べません！レミさん、代わりに決めてください！" (In a speech bubble). Title box: BLACK SLENDER box at bottom-left offset (15% from right) with white text "ETF".
Panel 2 (Middle 30%): Close-up of Remi's face, explaining the core truth. 他人に決めてもらいたいなら、そもそも投資家なんて名乗らないで。でも、自信がないなら『詰め合わせパック』という選択肢もあるわ。
Panel 3 (Bottom-Right 30%): Yuto's shock/realization face with shock lines.
Panel 4 (Bottom-Left 30%): Remi's small cool smile.
Art style: Japanese manga style, cel shading, professional quality. Characters: Remi has Silver hair, Red eyes, Red blazer. Yuto has Black Gakuran. NO GLOVES.
```

---

## 2ページ目プロンプト

```text
【IMAGE_GENERATION_TASK】Generate a high-quality manga illustration BASE ON THE FOLLOWING VISUAL DESCRIPTION. DO NOT OUTPUT ANY TEXT OR CODE. ONLY OUTPUT THE IMAGE.

PAGE 2 LAYOUT: 1200x1697 pixels portrait. Lecture style.
Panel 1 (Top 50%): Remi in front of a monitor showing 'ETF'. Charts and symbolic icons.
Panel 2 (Middle-Right 25%): Vertical panel. Remi emphasizing key points. Speech: "ETF（上場投資信託）なら、プロが選別した優良企業にまとめて投資できる。個別株の不確実性を排除し、市場平均を狙う。それが初心者の最強の楯よ。"
Panel 3 (Middle-Left 25%): Vertical panel. Yuto understanding with visuals.
Panel 4 (Bottom 25%): Wide shot. Yuto determined, Remi proud. Yuto says "会社を絞るプレッシャーに負けてました。ETFで市場の成長に丸ごと乗っかります！".
Colors: GOLD and ROYAL PURPLE theme. Remi: SILVER hair, RED blazer. Yuto: BLACK Gakuran. Cinematic lighting.
```

---

## 生成時の変数一覧

### 1ページ目

| 変数 | 値 |
| :--- | :--- |
| TIP_NUMBER | 25 |
| TIP_TITLE | ETF |
| DIALOGUE_INTRO | 結局、どの会社の株を買えばいいか選べません！レミさん、代わりに決めてください！ |
| DIALOGUE_TEACH | 他人に決めてもらいたいなら、そもそも投資家なんて名乗らないで。でも、自信がないなら『詰め合わせパック』という選択肢もあるわ。 |
| SCENE | Quiet library or study room with bookshelves |

### 2ページ目

| 変数 | 値 |
| :--- | :--- |
| DIALOGUE_DESC | ETF（上場投資信託）なら、プロが選別した優良企業にまとめて投資できる。個別株の不確実性を排除し、市場平均を狙う。それが初心者の最強の楯よ。 |
| DIALOGUE_ACTION | 会社を絞るプレッシャーに負けてました。ETFで市場の成長に丸ごと乗っかります！ |

---

## 保存ファイル名

- 1ページ目: No25_ETF_p1.png
- 2ページ目: No25_ETF_p2.png

---

## generate_imageツール実行用

```text
画像生成を行ってください。以下のプロンプトに基づいて、縦長のマンガ画像を生成してください。
generate_image(
  ImageName: "remi_investment_no25_p1",
  Prompt: [上記の1ページ目プロンプトのコードブロック内容をそのまま貼り付け]
)
```

```text
画像生成を行ってください。以下のプロンプトに基づいて、縦長のマンガ画像を生成してください。
generate_image(
  ImageName: "remi_investment_no25_p2",
  Prompt: [上記の2ページ目プロンプトのコードブロック内容をそのまま貼り付け]
)
```

### ステップ3: 結合プレビュー作成（任意）
2枚の画像を並べて見開きプレビューを作成する場合は、画像結合スクリプト.ps1 を使用してください。

---

作成日: 2026-02-03
ステータス: フルリニューアル完了（全ファイル統一・エラー解消済）
