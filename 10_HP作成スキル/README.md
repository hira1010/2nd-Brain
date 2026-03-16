# 🌐 HP作成スキル (Gemini x GitHub x Vercel)

このフォルダは、みらいち（MIRAICHI）さんのワークショップ **「GeminiでWebサイトを作ってGitHubで公開しよう！」** の流れをAntigravityで実践するためのスキルセットです。

## 🚀 ワークフロー

### 1. Webサイトの生成 (Antigravity)

専用プロンプトを使用して、AntigravityにWebサイトのコードを作らせます。

- `prompts/hp_generator_prompt.md` をコピーしてチャットに貼り付けるか、直接指示してください。
- 成果物（`index.html`, `style.css` 等）はこのフォルダ内に作成します。

### 2. GitHubへのプッシュ

`deploy_helper.ps1` を使用して、作成したプロジェクトをGitHubリポジトリにアップロードします。

### 3. Vercelで公開

1. [Vercel](https://vercel.com/) にログイン。
2. 「Add New」→「Project」を選択。
3. GitHubリポジトリをインポートしてデプロイ。

---

## 🛠️ ツール構成

- **プロンプト**: `prompts/hp_generator_prompt.md`
- **デプロイ補助**: `deploy_helper.ps1`
