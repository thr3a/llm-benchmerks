ローカルLLMサーバーの速度ベンチマークツール。プロンプト処理速度(pp)とトークン生成速度(tg)を計測し、CSVに保存する。

## コマンド

```
uv run run-benchmark.py --base-url https://example/v1 --model deep01 --count 3
```

# パターン

### saitama

- 概要
  - 「埼玉県の魅力を1000文字で紹介してください」というプロンプト
- 意図
  - 日本語のトークン生成速度(tg)を測る

### async_retry_comment

- 概要
  - `async_retry_client.txt` のPythonコードに日本語でコードコメントを付けさせる
- 意図
  - コードの生成速度(tg)を測る
  - 一部日本語も含むので実用的

### summarize

- 概要
  - `8700tokens.md`（約8700トークンの長文）を3行に要約させる
- 意図
  - 日本語のプロンプト処理速度(pp)を測る

### 新しいパターンの追加

- `patterns/` に1ファイル追加し、`PATTERN` を定義して `ALL_PATTERNS` に登録するだけで拡張できる
