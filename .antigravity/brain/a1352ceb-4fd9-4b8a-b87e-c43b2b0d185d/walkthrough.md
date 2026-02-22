# Walkthrough - レミの衣装カラー修正 (赤スーツへの強制)

## 実施内容

生成画像においてレミの衣装が黒くなる問題を解決するため、以下の強化修正を EP13.10、13.11、13.12 の全ページ（計12ページ）に適用しました。

### 1. ポジティブプロンプトの強化

- `Crimson Red Suit Jacket` の指定を `ONLY Crimson Red Suit Jacket:2.0` に変更。
- `(NO other colors, NO black clothing)` などの排他的な指示を追加。

### 2. ネガティブプロンプトの強化

- 黒、灰色、濃色のスーツを個別かつ重み付きで除外：`(black suit:1.5), (dark suit:1.5), (gray suit:1.5)`
- レミへの黒い服の混入を直接禁止：`(black clothes on remi:1.5)`
- 白シャツの重み付き除外：`(white shirt on remi:1.5)`

## 修正済みファイル

- [EP13.10_不平等の理.md](file:///c:/Users/hirak/Desktop/2nd-Brain/18_レミ投資漫画/マンガノ/01_長編_希望 of 投資/01_ストーリー/EP13.10_不平等の理.md)
- [EP13.11_資産の種.md](file:///c:/Users/hirak/Desktop/2nd-Brain/18_レミ投資漫画/マンガノ/01_長編_希望 of 投資/01_ストーリー/EP13.11_資産の種.md)
- [EP13.12_冷徹な平熱.md](file:///c:/Users/hirak/Desktop/2nd-Brain/18_レミ投資漫画/マンガノ/01_長編_希望 of 投資/01_ストーリー/EP13.12_冷徹な平熱.md)

## 検証結果

プロンプト上の記述において、他の色の入り込む余地を技術的に排除しました。これにより、一貫して赤いスーツを着用したレミが生成されるようになります。
