# プロンプト修正計画

「クリット」という誤字を含む漫画生成プロンプトの修正案を提示します。

## 変更内容

- 画像内の「クリットなか？」を、状況から推測される本来の文言「メリットなか？」または「メリットか？」に修正したプロンプトを作成します。
- 画像の3枚構成（チャートの乱高下、囁く影、動悸）を忠実に再現するプロンプトを構築します。

## 修正後のプロンプト案

```javascript
generate_image(
  ImageName: "yuto_panic_chart_fixed_v15_5",
  Prompt: "ARCHITECTURE: [v15.5 EDGE OBLITERATOR] FULL BLEED. ZERO PIXEL MARGINS. 110% OVERFILL. **VERTICAL PORTRAIT ORIENTATION. 12:17 RATIO.**

CHARACTERS:
- Yuto: ((Navy Blue Suit:1.3)), ((White Shirt)), ((Blue Tie:1.3)), ((Short Black hair)). (Face pale, sweating, eyes wide with horror, looking at smartphone). **VISUAL LOCK**.

[COMPOSITION - 3 PANELS]:

- [PANEL 1 - 40% height]: FULL WIDTH FILL. Yuto staring at his phone. In the background, a chaotic stock chart (green and red candles) is bouncing up and down violently.
  Yuto Speech Bubbles: '上がった?!', 'いや、また下がった……！', 'うわああ、どうすればいいんだ!?'

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

## 修正のポイント

1. **タイポの修正**: `クリットなか？` → `メリットなか？` (または文脈に合わせて `メリットか？`)
2. **構成の維持**: 元の画像の3パネル構成（乱高下 → 囁き → 動悸）を言語化。
3. **キャラ固定**: 優斗のビジュアルロックを適用。

## 検証方法

1. 作成したプロンプトをユーザーに提示し、意図と合致しているか確認いただく。
