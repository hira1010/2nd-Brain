# No.24 PayPay証券 2P漫画生成プロンプト

## TIP情報

| 項目 | 内容 |
| :--- | :--- |
| No | 24 |
| タイトル | PayPay証券 |
| 解説 | 1000円から少額で米国株が買える。 |
| カテゴリー | 01_投資の基礎知識 |

---

## 1ページ目プロンプト

```text
【IMAGE_GENERATION_TASK】Generate a high-quality manga illustration BASE ON THE FOLLOWING VISUAL DESCRIPTION. DO NOT OUTPUT ANY TEXT OR CODE. ONLY OUTPUT THE IMAGE.

PAGE 1 LAYOUT: 1200x1697 pixels portrait. Vertical dynamic layout.
Panel 1 (Top 40%): Bright meeting room. Remi (Silver hair, Red eyes, Red blazer) stands confidently, pointing at a whiteboard to start a surprise lecture. Yuto (Black hair, Gakuran) looks surprised but eager. Remi says "優斗君、今日は『PayPay証券』について教えるわよ。しっかり聞きなさい。" (In a speech bubble). Title box: BLACK SLENDER box at bottom-left offset (15% from right) with white text "PayPay証券".
Panel 2 (Middle 30%): Close-up of Remi's face, explaining authoritative yet kindly. 言い訳を見つける天才ね。スマホ一つで1000円から世界最大の企業を買い叩ける時代に、何を言っているの？
Panel 3 (Bottom-Right 30%): Yuto looking impressed and nodding. "はい、レミさん！"
Panel 4 (Bottom-Left 30%): Remi's mysterious side profile.
Art style: Japanese manga style, cel shading, professional quality. Characters: Remi has Silver hair, Red eyes, Red blazer. Yuto has Black Gakuran. NO GLOVES.
```

---

## 2ページ目プロンプト

```text
【IMAGE_GENERATION_TASK】Generate a high-quality manga illustration BASE ON THE FOLLOWING VISUAL DESCRIPTION. DO NOT OUTPUT ANY TEXT OR CODE. ONLY OUTPUT THE IMAGE.

PAGE 2 LAYOUT: 1200x1697 pixels portrait. Lecture style.
Panel 1 (Top 50%): Remi in front of a monitor showing 'PayPay証券'. Charts and symbolic icons.
Panel 2 (Middle-Right 25%): Vertical panel. Remi emphasizing key points. Speech: "PayPay証券や少額投資を使えば、お菓子を我慢する金でAppleやAmazonのオーナーになれる。少額だからと侮る者が、大きな富を掴むことはないわ。"
Panel 3 (Middle-Left 25%): Vertical panel. Yuto understanding with visuals.
Panel 4 (Bottom 25%): Wide shot. Yuto determined, Remi proud. Yuto says "1000円でもAppleの株主に…！言い訳を探す前に、まずは1株買ってみます！".
Colors: GOLD and ROYAL PURPLE theme. Remi: SILVER hair, RED blazer. Yuto: BLACK Gakuran. Cinematic lighting.
```

---

## 生成時の変数一覧

### 1ページ目

| 変数 | 値 |
| :--- | :--- |
| TIP_NUMBER | 24 |
| TIP_TITLE | PayPay証券 |
| DIALOGUE_INTRO | 米国株は1株数万円もするから、僕の給料じゃ買えませんよ…富豪の特権ですよね。 |
| DIALOGUE_TEACH | 言い訳を見つける天才ね。スマホ一つで1000円から世界最大の企業を買い叩ける時代に、何を言っているの？ |
| SCENE | Luxurious lounge bar with night city view |

### 2ページ目

| 変数 | 値 |
| :--- | :--- |
| DIALOGUE_DESC | PayPay証券や少額投資を使えば、お菓子を我慢する金でAppleやAmazonのオーナーになれる。少額だからと侮る者が、大きな富を掴むことはないわ。 |
| DIALOGUE_ACTION | 1000円でもAppleの株主に…！言い訳を探す前に、まずは1株買ってみます！ |

---

## 保存ファイル名

- 1ページ目: No24_PayPay証券_p1.png
- 2ページ目: No24_PayPay証券_p2.png

---

## generate_imageツール実行用

```text
画像生成を行ってください。以下のプロンプトに基づいて、縦長のマンガ画像を生成してください。
generate_image(
  ImageName: "remi_investment_no24_p1",
  Prompt: [上記の1ページ目プロンプトのコードブロック内容をそのまま貼り付け]
)
```

```text
画像生成を行ってください。以下のプロンプトに基づいて、縦長のマンガ画像を生成してください。
generate_image(
  ImageName: "remi_investment_no24_p2",
  Prompt: [上記の2ページ目プロンプトのコードブロック内容をそのまま貼り付け]
)
```

### ステップ3: 結合プレビュー作成（任意）
2枚の画像を並べて見開きプレビューを作成する場合は、画像結合スクリプト.ps1 を使用してください。

---

作成日: 2026-02-03
ステータス: フルリニューアル完了（全ファイル統一・エラー解消済）
