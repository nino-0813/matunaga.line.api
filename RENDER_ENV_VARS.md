# Render環境変数設定一覧

## 📋 必須の環境変数

Renderダッシュボードの **Environment** セクションで、以下の環境変数を設定してください。

### 1. LINE_CHANNEL_ACCESS_TOKEN
- **説明**: LINE Developers Consoleから取得したチャネルアクセストークン
- **取得方法**: 
  1. [LINE Developers Console](https://developers.line.biz/console/)にアクセス
  2. チャネルを選択
  3. 「Messaging API設定」タブ → 「チャネルアクセストークン（長期）」をコピー
- **値の例**: `AbCdEf1234567890...`
- **必須**: ✅ はい

---

### 2. LINE_CHANNEL_SECRET
- **説明**: LINE Developers Consoleから取得したチャネルシークレット
- **取得方法**:
  1. LINE Developers Console → チャネルを選択
  2. 「Messaging API設定」タブ → 「チャネルシークレット」をコピー
- **値の例**: `1234567890abcdef1234567890abcdef`
- **必須**: ✅ はい

---

### 3. OPENAI_API_KEY
- **説明**: OpenAI Platformから取得したAPIキー
- **取得方法**:
  1. [OpenAI Platform](https://platform.openai.com/)にアクセス
  2. 「API keys」→ 「Create new secret key」
  3. 生成されたキーをコピー（一度しか表示されません）
- **値の例**: `sk-1234567890abcdef...`
- **必須**: ✅ はい

---

## 🔧 推奨の環境変数

### 4. PYTHON_VERSION
- **説明**: Pythonのバージョンを指定（aiohttpの互換性のため）
- **値**: `3.11.0`
- **必須**: ⚠️ Python 3.13のエラーが出る場合は必須
- **注意**: `runtime.txt`で設定していますが、エラーが出る場合は環境変数でも設定してください

---

## 📝 オプションの環境変数

### 5. PORT
- **説明**: アプリケーションが使用するポート番号
- **値**: `8080`（デフォルト）
- **必須**: ❌ いいえ（Renderが自動的に設定します）
- **注意**: 通常は設定不要です

---

## 🎯 設定手順（Renderダッシュボード）

1. Renderダッシュボードでサービスを開く
2. 左側のメニューから **「Environment」** をクリック
3. 「Add Environment Variable」ボタンをクリック
4. 各環境変数を追加：
   - **Key**: 環境変数名（例: `LINE_CHANNEL_ACCESS_TOKEN`）
   - **Value**: 値（トークンやキー）
5. 「Save Changes」をクリック
6. すべての環境変数を追加したら、**「Manual Deploy」→「Deploy latest commit」** を実行

---

## ✅ チェックリスト

デプロイ前に、以下の環境変数がすべて設定されているか確認してください：

- [ ] `LINE_CHANNEL_ACCESS_TOKEN`
- [ ] `LINE_CHANNEL_SECRET`
- [ ] `OPENAI_API_KEY`
- [ ] `PYTHON_VERSION`（エラーが出る場合のみ）

---

## 🔒 セキュリティ注意事項

- ⚠️ **環境変数は絶対にGitHubにプッシュしないでください**
- ⚠️ `.env`ファイルは`.gitignore`に含まれています
- ⚠️ APIキーやトークンは他人と共有しないでください
- ⚠️ 定期的にトークンやキーを更新することを推奨します

---

## 📝 値の取得先まとめ

| 環境変数 | 取得先URL |
|---------|----------|
| LINE_CHANNEL_ACCESS_TOKEN | https://developers.line.biz/console/ |
| LINE_CHANNEL_SECRET | https://developers.line.biz/console/ |
| OPENAI_API_KEY | https://platform.openai.com/api-keys |

---

## 🐛 トラブルシューティング

### 環境変数が反映されない場合
1. 「Save Changes」をクリックしたか確認
2. 「Manual Deploy」を実行して再デプロイ
3. ログを確認してエラーメッセージをチェック

### 環境変数の値が間違っている場合
- LINE Developers Consoleでトークンが有効か確認
- OpenAI APIキーが有効か確認
- スペースや改行が入っていないか確認

