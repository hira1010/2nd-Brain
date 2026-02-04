# No.18 NISA枠 2P漫画生成プロンプト

## TIP情報

| 項目 | 内容 |
| :--- | :--- |
| No | 18 |
| タイトル | NISA枠 |
| 解説 | 年間360万円の非課税枠を活用する。 |
| カテゴリー | 01_投資の基礎知識 |

---

## 1ページ目プロンプト

```text
【IMAGE_GENERATION_TASK】Generate a high-quality manga illustration BASE ON THE FOLLOWING VISUAL DESCRIPTION. DO NOT OUTPUT ANY TEXT OR CODE. ONLY OUTPUT THE IMAGE.

PAGE 1 LAYOUT: 1200x1697 pixels portrait. Vertical dynamic layout.
Panel 1 (Top 40%): Bright meeting room. Remi (Silver hair, Red eyes, Red blazer) stands confidently, pointing at a whiteboard to start a surprise lecture. Yuto (Black hair, Gakuran) looks surprised but eager. Remi says "優斗君、今日は『NISA枠』について教えるわよ。しっかり聞きなさい。" (In a speech bubble). Title box: BLACK SLENDER box at bottom-left offset (15% from right) with white text "NISA枠".
Panel 2 (Middle 30%): Close-up of Remi's face, explaining authoritative yet kindly. 国が『非課税でお宝をあげる』って言ってるのに、それを無視するなんて。正気とは思えないわ。
Panel 3 (Bottom-Right 30%): Yuto looking impressed and nodding. "はい、レミさん！"
Panel 4 (Bottom-Left 30%): Remi's mysterious side profile.
Art style: Japanese manga style, cel shading, professional quality. Characters: Remi has Silver hair, Red eyes, Red blazer. Yuto has Black Gakuran. NO GLOVES.
```

---

## 2ページ目プロンプト

```text
【IMAGE_GENERATION_TASK】Generate a high-quality manga illustration BASE ON THE FOLLOWING VISUAL DESCRIPTION. DO NOT OUTPUT ANY TEXT OR CODE. ONLY OUTPUT THE IMAGE.

PAGE 2 LAYOUT: 1200x1697 pixels portrait. Lecture style.
Panel 1 (Top 50%): Remi in front of a monitor showing 'NISA枠'. Charts and symbolic icons.
Panel 2 (Middle-Right 25%): Vertical panel. Remi emphasizing key points. Speech: "本来20%取られる税金がゼロになる。年間360万円の枠は、庶民が資産形成するための最強の権利よ。面倒と言う間に、複利チャンスを逃しているのよ。"
Panel 3 (Middle-Left 25%): Vertical panel. Yuto understanding with visuals.
Panel 4 (Bottom 25%): Wide shot. Yuto determined, Remi proud. Yuto says "手続きをサボっている間に損をしていたのか…明日、証券口座の開設申し込みます！".
Colors: GOLD and ROYAL PURPLE theme. Remi: SILVER hair, RED blazer. Yuto: BLACK Gakuran. Cinematic lighting.
```

---

## 生成時の変数一覧

### 1ページ目

| 変数 | 値 |
| :--- | :--- |
| TIP_NUMBER | 18 |
| TIP_TITLE | NISA枠 |
| DIALOGUE_INTRO | NISAって最近よく聞きますけど、手続きが面倒そうだし後回しでいいですよね？ |
| DIALOGUE_TEACH | 国が『非課税でお宝をあげる』って言ってるのに、それを無視するなんて。正気とは思えないわ。 |
| SCENE | Stylish cafe with warm lighting and wooden furniture |

### 2ページ目

| 変数 | 値 |
| :--- | :--- |
| DIALOGUE_DESC | 本来20%取られる税金がゼロになる。年間360万円の枠は、庶民が資産形成するための最強の権利よ。面倒と言う間に、複利チャンスを逃しているのよ。 |
| DIALOGUE_ACTION | 手続きをサボっている間に損をしていたのか…明日、証券口座の開設申し込みます！ |

---

## 保存ファイル名

- 1ページ目: No18_NISA枠_p1.png
- 2ページ目: No18_NISA枠_p2.png

---

## generate_imageツール実行用

```text
画像生成を行ってください。以下のプロンプトに基づいて、縦長のマンガ画像を生成してください。
generate_image(
  ImageName: "remi_investment_no18_p1",
  Prompt: [上記の1ページ目プロンプトのコードブロック内容をそのまま貼り付け]
)
```

```text
画像生成を行ってください。以下のプロンプトに基づいて、縦長のマンガ画像を生成してください。
generate_image(
  ImageName: "remi_investment_no18_p2",
  Prompt: [上記の2ページ目プロンプトのコードブロック内容をそのまま貼り付け]
)
```

### ステップ3: 結合プレビュー作成（任意）
2枚の画像を並べて見開きプレビューを作成する場合は、画像結合スクリプト.ps1 を使用してください。

---

作成日: 2026-02-03
ステータス: フルリニューアル完了（全ファイル統一・エラー解消済）
