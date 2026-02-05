# No.28 インカムvsキャピタル 2P漫画生成プロンプト

## TIP情報

| 項目 | 内容 |
| :--- | :--- |
| No | 28 |
| タイトル | インカムvsキャピタル |
| 解説 | 配当狙いか値上がり狙いか。 |
| カテゴリー | 02_マインド・哲学 |
| ページ数 | 2 |

---

## 画像生成用プロンプト (コピペ用)

以下のテキストをすべてコピーして、Geminiに貼り付けてください。

### 1ページ目

```text
画像生成をお願いします。
以下の要件に基づいて、日本の漫画スタイルの画像を1枚生成してください。
コードの解説やテキストの出力は不要です。画像のみを出力してください。
縦長(Portrait)の4コマ漫画形式です。

【要件】
**Output Format**: A single 4-panel MANGA page (Portrait Aspect Ratio).
**Style**: Japanese Anime/Manga style, colored, cel-shaded.
**Language**: Text in speech bubbles must be JAPANESE.

【Prompt】
Create a 4-panel MANGA page (Portrait 1200x1697).
PAGE FLOW: Theme -> Explain -> Visual -> Understand.

### CHARACTER SETTING
- Remi (Woman): Silver hair, Red eyes, Sharp eyes. Wearing RED blazer over black lace top. Cool, intelligent. NO GLOVES.
- Yuto (Boy): Short Black hair, Black GAKURAN school uniform, Gold buttons. Young learner. NO GLOVES.

### LAYOUT & CONTENT
Panel 1 (Top 25%): THEME INTRO. Bright office. Remi (in RED blazer) speaks to Yuto.
   - Remi says: "優斗君、今日は『インカムvsキャピタル』について教えるわよ。"
   - Title box: "インカムvsキャピタル"

Panel 2 (Middle-Top 25%): VERBAL EXPLANATION. Close-up of Remi teaching.
   - Remi says: "インカムは保有で得る『配当金』。キャピタルは売却で得る『値上がり益』よ。"

Panel 3 (Middle-Bottom 35%): VISUAL EXPLANATION (KEY PANEL).
   - Visual: Split screen. Left side shows "Income" (Wallet receiving coins regularly from a tree). Right side shows "Capital" (A chart arrow going up, showing profit from selling).
   - Remi points at it. She says: "イメージで捉えるとこういうことよ。"

Panel 4 (Bottom 15%): UNDERSTANDING. Yuto nodding/enlightened.
   - Yuto says: "なるほど！ 定期収入か、売却益か、全然違うんですね！"

### FINAL CHECK
- Ensure 4 distinct panels.
- Ensure Japanese text is correct.
- High quality manga art.
```

### 2ページ目

```text
画像生成をお願いします。
以下の要件に基づいて、日本の漫画スタイルの画像を1枚生成してください。
コードの解説やテキストの出力は不要です。画像のみを出力してください。
縦長(Portrait)の4コマ漫画形式です。

【要件】
**Output Format**: A single 4-panel MANGA page (Portrait Aspect Ratio).
**Style**: Japanese Anime/Manga style, colored, cel-shaded, cinematic lighting.
**Language**: Text in speech bubbles must be JAPANESE.

【Prompt】
Create a 4-panel MANGA page (Portrait 1200x1697).
PAGE FLOW: Metaphor -> Summary -> Internalize -> Future.

### CHARACTER SETTING
- Remi (Woman): Silver hair, Red eyes. RED blazer. NO GLOVES.
- Yuto (Boy): Black hair, Black GAKURAN. NO GLOVES.

### LAYOUT & CONTENT
Panel 1 (Top 40%): EPIC METAPHOR. Remi navigating a symbolic world of 'Income vs Capital'.
   - Background: Split background. Left: Peaceful Orchard with slowly growing trees (Income style). Right: Intense Hunting Ground or Trading Floor (Capital style).

Panel 2 (Middle 30%): STRONG SUMMARY. Visual manifestation of the concept.
   - Visual: Remi stands between the two worlds. Left side represents "Slow & Steady", Right side represents "High Risk & Reward".
   - Remi says: "農耕のように育てるか、狩りのように狙うか。これが投資の二つの顔よ。"

Panel 3 (Bottom-Right 15%): INTERNALIZING. Yuto visualizing his success.
   - Visual: Golden icons representing both wealth styles.

Panel 4 (Bottom-Left 15%): DETERMINATION. Yuto determined, Remi proud.
   - Yuto says: "自分の性格にはどっちが合うか、よく考えてみます！"
   - Remi thinks: "期待しているわよ。"

### FINAL CHECK
- Ensure 4 distinct panels.
- Ensure Japanese text is correct.
- High quality manga art.
```

---

## 編集用データ (変数の参照元)

### 1ページ目

- **TITLE**: インカムvsキャピタル
- **DIALOGUE_THEME**: 「優斗君、今日は『インカムvsキャピタル』について教えるわよ。」
- **DIALOGUE_TEACH_1**: 「インカムは保有で得る『配当金』。キャピタルは売却で得る『値上がり益』よ。」
- **VISUAL_INSTRUCTION_1**: Split screen. Left side shows "Income" (Wallet receiving coins regularly from a tree). Right side shows "Capital" (A chart arrow going up, showing profit from selling).
- **DIALOGUE_ACTION_1**: 「なるほど！ 定期収入か、売却益か、全然違うんですね！」

### 2ページ目

- **VISUAL_INSTRUCTION_2**: Split background. Left: Peaceful Orchard with slowly growing trees (Income style). Right: Intense Hunting Ground or Trading Floor (Capital style).
- **DIALOGUE_SUMMARY**: 「農耕のように育てるか、狩りのように狙うか。これが投資の二つの顔よ。」
- **DIALOGUE_ACTION_2**: 「自分の性格にはどっちが合うか、よく考えてみます！」

---

## 保存ファイル名

- p1: No28_インカムvsキャピタル_p1.png
- p2: No28_インカムvsキャピタル_p2.png
