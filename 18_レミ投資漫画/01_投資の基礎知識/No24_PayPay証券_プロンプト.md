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
【IMAGE_GENERATION_TASK】Generate high-quality manga. VISUAL CONSISTENCY IS CRITICAL: Characters MUST wear the EXACT SAME OUTFIT in every panel. DO NOT DRAW ANY ENGLISH TEXT.

### INSTRUCTION: CRITICAL - DO NOT DRAW ANY ENGLISH TEXT. NO VARIATIONS in clothing.
### CHARACTER SETTING
- Remi: Remi: (Silky SILVER hair:1.5), (Vibrant RED eyes:1.4). OUTFIT: Always wearing a (Tailored RED blazer:1.3) with a (Black lace camisole:1.2) underneath. Identical clothes in every panel. NO GLOVES.
- Yuto: Yuto: (Short Black hair:1.3). OUTFIT: (Traditional Black GAKURAN school uniform:1.4) with gold buttons. Identical clothes in every panel. NO GLOVES.
### PAGE LAYOUT (Portrait 1200x1697)
Panel 1: Remi (in the SAME RED blazer) pointing at whiteboard, Yuto (in the SAME Black Gakuran) taking notes. Remi says "優斗君、今日は『PayPay証券』について教えるわよ。" in a Japanese speech bubble. Title box: Black box with white Japanese text "PayPay証券".
Panel 2: Remi (in the SAME RED blazer) explaining concepts. She says "言い訳を見つける天才ね。スマホ一つで1000円から世界最大の企業を買い叩ける時代に、何を言っているの？" in a Japanese speech bubble.
Panel 3: Yuto (in the SAME Black Gakuran) nodding. "はい、レミさん！" in a bubble.
Panel 4: Remi (in the SAME RED blazer)'s side profile.
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
Panel 1: EPIC METAPHOR SCENE. Remi (in the SAME RED blazer) navigating a symbolic world of 'PayPay証券'. Digital charts in background. Remi has absolute authority.
Panel 2: Remi (in the SAME RED blazer) making a sharp gesture. She says "PayPay証券や少額投資を使えば、お菓子を我慢する金でAppleやAmazonのオーナーになれる。少額だからと侮る者が、大きな富を掴むことはないわ。" in a Japanese speech bubble.
Panel 3: Yuto (in the SAME Black Gakuran) visualizing profit with golden icons.
Panel 4: Yuto (in the SAME Black Gakuran) determined, Remi (in the SAME RED blazer) proud. Yuto says "1000円でもAppleの株主に…！言い訳を探す前に、まずは1株買ってみます！" in a bubble. Remi thinks "期待しているわよ。" in a small thoughts bubble.
### STYLE: Cinematic lighting, Gold/Purple theme. NO GLOVES.
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
