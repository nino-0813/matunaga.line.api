# Renderでのデプロイ手順

## 前提条件
- GitHubリポジトリ: https://github.com/nino-0813/matunaga.ai.api
- Renderアカウント（無料で作成可能）

## ステップ1: Renderアカウントの作成

1. https://render.com にアクセス
2. "Get Started for Free" をクリック
3. GitHubアカウントでサインアップ（推奨）

## ステップ2: 新しいWebサービスの作成

1. Renderダッシュボードで "New +" ボタンをクリック
2. "Web Service" を選択
3. GitHubリポジトリを接続:
   - "Connect account" をクリック（初回のみ）
   - GitHubの認証を許可
   - リポジトリ `nino-0813/matunaga.ai.api` を選択

## ステップ3: サービスの設定

### 基本設定
- **Name**: `matunaga-ai-api`（任意の名前）
- **Region**: `Singapore`（日本に近い）
- **Branch**: `main`
- **Root Directory**: （空白のまま）
- **Runtime**: `Python 3`（自動的に`runtime.txt`のバージョンを使用）
- **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
- **Start Command**: `python app.py`

### 環境変数の設定

"Environment" セクションで以下の環境変数を追加：

1. **LINE_CHANNEL_ACCESS_TOKEN**
   - 値: LINE Developers Consoleから取得したチャネルアクセストークン

2. **LINE_CHANNEL_SECRET**
   - 値: LINE Developers Consoleから取得したチャネルシークレット

3. **OPENAI_API_KEY**
   - 値: OpenAI Platformから取得したAPIキー

4. **PORT**
   - 値: `8080`（Renderが自動的に設定するため、設定不要でもOK）

### プランの選択
- **Free** を選択（無料プラン）
  - 注意: 無料プランは15分間アクセスがないとスリープします
  - スリープから復帰するまで数秒かかります

## ステップ4: デプロイ

1. "Create Web Service" をクリック
2. デプロイが開始されます（数分かかります）
3. デプロイが完了すると、URLが表示されます
   - 例: `https://matunaga-ai-api.onrender.com`

## ステップ5: LINE Webhook URLの設定

1. [LINE Developers Console](https://developers.line.biz/console/) にアクセス
2. チャネルを選択
3. 「Messaging API設定」タブを開く
4. 「Webhook URL」に以下のURLを設定:
   ```
   https://あなたのサービス名.onrender.com/callback
   ```
   例: `https://matunaga-ai-api.onrender.com/callback`
5. 「検証」ボタンをクリックして接続を確認
6. 「Webhookの利用」を「利用する」に変更
7. 「応答メッセージ」を「無効」に変更（AIが応答するため）

## ステップ6: 動作確認

1. LINEアプリでBotにメッセージを送信
2. 正常に応答することを確認

## トラブルシューティング

### デプロイエラーが発生する場合

1. **ログを確認**
   - Renderダッシュボードの "Logs" タブを確認
   - エラーメッセージを確認

2. **よくあるエラー**
   - **環境変数が設定されていない**: Environmentセクションで確認
   - **依存関係のエラー**: `requirements.txt` を確認
   - **ポートのエラー**: `PORT` 環境変数が正しく設定されているか確認

### スリープについて

無料プランでは、15分間アクセスがないとスリープします。
- スリープからの復帰には数秒かかります
- 定期的にアクセスがあるとスリープしません

### スリープを防ぐ方法（オプション）

1. **有料プランにアップグレード**（$7/月）
2. **外部サービスで定期アクセス**（UptimeRobotなど）

## 次のステップ

- コードを更新したら、GitHubにプッシュするだけで自動的に再デプロイされます
- 環境変数を変更した場合は、Renderダッシュボードから変更し、再デプロイが必要です

