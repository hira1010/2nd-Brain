# No.84 Grokで銘柄探し 2P漫画生成プロンプト

## TIP情報

| 項目 | 内容 |
| :--- | :--- |
| No | 84 |
| タイトル | Grokで銘柄探し |
| 解説 | AIを活用して有望銘柄を見つける。 |
| カテゴリー | 04_未来・テクノロジー |
| ページ数 | 2 |

---

## 画像生成手順

**重要: 1ページずつ分けて生成してください。一度に両方を貼り付けると、うまく生成されません。**

### 手順1: 1ページ目の生成

以下のテキストボックスの内容をコピーして、Geminiに貼り付けてください。

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
   - Remi says: "優斗君、今日は『Grokで銘柄探し』について教えるわよ。"
   - Title box: "Grokで銘柄探し"

Panel 2 (Middle-Top 25%): VERBAL EXPLANATION. Close-up of Remi teaching.
   - Remi says: "いいわよ。しっかり聞きなさい。"

Panel 3 (Middle-Bottom 35%): VISUAL EXPLANATION (KEY PANEL).
   - Visual: Use Icons/Charts/Diagrams to visually explain "Grokで銘柄探し". Draw a conceptual illustration representing 'AIを活用して有望銘柄を見つける。'.
   - Remi points at it. She says: "イメージで捉えるとこういうことよ。"

Panel 4 (Bottom 15%): UNDERSTANDING. Yuto nodding/enlightened.
   - Yuto says: "なるほど…！ イメージできました！"

### FINAL CHECK
- Ensure 4 distinct panels.
- Ensure Japanese text is correct.
- High quality manga art.
```

### 手順2: 2ページ目の生成

1ページ目の生成が終わったら、続けて以下のテキストボックスの内容をコピーして、Geminiに貼り付けてください。

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
Panel 1 (Top 40%): EPIC METAPHOR. Remi navigating a symbolic world of 'Grokで銘柄探し'.
   - Background: Digital charts / Abstract visuals. Remi has authority.

Panel 2 (Middle 30%): STRONG SUMMARY. Visual manifestation of the concept.
   - Visual: The background vividly illustrates the concept of 'Grokで銘柄探し'. (Use symbolic imagery to represent the concept)
   - Remi says: "AIを活用して有望銘柄を見つける。 これが投資の本質よ。しっかり頭に叩き込みなさい。"

Panel 3 (Bottom-Right 15%): INTERNALIZING. Yuto visualizing his success.
   - Visual: Golden icons or happy future self.

Panel 4 (Bottom-Left 15%): DETERMINATION.
   - Yuto (Left) says: "そうか…Grokで銘柄探しの本質はここにあったんですね。"
   - Remi (Right) says: "期待しているわよ。"

### FINAL CHECK
- Ensure 4 distinct panels.
- Ensure Japanese text is correct.
- High quality manga art.
```

---

## 編集用データ (変数の参照元)

### 1ページ目

- **TITLE**: Grokで銘柄探し
- **DIALOGUE_THEME**: 「優斗君、今日は『Grokで銘柄探し』について教えるわよ。」
- **DIALOGUE_TEACH_1**: 「いい心がけね。でも、ただ知るだけじゃ意味がないわ。 つまり、AIを活用して有望銘柄を見つける。」
- **VISUAL_INSTRUCTION_1**: (ここには視覚的説明の指示を記述: Icons/Charts/Diagrams etc.)
- **DIALOGUE_ACTION_1**: 「なるほど…！ イメージできました！」

### 2ページ目

- **VISUAL_INSTRUCTION_2**: (ここには概念を象徴する視覚的描写を記述)
- **DIALOGUE_SUMMARY**: 「AIを活用して有望銘柄を見つける。 これが投資の本質よ。しっかり頭に叩き込みなさい。」
- **DIALOGUE_ACTION_2**: 「そうか…Grokで銘柄探しの本質はここにあったんですね。」

---

## 保存ファイル名

- p1: No84_Grokで銘柄探し_p1.png
- p2: No84_Grokで銘柄探し_p2.png
