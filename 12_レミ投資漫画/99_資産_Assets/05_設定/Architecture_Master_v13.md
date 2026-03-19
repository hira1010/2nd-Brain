# 漫画生成マスタープロンプト・アーカイブ (Master Standard v13.0 Full Bleed)

本ファイルは、プロジェクト全体で「正解」とされる、成功実績に基づいた最上位のプロンプト定義（Architecture）を、さらに「右余白」等の不備を解消した最終安定版として保存するものです。

## 究極の構造定義 (The Architecture v13.0)

この構文はAIに対し、物理的なキャンバスの端から端までを描画することを強制し、標準的な漫画の「余白（Safe Area）」を完全に無視させます。

```text
ARCHITECTURE: A vertical Japanese manga page composed of 3 DISTINCT HORIZONTAL TIERS. CRITICAL: 12:17 Portrait ratio. MANDATORY: ZERO MARGINS ON ALL SIDES. Art MUST fill 100% of the canvas width, touching both literal left and right pixel-edges without any gap. TRUE FULL BLEED: Art MUST touch the literal pixel-edges (Top, Bottom, Left, Right). 100% CANVAS FILL. NO white strips on sides, NO safe area, NO padding, NO outer frame. The illustration must extend to the absolute edges of the image width and height.

### Characters:
- Remi: (Crimson RED blazer, Black lace top). (Silky SILVER hair), (RED eyes). NO GLOVES. (ONLY ONE Remi per panel).
- Yuto: (Traditional SOLID BLACK Gakuran school uniform, gold buttons). (Short Black hair). BARE HANDS. (ONLY ONE Yuto per panel).

[TIER 1 - TOP 40%]: [Scene Description] Art MUST stretch to 100% width. (Japanese speech bubbles: "...")

[TIER 2 - MIDDLE 35%]: [Scene Description] Art MUST stretch to 100% width. (Japanese speech bubbles: "...")

[TIER 3 - BOTTOM 25%]: [Scene Description] Art MUST stretch to 100% width. (Japanese speech bubbles: "...")

### Style: Premium manga, cinematic lighting. 12:17 ratio. NO PADDING, NO MARGINS. FULL WIDTH FILL.
```

## 各テーマへの展開ルール (Expansion Rules)

1. **幅 100% の強制**: 各 Tier の説明冒頭に `Art MUST stretch to 100% width.` を配置し、AI が左右に余白を残す余地を封殺します。
2. **ノイズ排除**: 前バージョン同様、Architecture 構造以外の装飾語を徹底的に削ぎ落とします。
3. **等価交換**: 中身の記述のみをテーマに合わせて入れ替えます。

---
最終更新: 2026-02-06
ステータス: 右余白問題を物理的に解決した v13.0 規格として確立
