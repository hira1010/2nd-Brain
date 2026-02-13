# Episode {NO}: {TITLE}

## TIPS情報

| 項目 | 内容 |
| :--- | :--- |
| EP | {NO} |
| タイトル | {TITLE} |
| 解説 | {DESC} |

---

## Page 1 (The Hook)

```javascript
generate_image(
  ImageName: "remi_ep{NO_CLEAN}_p1_v1",
  Prompt: "((Vertical Portrait A4 Ratio)), ((Long Strip Format)), ((Manga Page Layout)). ((NO TEXT, NO WORDS, NO LABELS)). (High Quality Manga Layout). (Full Bleed).

[Scene]:
Remi: ((Crimson Red Suit Jacket)), ((Black Lace High-neck Camisole)), ((Tight Red Skirt)). (Silver Long Hair, Hime-cut), (Sharp Red Eyes, Cool Beauty Face). **VISUAL LOCK**.
Yuto: ((Navy Blue Suit)), (White Shirt), ((Blue Tie)). (Short Black hair, slightly messy). **VISUAL LOCK**.

[Panel 1]: {SCENE}. Remi stands calmly next to a large holographic display showing '{TITLE}'. Unlike usual, the screen shows a simple balanced symbol. Yuto looks puzzled.
[Panel 2]: Close-up. Remi's face, mysterious. **STRICT SPEECH BUBBLE**: '{DIALOGUE_INTRO}'
[Panel 3]: Visualization. A clear comparison or balanced symbolic image representing the core concept of '{TITLE}'. Remi points to the correct/positive side. **STRICT SPEECH BUBBLE**: '{DIALOGUE_TEACH}'

(Style: Premium Digital Anime, Mathematical surrealism, Cosmic scales, Glowing geometric patterns).
**NEGATIVE PROMPT**: text, title, alphabet, signature, watermark, username, speech bubble, chat bubble, quote, writing, caption, english text, error, glitch, noise, jpeg artifacts, borders, white frame, architectural text, white shirt, collared shirt, blouse, ((black dress)), ((black clothes)), ribbon, school uniform.
"
)
```

## Page 2 (The Insight)

```javascript
generate_image(
  ImageName: "remi_ep{NO_CLEAN}_p2_v1",
  Prompt: "((Vertical Portrait A4 Ratio)), ((Long Strip Format)), ((Manga Page Layout)). ((NO TEXT, NO WORDS, NO LABELS)). (High Quality Manga Layout). (Full Bleed).

[Scene]:
Remi: ((Crimson Red Suit Jacket)), ((Black Lace High-neck Camisole)), ((Tight Red Skirt)). (Silver Long Hair, Hime-cut), (Sharp Red Eyes, Cool Beauty Face). **VISUAL LOCK**.
Yuto: ((Navy Blue Suit)), (White Shirt), ((Blue Tie)). (Short Black hair, slightly messy). **VISUAL LOCK**.

[Panel 1]: Visual Manifestation. Close up on Remi holding a small, glowing sphere of light or symbol that represents '{TITLE}'. It shines brighter than the Background elements. **STRICT SPEECH BUBBLE**: '{DIALOGUE_DESC}'
[Panel 2]: Contrast Scene. Remi stands in a split world. On her left, a chaotic storm representing 'Risk/Confusion'. On her right, a peaceful, golden garden representing '{TITLE}'. She calmly points towards the peace.
[Panel 3]: Realization. Yuto looking enlightened and relieved. **STRICT SPEECH BUBBLE**: '{DIALOGUE_ACTION}'

(Style: Premium Digital Anime, Breathtaking miracle, Particle effects, Divine lighting).
**NEGATIVE PROMPT**: text, title, alphabet, signature, watermark, username, speech bubble, chat bubble, quote, writing, caption, english text, error, glitch, noise, jpeg artifacts, borders, white frame, architectural text, white shirt, collared shirt, blouse, ((black dress)), ((black clothes)), ribbon, school uniform.
"
)
```

---

Created: {TODAY}
