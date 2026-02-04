# No.32 ESBI 2P漫画生成プロンプト

## TIP情報

| 項目 | 内容 |
| :--- | :--- |
| No | 32 |
| タイトル | ESBI |
| 解説 | 金持ち父さんの4つのクワドラント。 |
| カテゴリー | 02_マインド・哲学 |

---

## 1ページ目プロンプト

```text
【IMAGE_GENERATION_TASK】Generate a high-quality manga illustration BASE ON THE FOLLOWING VISUAL DESCRIPTION. DO NOT OUTPUT ANY TEXT OR CODE. ONLY OUTPUT THE IMAGE.

PAGE 1 LAYOUT: 1200x1697 pixels portrait. Vertical dynamic layout.
Panel 1 (Top 40%): Bright meeting room. Remi (Silver hair, Red eyes, Red blazer) stands confidently, pointing at a whiteboard to start a surprise lecture. Yuto (Black hair, Gakuran) looks surprised but eager. Remi says "優斗君、今日は『ESBI』について教えるわよ。しっかり聞きなさい。" (In a speech bubble). Title box: BLACK SLENDER box at bottom-left offset (15% from right) with white text "ESBI".
Panel 2 (Middle 30%): Close-up of Remi's face, explaining authoritative yet kindly. いい心がけね。でも、ただ知るだけじゃ意味がないわ。
Panel 3 (Bottom-Right 30%): Yuto looking impressed and nodding. "はい、レミさん！"
Panel 4 (Bottom-Left 30%): Remi's mysterious side profile.
Art style: Japanese manga style, cel shading, professional quality. Characters: Remi has Silver hair, Red eyes, Red blazer. Yuto has Black Gakuran. NO GLOVES.
```

---

## 2ページ目プロンプト

```text
【IMAGE_GENERATION_TASK】Generate a high-quality manga illustration BASE ON THE FOLLOWING VISUAL DESCRIPTION. DO NOT OUTPUT ANY TEXT OR CODE. ONLY OUTPUT THE IMAGE.

PAGE 2 LAYOUT: 1200x1697 pixels portrait. Lecture style.
Panel 1 (Top 50%): Remi in front of a monitor showing 'ESBI'. Charts and symbolic icons.
Panel 2 (Middle-Right 25%): Vertical panel. Remi emphasizing key points. Speech: "金持ち父さんの4つのクワドラント。 これが投資の本質よ。しっかり頭に叩き込みなさい。"
Panel 3 (Middle-Left 25%): Vertical panel. Yuto understanding with visuals.
Panel 4 (Bottom 25%): Wide shot. Yuto determined, Remi proud. Yuto says "なるほど！実践してみます！".
Colors: GOLD and ROYAL PURPLE theme. Remi: SILVER hair, RED blazer. Yuto: BLACK Gakuran. Cinematic lighting.
```

---

## 生成時の変数一覧

### 1ページ目

| 変数 | 値 |
| :--- | :--- |
| TIP_NUMBER | 32 |
| TIP_TITLE | ESBI |
| DIALOGUE_INTRO | レミさん、ESBIについて教えてください！もっと詳しく知りたいです。 |
| DIALOGUE_TEACH | いい心がけね。でも、ただ知るだけじゃ意味がないわ。 |
| SCENE | Stylish cafe with warm lighting and wooden furniture |

### 2ページ目

| 変数 | 値 |
| :--- | :--- |
| DIALOGUE_DESC | 金持ち父さんの4つのクワドラント。 これが投資の本質よ。しっかり頭に叩き込みなさい。 |
| DIALOGUE_ACTION | なるほど！実践してみます！ |

---

## 保存ファイル名

- 1ページ目: No32_ESBI_p1.png
- 2ページ目: No32_ESBI_p2.png

---

## generate_imageツール実行用

```text
画像生成を行ってください。以下のプロンプトに基づいて、縦長のマンガ画像を生成してください。
generate_image(
  ImageName: "remi_investment_no32_p1",
  Prompt: [上記の1ページ目プロンプトのコードブロック内容をそのまま貼り付け]
)
```

```text
画像生成を行ってください。以下のプロンプトに基づいて、縦長のマンガ画像を生成してください。
generate_image(
  ImageName: "remi_investment_no32_p2",
  Prompt: [上記の2ページ目プロンプトのコードブロック内容をそのまま貼り付け]
)
```

### ステップ3: 結合プレビュー作成（任意）

2枚の画像を並べて見開きプレビューを作成する場合は、画像結合スクリプト.ps1 を使用してください。

---

作成日: 2026-02-03
ステータス: フルリニューアル完了（全ファイル統一・エラー解消済）
