# 体組成ログ

体組成計の文字データを貼り付けて、体重・体脂肪率・筋肉量・BMI・内臓脂肪・基礎代謝・体内年齢を記録してグラフ化するサイトです。

## ローカルで使う

`index.html` をブラウザで開くと使えます。ローカル利用時の保存先はブラウザの `localStorage` です。

```powershell
node server.js
```

上のコマンドで `http://127.0.0.1:5179/` からも確認できます。

## 変更後の確認

```powershell
npm run verify
```

このコマンドで、サイト・Workerの構文チェックと、6/9形式・絵文字つき6/13形式の読み取りテストを実行します。

## Cloudflareでメール追加を使う

Cloudflare Workers + D1 + Email Routing を使うと、iPhoneのOCRで読み取った文字データをメール本文として送るだけで記録できます。

1. Wranglerを使える状態にします。
   ```powershell
   npm install -g wrangler
   wrangler login
   ```

2. D1を作成します。
   ```powershell
   wrangler d1 create body-composition
   ```

3. 表示された `database_id` を `wrangler.toml` の `REPLACE_WITH_D1_DATABASE_ID` と置き換えます。

4. D1にテーブルを作ります。
   ```powershell
   wrangler d1 execute body-composition --remote --file=schema.sql
   ```

5. Workerをデプロイします。
   ```powershell
   wrangler deploy
   ```

6. Cloudflare Dashboard の Email Routing で、受信用メールアドレスをこのWorkerにルーティングします。

メール本文には、次のようなOCR済みテキストだけを入れれば保存されます。

```text
6/9

体重
93.30 kg
体脂肪
29.5 %（27.5 kg）
骨格筋
全体：29.6 %（27.9 kg）
内臓脂肪レベル
16.5 level
基礎代謝
1,951 kcal
体年齢
58 才
BMI
29.4
```

## API

- `GET /api/logs`: 記録一覧
- `POST /api/logs`: サイトから1件保存
- `DELETE /api/logs/:date`: 指定日の削除
- `DELETE /api/logs`: 全削除
- `POST /api/email-test`: メール本文と同じ文字列で保存テスト
