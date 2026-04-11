Title: Antigravity × Gemma 4 完全統合ガイド — ローカルLLMでプライバシー保護開発環境を構築する | Antigravity Lab

Description: 2026年4月2日にApache 2.0でリリースされたGemma 4を、Antigravityのローカルモデルとして統合する方法を解説。OllamaとLM Studioを使ったセットアップから、コードが端末外に出ないプライバシー保護開発ワークフローまで実践的に紹介します。

Source: https://antigravitylab.net/articles/integrations/antigravity-gemma4-local-llm-dev-workflow-guide

---

## なぜ今「ローカル LLM + Antigravity」なのか
2026年4月2日、Google はGemma 4を Apache 2.0 ライセンスでリリースしました。注目すべきは、最小モデルの E2B（約 12B パラメータ）がコンシューマー向けノートパソコンの GPU（VRAM 8GB 以上）で快適に動作し、26B・31B といった大型モデルでも M3 MacBook Pro や RTX 4090 搭載の Windows PC で現実的な速度を出せる点です。
Antigravity は外部APIとの接続だけでなく、OpenAI互換エンドポイントをサポートしているため、Gemma 4 を Ollama や LM Studio でローカルサーバとして起動すれば、クラウドの代わりにローカルモデルを使う構成が実現できます。

### この構成の主なメリット
- **プライバシーとセキュリティ**: コードが一切クラウドに送られない。
- **オフライン対応**: ネット接続なしで AI アシストが使える。
- **コスト最適化**: API コスト不要。

## Gemma 4 のモデル構成を理解する
Gemma 4 は4つのバリアントで提供されています（2026年4月時点）：
- **E2B（約 12B パラメータ）**: ノートPC 環境向け。VRAM 8GB で動作。
- **E4B（約 27B パラメータ）**: VRAM 16GB 推奨。より複雑なコード理解が可能。
- **26B（フルサイズ）**: VRAM 24GB 以上推奨。設計議論に適している。
- **31B（最大モデル）**: RTX 4090 クラスの GPU が必要。最高品質のコード生成。

## 環境構築: Ollama で Gemma 4 を起動する

### Ollama のインストール
Windows の場合は [Ollama 公式サイト](https://ollama.com/) からインストーラーをダウンロードしてください。

### Gemma 4 モデルのダウンロード
```bash
# E2B モデル（推奨: まずこれから試す）
ollama pull gemma4:e2b
```

### サーバーとして起動
```bash
# Ollama を OpenAI 互換サーバーとして起動
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

## Antigravity に Gemma 4 を接続する

### 設定ファイルでの接続設定
`antigravity.config.json` または設定 UI から以下のように設定します。

```json
{
  "models": {
    "local": {
      "provider": "openai-compatible",
      "baseUrl": "http://localhost:11434/v1",
      "model": "gemma4:e2b",
      "apiKey": "ollama",
      "temperature": 0.1,
      "maxTokens": 4096,
      "contextWindow": 128000
    }
  },
  "defaultModel": "local"
}
```

### モデルの切り替えショートカット
チャット内でコマンドを使って切り替えられます。
- `@local` → Gemma 4（ローカル）
- `@claude` → Claude
- `@gemini` → Gemini

## 実際の開発ワークフロー
- **パターン1: ハイブリッド**: 日常的な補完はローカル、複雑な設計はクラウド。
- **パターン2: 強制ローカル**: 機密プロジェクト向け。クラウド接続を完全に遮断。
- **パターン3: オフライン**: 出張先や機内での開発。

## まとめ
Gemma 4 + Antigravity の統合は、プライバシー・オフライン・コストの課題を解決します。まずは軽量な E2B モデルから試して、ローカル AI の快適さを体験してみてください。
