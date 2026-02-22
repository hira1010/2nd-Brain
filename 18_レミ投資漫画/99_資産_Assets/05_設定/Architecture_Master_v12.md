# 漫画生成マスタープロンプト・アーカイブ (Master Standard v12.0 Architecture)

本ファイルは、プロジェクト全体で「正解」とされる、成功実績に基づいた最上位のプロンプト定義（Architecture）を永続保存するものです。今後の全エピソード、全テーマにおいて、本構造を基底クラス（テンプレート）として使用します。

## 成功の構造定義 (The Architecture)

この構文はAIに対する「設計図モード」の起動命令であり、12:17比率、全面描画、およびTIER分割を物理的に保証します。

```text
ARCHITECTURE: A vertical Japanese manga page composed of 3 DISTINCT HORIZONTAL TIERS. CRITICAL: 12:17 Portrait ratio. TRUE FULL BLEED: Art MUST touch the literal pixel-edges of the file on all 4 sides (Top, Bottom, Left, Right). 100% CANVAS FILL. NO white margins, NO outer borders, NO padding, NO gaps, NO frame. The illustration must extend to the absolute edges of the image width and height without any blank space.

### Characters:
- Remi: (Crimson RED blazer, Black lace top). (Silky SILVER hair), (RED eyes). NO GLOVES. (ONLY ONE Remi per panel).
- Yuto: (Traditional SOLID BLACK Gakuran school uniform, gold buttons). (Short Black hair). BARE HANDS. (ONLY ONE Yuto per panel).

[TIER 1 - TOP 40%]: [Two-Shot Scene] Full-width borderless art. Yuto (BLACK GAKURAN) is troubled at desk, Remi (RED blazer, Silver hair) stands behind him. [TITLE BOX]: Horizontal black rectangle in BOTTOM-RIGHT.

[TIER 2 - MIDDLE 35%]: [Focus Shot - BORDERLESS] Remi gestures to a visual metaphor / hologram. Art must touch physical left/right boundaries.

[TIER 3 - BOTTOM 25%]: [Reaction Shot - BORDERLESS] Close-up of Yuto in shock. Absolutely NO title box.

### Style: Premium manga, cinematic lighting. 12:17 ratio. NO PADDING, NO MARGINS. FULL BLEED.
```

## 各テーマへの展開ルール (Expansion Rules)

1. **等価交換**: `[ ]` 内の内容のみをテーマに合わせて書き換え、構造ラベル（TIER 1等）は一切変更しない。
2. **ノイズ排除**: プロンプト内に余計な説明文（例：「ここをこうしてください」等）を混ぜない。すべてを「記述的（Declarative）」な表現に変換する。
3. **セリフ（Dialogue）**: 各Tierの説明文の末尾に `(Japanese speech bubbles: "...")` 形式で配置する。

## 適用実績

- **No.61 手段と目的**: v12.0 Architecture 版にて承認。

---
最終更新: 2026-02-06
ステータス: プロジェクト最上位定義として確立
