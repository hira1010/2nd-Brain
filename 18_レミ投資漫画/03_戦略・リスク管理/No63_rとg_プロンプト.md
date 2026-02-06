# No.63 r > g 漫画生成プロンプト (Master Standard v15.0 Edge Crusher)

## TIP情報

| 項目 | 内容 |
| :--- | :--- |
| No | 63 |
| タイトル | r > g |
| 解説 | 労働（g）より資本（r）の成長が早い。富の格差の根本原因。 |

---

## 1ページ目プロンプト (v15.0 Edge Crusher)

```text
ARCHITECTURE: FULL BLEED WALL-TO-WALL CINEMATIC ARTWORK. MASKED AS A 3-PANEL VERTICAL PAGE. CRITICAL: 12:17 Portrait ratio. MANDATORY: ZERO PIXEL INTERNAL MARGINS. ART MUST PHYSICALLY TOUCH AND BLEED OFF THE LITERAL 1224x1728 PIXEL BOUNDARIES. NO WHITE SIDE BORDERS. NO PILLARBOXING. DRAW BEYOND THE CANVAS EDGE TO ENSURE ZERO WHITE SPACE. **MANDATORY**: DO NOT DRAW ANY LABELS LIKE "[TOP...]" OR "[PANEL...]". DRAW ONLY THE STORY CONTENT.

### Characters:
- Remi: (Crimson RED blazer, Black lace top). (Silky SILVER hair), (RED eyes). NO GLOVES. (ONLY ONE Remi per panel).
- Yuto: (Traditional SOLID BLACK Gakuran school uniform, gold buttons). (Short Black hair). BARE HANDS. (ONLY ONE Yuto per panel).

[TOP PANEL - 40% height]: [Action Scene] FULL WIDTH ART. Art MUST stretch to 100% width, touching the literal pixel-edges. Remi draws a giant flaming formula "r > g" in space near a giant scale. **STRICT TITLE BOX**: A HORIZONTAL black rectangular title box placed in the BOTTOM-RIGHT corner of THIS TOP PANEL, containing white Japanese text "rとg". (Japanese speech bubbles: "優斗君、これが世界のルールを支配する『残酷な不等式』よ。", "r（資本収益）は常にg（経済成長）を追い越す。")

[MIDDLE PANEL - 35% height]: [Focus Shot - FULL WIDTH] FULL WIDTH ART. Art MUST stretch to 100% width, NO MARGINS. The scale tilts heavily toward the "r" side (golden key). The "g" side (heavy hammer) is pulled up. (ONLY ONE Remi). (Japanese speech bubble: "お金がお金を生むスピードは、人が働いて得る豊かさを追い越してきた。働くだけでは一生追いつけないのよ。")

[BOTTOM PANEL - 25% height]: [Reaction Shot - FULL WIDTH] FULL WIDTH ART. Art MUST stretch to 100% width, NO MARGINS. Close-up of Yuto (BLACK GAKURAN) in shock. (Japanese speech bubble: "どんなに頑張っても最初から負けるようにできているっていうのか…！？")

### Style: Premium manga, cinematic lighting. 12:17 ratio. NO PADDING, NO MARGINS. LITERAL FULL WIDTH FILL. **NEG PROMPT**: NO side labels, NO text labels, NO margin text, NO white bars, NO grey borders.
```

---

## 2ページ目プロンプト (v15.0 Edge Crusher)

```text
ARCHITECTURE: FULL BLEED WALL-TO-WALL CINEMATIC ARTWORK. 12:17 ratio. ZERO PIXEL MARGINS. FULL WIDTH OVERFLOW. NO LABELS, NO MARGIN TEXT.

### Characters:
- Remi: (RED blazer). (SILVER hair). NO GLOVES.
- Yuto: (BLACK Gakuran). BARE HANDS.

[TOP PANEL - 40% height]: [Metaphor] FULL WIDTH FILL. Visualization of an "r-Escalator" and a "g-Runner". Remi rides golden escalator rising to stars, while people below are running on flat path. (Japanese speech bubbles: "資本(r)は複利で加速し、賃金(g)は良くて鈍足。このわずかな差が、乗り越えられない壁を作るの。", "投資の側に回らなければ、地平線は遠のくばかりよ。")

[MIDDLE PANEL - 35% height]: [Focus Shot] FULL WIDTH FILL. Close-up Remi pointing to golden "Investment Door". (Japanese speech bubble: "抜け出す道は一つ。労働で得た種を、成長の側へ植え替えること。")

[BOTTOM PANEL - 25% height]: [Perspective] Yuto holding golden seed. (Japanese speech bubble: "給料の一部を資本に移し替える… 数式の呪いを解くのは、僕の決断なんだ。")

### Style: Premium manga, cinematic lighting. 12:17 ratio. LITERAL FULL WIDTH FILL.
```

---

## 3ページ目プロンプト (v15.0 Edge Crusher)

```text
ARCHITECTURE: FULL BLEED WALL-TO-WALL CINEMATIC ARTWORK. 12:17 ratio. ZERO PIXEL MARGINS. FULL WIDTH OVERFLOW. NO LABELS, NO MARGIN TEXT.

### Characters:
- Remi: (RED blazer). (SILVER hair). NO GLOVES.
- Yuto: (BLACK Gakuran). BARE HANDS.

[TOP PANEL - 40% height]: [Action] FULL WIDTH FILL. Remi showing glowing terminal displaying 'INDEX FUND'. (Japanese speech bubbles: "今は誰でも大企業のオーナーになれる。特別な階級なんていらないわ。", "ただ、インデックスという橋を渡る勇気があればいいの。")

[MIDDLE PANEL - 35% height]: [Action] Yuto pressing button on terminal, golden stardust. (Japanese speech bubble: "一歩を踏み出す。数式の向こう側、成長の世界へ。")

[BOTTOM PANEL - 25% height]: [Resolve] Remi nodding with cosmic background. (Japanese speech bubble: "ええ。その決断が、あなたの人生という資本を最大化させるの。")

### Style: Premium manga, cinematic lighting. 12:17 ratio. LITERAL FULL WIDTH FILL.
```

---

## 4ページ目プロンプト (v15.0 Edge Crusher)

```text
ARCHITECTURE: FULL BLEED WALL-TO-WALL CINEMATIC ARTWORK. 12:17 ratio. ZERO PIXEL MARGINS. FULL WIDTH OVERFLOW. NO LABELS, NO MARGIN TEXT.

### Characters:
- Remi: (RED blazer). (SILVER hair). NO GLOVES.
- Yuto: (BLACK Gakuran). BARE HANDS.

[TOP PANEL - 40% height]: [Epilogue] Yuto and Remi on mountain of light, formula "r > g" shining like constellation in sky. (Japanese speech bubbles: "不条理を嘆くのではなく、不条理を味方にしなさい。", "世界は、動く勇気がある者にだけ優しいのよ。")

[MIDDLE PANEL - 35% height]: [Focus Shot] Close-up Yuto with bright smile. (Japanese speech bubble: "レミさん、僕、もう走るのをやめません。成長の波に、乗り続けます！")

[BOTTOM PANEL - 25% height]: [Final] Remi looking at camera with beautiful smile. (Japanese speech bubble: "さあ、最高にロジカルな、あなたの物語を。")

### Style: Premium manga, cinematic lighting. 12:17 ratio. LITERAL FULL WIDTH FILL.
```

---

## 生成手順 (v15.0 Edge Crusher)

### ステップ1: 1ページ目を生成

```javascript
generate_image(
  ImageName: "remi_no63_page1_v15_ms",
  Prompt: "ARCHITECTURE: FULL BLEED WALL-TO-WALL CINEMATIC ARTWORK. MASKED AS A 3-PANEL VERTICAL PAGE. CRITICAL: 12:17 Portrait ratio. MANDATORY: ZERO PIXEL INTERNAL MARGINS. ART MUST PHYSICALLY TOUCH AND BLEED OFF THE LITERAL 1224x1728 PIXEL BOUNDARIES. NO WHITE SIDE BORDERS. NO PILLARBOXING. DRAW BEYOND THE CANVAS EDGE TO ENSURE ZERO WHITE SPACE. **MANDATORY**: DO NOT DRAW ANY LABELS LIKE '[TOP...]' OR '[PANEL...]'. DRAW ONLY THE STORY CONTENT. ### Characters: - Remi: (RED blazer, Black lace top). (SILVER hair). (RED eyes). NO GLOVES. - Yuto: (BLACK Gakuran, gold buttons). (Short Black hair). BARE HANDS. [PANEL 1 - 40% height]: FULL WIDTH ART. Remi draws giant flaming formula 'r > g' in space near a giant scale. **STRICT TITLE BOX**: A HORIZONTAL black rectangular title box placed in the BOTTOM-RIGHT corner of THIS PANEL, with white Japanese text 'rとg'. (Japanese speech bubbles: '優斗君、これが残酷な不等式よ。', 'rは常にgを追い越す。') [PANEL 2 - 35% height]: FULL WIDTH ART. NO MARGINS. Scale tilts heavily toward 'r' side (golden key). 'g' side pulled up. (Japanese speech bubble: 'お金がお金を生むスピードは、人が働いて得る豊かさを追い越してきた。働くだけでは一生追いつけないのよ。') [PANEL 3 - 25% height]: FULL WIDTH ART. NO MARGINS. Close-up of Yuto (BLACK GAKURAN) in shock. (Japanese speech bubble: 'どんなに頑張っても最初から負けるようにできているっていうのか…！？') ### Style: Premium manga, cinematic lighting. 12:17 ratio. LITERAL FULL WIDTH FILL. **NEG PROMPT**: NO side labels, NO text labels, NO margin text, NO white bars, NO grey borders."
)
```

---
作成日: 2026-02-06
ステータス: No.63 全4ページ v15.0 Edge Crusher 完備
