# No.63 rとg - プロンプト

## TIP情報

| 項目 | 内容 |
| :--- | :--- |
| No | 63 |
| タイトル | rとg |
| 解説 | 投資側（r）に回る重要性。 |
| カテゴリー | 03_戦略・リスク管理 |

---

## 1. キャラクター設定

### レミ (Remi)

- **外見**: 銀髪のロングヘア（センター分け）、赤色の目
- **服装**: 鮮やかな赤のブレザー、黒レースのインナー（お手本画像を完全再現）

### ユウト (Yuto)

- **外見**: 短い黒髪
- **服装**: 黒の学ラン（金ボタン）

---

## 1ページ目プロンプト

```text
FORMAT: TALL VERTICAL PORTRAIT (1024x1792). ONE SINGLE high-end 2D anime manga page. **MANDATORY**: VIBRANT FULL COLOR. **STYLE**: PURE 2D ANIME (CEL SHADED). Sharp clean lineart, FLAT COLORS, NO 3D shading, NO realistic gradients. **MASTERS STANDARD**: High-contrast Japanese anime aesthetics. The illustration MUST be TALL and FILL the entire vertical canvas. NO side margins. Use clean white gutters between panels. NO black borders.

### Characters: Remi: (Crimson RED eyes). (WAIST-LENGTH needle-thin STARK SILVER hair:1.8). (STRICT CENTER-PARTED bangs). (Cool beauty). Remi wears a (Vibrant Crimson RED blazer over a BLACK LACE inner top). **VISUAL LOCK**: Pure silver hair, center-parted. Red blazer. No 3D shading on skin. Sharp 2D eyes., Yuto: (Short Black hair). (Traditional BLACK Gakuran school uniform). Dynamic 2D anime style.. ### Anatomy: Perfect anime fingers (5), symmetrical eyes.

### INTEGRATED 2D MASTERPIECE (VERTICAL PORTRAIT / FULL COLOR / BLANK BUBBLES)
[Panel 1 (Top, 40% height)]: [Cosmology] Giant golden glowing brain in deep space nebula. Pure 2D anime. **TITLE CARD**: A small horizontal black title box with Japanese text "rとg" (Ensure accurate spelling). NO ENGLISH.. **MANDATORY**: VERTICAL ORIENTATION.

[Panel 2 (Middle, 30% height)]: [Teaching] Remi (red blazer) amidst swirling golden energy. **BLANK SPEECH BUBBLE**.

[Panel 3 (Bottom, 30% height)]: [Awe] Yuto looking up. High-contrast 2D lighting. Reach both side edges.

### Technical Style: **PURE 2D ANIME (CEL SHADED)**. Sharp lineart. NO 3D effects. NO gradients on skin. TALL VERTICAL PORTRAIT ONLY. **LEAVE ALL SPEECH BUBBLES BLANK** (No text inside).
```

## 2ページ目プロンプト

```text
FORMAT: TALL VERTICAL PORTRAIT (1024x1792). ONE SINGLE high-end 2D anime manga page. **MANDATORY**: VIBRANT FULL COLOR. **STYLE**: PURE 2D ANIME (CEL SHADED). Sharp clean lineart, FLAT COLORS, NO 3D shading, NO realistic gradients. **MASTERS STANDARD**: High-contrast Japanese anime aesthetics. The illustration MUST be TALL and FILL the entire vertical canvas. NO side margins. Use clean white gutters between panels. NO black borders.

### Characters: Remi: (Crimson RED eyes). (WAIST-LENGTH needle-thin STARK SILVER hair:1.8). (STRICT CENTER-PARTED bangs). (Cool beauty). Remi wears a (Vibrant Crimson RED blazer over a BLACK LACE inner top). **VISUAL LOCK**: Pure silver hair, center-parted. Red blazer. No 3D shading on skin. Sharp 2D eyes., Yuto: (Short Black hair). (Traditional BLACK Gakuran school uniform). Dynamic 2D anime style.. ### Anatomy: Perfect anime fingers (5), symmetrical eyes.

### INTEGRATED 2D MASTERPIECE (VERTICAL PORTRAIT / FULL COLOR / BLANK BUBBLES)
[Panel 1 (Top, 40% height)]: [Guidance] Path of light through stars. Flat 2D art. TALL layout.

[Panel 2 (Middle, 30% height)]: [Remi Solo] Remi glowing with 2D aura. **BLANK SPEECH BUBBLE**.

[Panel 3 (Bottom, 30% height)]: [Understanding] Yuto in awe. Professional 2D anime style.

### Technical Style: **PURE 2D ANIME (CEL SHADED)**. Sharp lineart. NO 3D effects. NO gradients on skin. TALL VERTICAL PORTRAIT ONLY. **LEAVE ALL SPEECH BUBBLES BLANK** (No text inside).
```

---

## 重要な生成手順

### ステップ1: 1ページ目を生成

```text
generate_image(
  ImageName: "remi_no63_page1",
  Prompt: [上記1ページ目プロンプトを完全にコピペ],
  Size: "1024x1792"
)
```

---

作成日: 2026-02-06
ステータス: お手本画像に基づく画風・キャラ・ノイズ対策対応完了
