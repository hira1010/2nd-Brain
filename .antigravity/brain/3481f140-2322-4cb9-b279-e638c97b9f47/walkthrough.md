# Walkthrough - 「クリット」誤字の修正

画像内に発生していた「クリット」という誤字を、投資文脈で適切な「メリット」に修正したプロンプトを作成しました。

## 修正内容

### 1. タイポの原因特定

- **「クリット」**: 投資用語としては存在せず、AI（DALL-E 3等）による生成時の誤字であると判断しました。
- **推測される意図**: 状況から「メリットなか？（メリットはあるか？）」という初心者の迷いを描こうとしたものと推測。

### 2. プロンプトの修正

- 「クリットなか？」を **「メリットなか？」** に修正。
- 画像の3パネル構成（チャートの乱高下 → 囁く影 → 動悸・パニック）を正確にプロンプト化。

## 修正済みプロンプト (Final)

```javascript
generate_image(
  ImageName: "yuto_panic_chart_fixed_v15_5",
  Prompt: "ARCHITECTURE: [v15.5 EDGE OBLITERATOR] FULL BLEED. ZERO PIXEL MARGINS. 110% OVERFILL. **VERTICAL PORTRAIT ORIENTATION. 12:17 RATIO.**

CHARACTERS:
- Yuto: ((Navy Blue Suit:1.3)), ((White Shirt)), ((Blue Tie:1.3)), ((Short Black hair)). (Face pale, sweating, eyes wide with horror, looking at smartphone). **VISUAL LOCK**.

[COMPOSITION - 3 PANELS]:

- [PANEL 1 - 40% height]: FULL WIDTH FILL. Yuto staring at his phone. In the background, a chaotic stock chart (green and red candles) is bouncing up and down violently.
  Yuto Speech Bubbles: '上がった?!', 'いや, また下がった……!', 'うわああ, どうすればいいんだ!?'

- [PANEL 2 - 35% height]: FULL WIDTH FILL. Close-up of Yuto holding his head in agony. Small, dark, fuzzy monster-like 'Noise' (Shadows) are floating around him, whispering to his ears.
  Shadows Speech Bubbles (Whispering): '売りか？', '買いか？', 'チャンスだ!', 'メリットなか？'

- [PANEL 3 - 25% height]: FULL WIDTH FILL. Extreme close-up of Yuto's chest, his hand clutching his heart in pain. Dramatic speed lines radiating from his heart. 
  Japanese Onomatopoeia: 'ドッ'

STYLE: [PREMIUM DIGITAL MANGA]. High-end 2D Anime, Crisp linework, Vibrant colors, Dynamic cinematic lighting, Sharp Cel Shading.
**FONT: Traditional Japanese Manga Font (Antic Gothic / アンチック体)**.
**NEGATIVE PROMPT**: metadata at top, gibberish text, hallucinated letters, 'クリット', brown hair, blue eyes, generic face.
"
)
```

## 検証

- ワークスペース内を全検索しましたが、元のファイルが特定できなかったため、今回のプロンプト案を「正」として提示。
- ユーザーより「LGTM」の承認をいただきました。
