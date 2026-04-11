# キャラクター「アイ」生成用テンプレート

このテンプレートを使用することで、一貫したビジュアルの「アイ」を生成できます。

## 1. ページ構成用テンプレート（基本）

```javascript
generate_image(
  ImageName: "ai_character_v1",
  Prompt: "((Vertical Portrait A4 Ratio)), ((Manga Page Layout)). ((NO TEXT)). 
  [Scene]: 
  Ai: (Short BLACK hair:1.5), (Amber eyes:1.4), (Calm expression:1.2). 
  Wearing a (Navy blue school blazer:1.3), (Red necktie:1.3), (Beige cardigan:1.2). 
  NO GLOVES. (ONLY ONE Ai per panel).
  
  [Panel 1]: Ai standing in a classroom, looking at a smartphone with a serious face.
  [Panel 2]: Close-up of Ai's face, slightly smiling.
  "
)
```

## 2. アルバイト(喫茶店)モード

```javascript
generate_image(
  ImageName: "ai_waitress_v1",
  Prompt: "((Vertical Portrait A4 Ratio)), ((Manga Page Layout)). ((NO TEXT)). 
  [Scene]: 
  Ai: (Short BLACK hair:1.5), (Amber eyes:1.4), (Cool face:1.2). 
  Wearing a (White shirt:1.3), (Black apron:1.3), (Black bow tie:1.2). 
  NO GLOVES. (ONLY ONE Ai per panel).
  
  [Panel 1]: Ai holding a tray in a stylish cafe.
  [Panel 2]: Ai bowing slightly to a customer.
  "
)
```
