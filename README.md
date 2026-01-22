# 二の腕エステサロン LINE Bot（ChatGPT連携）

LINE公式アカウントとChatGPT APIを使用した、二の腕エステサロンの受付チャットAIです。

## 機能

- LINE Messaging APIとの連携
- OpenAI（ChatGPT）APIを使用した自然な会話
- エステサロンの受付・サポートに特化したプロンプト設定
- 会話履歴の保持（メモリ機能）

## セットアップ手順

### 1. 必要なアカウントとAPIキーの取得

#### LINE Developers アカウント
1. [LINE Developers](https://developers.line.biz/ja/)にアクセス
2. プロバイダーを作成
3. チャネルを作成（Messaging APIチャネル）
4. チャネルアクセストークンとチャネルシークレットを取得

#### OpenAI アカウント
1. [OpenAI Platform](https://platform.openai.com/)にアクセス
2. アカウントを作成
3. APIキーを生成・取得

### 2. プロジェクトのセットアップ

```bash
# 仮想環境を作成（推奨）
python3 -m venv venv

# 仮想環境を有効化
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 依存関係をインストール
pip install -r requirements.txt
```

### 3. 環境変数の設定

`.env.example`を`.env`にコピーし、実際の値を設定してください：

```bash
cp .env.example .env
```

`.env`ファイルを編集：

```env
LINE_CHANNEL_ACCESS_TOKEN=取得したチャネルアクセストークン
LINE_CHANNEL_SECRET=取得したチャネルシークレット
OPENAI_API_KEY=取得したOpenAI APIキー
PORT=5000
```

### 4. アプリケーションの起動

```bash
python app.py
```

アプリケーションは `http://localhost:5000` で起動します。

### 5. LINE Webhook URLの設定

1. [LINE Developers Console](https://developers.line.biz/console/)にアクセス
2. 作成したチャネルを選択
3. 「Messaging API設定」タブを開く
4. Webhook URLを設定: `https://あなたのドメイン/callback`
5. Webhookの利用を有効化

**ローカル開発時:**
- [ngrok](https://ngrok.com/)などのツールを使用してローカルサーバーを公開
- 例: `ngrok http 5000`
- 生成されたURL（例: `https://xxxx.ngrok.io/callback`）をWebhook URLに設定

### 6. LINE Botへの友達追加

1. LINE Developers ConsoleでQRコードを取得
2. スマートフォンでQRコードをスキャンして友達追加

## カスタマイズ

### プロンプトの変更

`app.py`の`SYSTEM_PROMPT`変数を編集することで、AIの応答内容をカスタマイズできます。

```python
SYSTEM_PROMPT = """あなたは二の腕エステサロンの親切で丁寧な受付スタッフです。
...（プロンプト内容）
"""
```

### 営業時間やサービスの変更

`SYSTEM_PROMPT`内のサロン情報を実際の情報に合わせて更新してください。

## デプロイ

### Heroku

1. Herokuアカウントを作成
2. Heroku CLIをインストール
3. 以下のコマンドを実行：

```bash
heroku create your-app-name
heroku config:set LINE_CHANNEL_ACCESS_TOKEN=your_token
heroku config:set LINE_CHANNEL_SECRET=your_secret
heroku config:set OPENAI_API_KEY=your_key
git push heroku main
```

### その他のクラウドサービス

- AWS Lambda + API Gateway
- Google Cloud Run
- Azure App Service
- VPS（Nginx + Gunicorn）

## 注意事項

- 本番環境では、会話履歴の保存にデータベース（PostgreSQL、MongoDBなど）を使用することを推奨します
- APIキーは絶対に公開しないでください（`.env`を`.gitignore`に含めることを確認）
- OpenAI APIの利用には料金が発生します
- LINE Messaging APIにも利用制限があります

## トラブルシューティング

### Webhookエラー
- LINE Developers ConsoleでWebhook URLが正しく設定されているか確認
- SSL証明書が必要です（https://で始まるURLを使用）

### OpenAI APIエラー
- APIキーが正しく設定されているか確認
- 利用制限やクレジット残高を確認

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

