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
【IMAGE_GENERATION_TASK】Generate high-quality manga. VISUAL CONSISTENCY IS CRITICAL: Characters MUST wear the EXACT SAME OUTFIT in every panel. DO NOT DRAW ANY ENGLISH TEXT.

### INSTRUCTION: CRITICAL - DO NOT DRAW ANY ENGLISH TEXT. NO VARIATIONS in clothing.
### CHARACTER SETTING
- Remi: Remi: (Silky SILVER hair:1.5), (Vibrant RED eyes:1.4). OUTFIT: Always wearing a (Tailored RED blazer:1.3) with a (Black lace camisole:1.2) underneath. Identical clothes in every panel. NO GLOVES.
- Yuto: Yuto: (Short Black hair:1.3). OUTFIT: (Traditional Black GAKURAN school uniform:1.4) with gold buttons. Identical clothes in every panel. NO GLOVES.
### PAGE LAYOUT (Portrait 1200x1697)
Panel 1: Yuto (in the SAME Black Gakuran) and Remi (in the SAME RED blazer) in a meeting room. Yuto says "結局、どの会社の株を買えばいいか選べません！レミさん、代わりに決めてください！" in a Japanese speech bubble. Title box: Black slender box with white Japanese text "ETF".
Panel 2: Extreme Close-up of Remi (in the SAME RED blazer)'s red eyes. She says "他人に決めてもらいたいなら、そもそも投資家なんて名乗らないで。でも、自信がないなら『詰め合わせパック』という選択肢もあるわ。" in a Japanese speech bubble.
Panel 3: Yuto (in the SAME Black Gakuran) with manga shock lines.
Panel 4: Remi (in the SAME RED blazer) smiling coolly.
### STYLE: Japanese manga, cel shaded. NO GLOVES.
```

---

## 2ページ目プロンプト

```text
【IMAGE_GENERATION_TASK】Generate high-quality manga. VISUAL CONSISTENCY IS CRITICAL: Characters MUST wear the EXACT SAME OUTFIT in every panel. DO NOT DRAW ANY ENGLISH TEXT.

### INSTRUCTION: CRITICAL - DO NOT DRAW ANY ENGLISH TEXT. NO VARIATIONS in clothing.
### CHARACTER SETTING
- Remi: Remi: (Silky SILVER hair:1.5), (Vibrant RED eyes:1.4). OUTFIT: Always wearing a (Tailored RED blazer:1.3) with a (Black lace camisole:1.2) underneath. Identical clothes in every panel. NO GLOVES.
- Yuto: Yuto: (Short Black hair:1.3). OUTFIT: (Traditional Black GAKURAN school uniform:1.4) with gold buttons. Identical clothes in every panel. NO GLOVES.
### PAGE LAYOUT (Portrait 1200x1697)
Panel 1: EPIC METAPHOR SCENE. Remi (in the SAME RED blazer) navigating a symbolic world of 'ETF'. Digital charts in background. Remi has absolute authority.
Panel 2: Remi (in the SAME RED blazer) making a sharp gesture. She says "ETF（上場投資信託）なら、プロが選別した優良企業にまとめて投資できる。個別株の不確実性を排除し、市場平均を狙う。それが初心者の最強の楯よ。" in a Japanese speech bubble.
Panel 3: Yuto (in the SAME Black Gakuran) visualizing profit with golden icons.
Panel 4: Yuto (in the SAME Black Gakuran) determined, Remi (in the SAME RED blazer) proud. Yuto says "会社を絞るプレッシャーに負けてました。ETFで市場の成長に丸ごと乗っかります！" in a bubble. Remi thinks "期待しているわよ。" in a small thoughts bubble.
### STYLE: Cinematic lighting, Gold/Purple theme. NO GLOVES.
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
