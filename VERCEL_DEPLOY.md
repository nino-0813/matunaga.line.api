# Vercelデプロイ手順

このAPIをVercelで公開する手順です。

## ✅ Vercelで動作する理由

- ✅ **サーバーレス関数として動作**: Vercelはサーバーレス関数としてFlaskアプリを実行します
- ✅ **自動スケーリング**: リクエストに応じて自動的にスケールします
- ✅ **無料プランあり**: 個人利用なら無料で使えます
- ✅ **自動デプロイ**: GitHubと連携すれば、プッシュするだけで自動デプロイ

## 📋 前提条件

- ✅ GitHubリポジトリにコードがプッシュされている
- ✅ Vercelアカウントを持っている（GitHubアカウントでサインアップ可能）

---

## 🚀 デプロイ手順

### ステップ1: Vercelアカウントを作成

1. [Vercel](https://vercel.com/)にアクセス
2. 「Sign Up」をクリック
3. 「Continue with GitHub」を選択してGitHubアカウントでログイン

### ステップ2: プロジェクトをインポート

1. Vercelダッシュボードで「Add New...」→「Project」をクリック
2. GitHubリポジトリ `nino-0813/matunaga.line.api` を選択
3. 「Import」をクリック

### ステップ3: プロジェクト設定

Vercelが自動的に設定を検出しますが、以下を確認してください：

**Framework Preset**: `Other` または `Python`

**Root Directory**: `./`（そのまま）

**Build Command**: （空欄でOK）

**Output Directory**: （空欄でOK）

**Install Command**: `pip install -r requirements.txt`

### ステップ4: 環境変数を設定

「Environment Variables」セクションで、以下の環境変数を追加：

| 環境変数名 | 値 |
|----------|-----|
| `LINE_CHANNEL_ACCESS_TOKEN` | LINE Developers Consoleで取得したトークン |
| `LINE_CHANNEL_SECRET` | LINE Developers Consoleで取得したシークレット |
| `OPENAI_API_KEY` | OpenAI APIキー |

⚠️ **重要**: `PORT`環境変数は設定しないでください（Vercelが自動設定します）

### ステップ5: デプロイ

1. 「Deploy」ボタンをクリック
2. デプロイが完了するまで待つ（1〜2分）
3. デプロイが完了すると、URLが表示されます
   - 例: `https://matunaga-line-api.vercel.app`

---

## 🔗 Webhook URLの設定

デプロイが完了したら、LINE Developers ConsoleでWebhook URLを設定してください：

1. [LINE Developers Console](https://developers.line.biz/console/)にアクセス
2. チャネルを選択
3. 「Messaging API設定」タブを開く
4. 「Webhook URL」に以下を入力：
   ```
   https://あなたのVercelドメイン/callback
   ```
   **例：**
   ```
   https://matunaga-line-api.vercel.app/callback
   ```
5. 「検証」ボタンをクリックして確認
6. 「Webhookの利用」を「利用する」に設定
7. 「応答メッセージ」を「無効」に設定

---

## ✅ 動作確認

### 1. ヘルスチェック

ブラウザで以下にアクセス：
```
https://あなたのVercelドメイン/
```

以下のJSONが表示されればOK：
```json
{"status": "ok", "message": "LINE Bot is running"}
```

### 2. LINE Botでテスト

1. LINEアプリでBotにメッセージを送信
2. AIが応答することを確認

---

## 🔄 自動デプロイの設定

GitHubと連携している場合、自動デプロイが有効になっています：

- **mainブランチにプッシュ** → 本番環境に自動デプロイ
- **他のブランチにプッシュ** → プレビュー環境に自動デプロイ

---

## 🐛 トラブルシューティング

### ❌ デプロイが失敗する

**原因1: 依存関係のエラー**
- **確認**: `requirements.txt`にすべての依存関係が記載されているか
- **確認**: Vercelのログでエラーメッセージを確認

**原因2: 環境変数が設定されていない**
- **確認**: すべての環境変数が設定されているか
- **確認**: 環境変数名にタイプミスがないか

### ❌ Webhook URLの検証が失敗する

**原因1: デプロイが完了していない**
- **確認**: Vercelダッシュボードでデプロイが「Ready」になっているか
- **確認**: ヘルスチェックエンドポイント（`/`）にアクセスして動作確認

**原因2: URLが間違っている**
- **確認**: URLの最後に `/callback` が付いているか
- **確認**: `https://` で始まっているか

### ❌ メッセージを送っても応答がない

**原因1: 環境変数が設定されていない**
- **確認**: Vercelダッシュボードで環境変数を確認
- **確認**: 環境変数を変更した場合は、再デプロイが必要

**原因2: ログを確認**
- Vercelダッシュボードの「Functions」タブでログを確認
- エラーメッセージがあれば、それを解決

---

## 📊 Vercelの無料プランの制限

- **関数の実行時間**: 最大10秒（Hobbyプラン）
- **月間リクエスト数**: 100GB時間（通常の使用では十分）
- **同時実行数**: 制限あり（通常の使用では問題なし）

⚠️ **注意**: LINE Webhookは通常数秒以内に応答する必要があるため、Vercelの無料プランで問題なく動作します。

---

## 💡 カスタムドメインの設定（オプション）

1. Vercelダッシュボードでプロジェクトを選択
2. 「Settings」→「Domains」を開く
3. カスタムドメインを追加

---

## 🎉 完了！

これで、VercelでAPIが公開され、LINE Botとして動作するようになりました！

---

## 📝 参考リンク

- [Vercel公式ドキュメント](https://vercel.com/docs)
- [Vercel Pythonサポート](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python)

