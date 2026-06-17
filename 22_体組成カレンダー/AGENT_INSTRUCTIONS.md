# AI Agent Instructions (CodeX & Antigravity)

このプロジェクト（体組成カレンダー）は、AIエージェント（CodeX や Antigravity、Cursor など）が共同でスムーズに開発・メンテナンスを行えるように設計されています。
開発に参加するAIは、必ずこのガイドラインに目を通し、方針に従って作業を行ってください。

## 🛠️ プロジェクト構造
- **フロントエンド**: `public/index.html`, `public/script.js`, `public/styles.css` (Vanilla HTML/JS/CSS)
- **バックエンド**: `worker.js` (Cloudflare Workers API)
- **データベース**: Cloudflare D1 (`schema.sql` でスキーマ定義)
- **設定ファイル**: `wrangler.toml`, `package.json`

## 🚀 主要コマンド
環境内では `npm` 経由でコマンドを実行できるように `package.json` に設定しています。

- **ローカル開発サーバー起動**: `npm run dev` (Wrangler dev)
- **本番環境へのデプロイ**: `npm run deploy` (Wrangler deploy)
- **構文エラーチェック**: `npm run verify`

## 💡 開発のルールと方針
1. **フレームワークの不使用**: React や Vue、Tailwind などのフレームワークは導入せず、Vanilla JS と CSS で開発してください。
2. **文字コードの徹底**: ファイルを編集・作成する際は、必ず **UTF-8** で保存してください。ターミナルコマンド実行時は `$env:PYTHONUTF8=1` や `-Encoding UTF8` などの指定を忘れずに行ってください。
3. **安全なデータ操作**: Cloudflare D1 にアクセスする際、本番データベースを直接破壊するような操作（DROP TABLE など）はユーザーの明示的な許可なく実行しないでください。
4. **段階的な確認**: 大きな機能追加や仕様変更を行う際は、事前にユーザーに実装計画を提案し、承認を得てからコードを変更してください。
5. **自己検証の実施**: アンチグラビティは作業完了時に必ずルートディレクトリの `python scripts/antigravity_check.py` を実行して、エラーがないか（GREENか）を確認してから報告してください。

## 📝 連携時の注意点
- CodeX と Antigravity は、互いの作業内容をコードの変更履歴（git）やファイルの現状から読み取って継続してください。
- ユーザーに質問する場合は、専門用語を避け、分かりやすい日本語で簡潔に説明してください。
