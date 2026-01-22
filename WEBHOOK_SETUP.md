# LINE Webhook URL設定手順

## 📍 Webhook URL

RenderのサービスURLに `/callback` を追加したURLを設定してください。

### あなたのWebhook URL

```
https://matunaga-ai-api-1.onrender.com/callback
```

---

## 📝 設定手順

1. [LINE Developers Console](https://developers.line.biz/console/)にアクセス
2. チャネルを選択（Messaging APIチャネル）
3. 左側のメニューから「Messaging API設定」タブを開く
4. 「Webhook URL」セクションをスクロールして表示
5. 「Webhook URL」欄に以下のURLを入力：
   ```
   https://matunaga-ai-api-1.onrender.com/callback
   ```
6. **検証前にサービスを起動させる**（重要！）
   - ブラウザで `https://matunaga-ai-api-1.onrender.com/` にアクセス
   - サービスが起動するまで30秒〜1分待つ
7. 「検証」ボタンをクリック
   - ✅ **成功**: 「Webhook URLの検証に成功しました」と表示される
   - ❌ **タイムアウトエラー**: サービスがスリープしている可能性があります（後述のトラブルシューティングを参照）
7. 「Webhookの利用」を「利用する」に変更
8. 「応答メッセージ」を「無効」に変更（AIが応答するため）

---

## ✅ 設定後の確認

### 正常に動作しているか確認

1. LINEアプリでBotにメッセージを送信
2. AIが応答することを確認

### Webhook送信の確認

LINE Developers Consoleの「Messaging API設定」タブで：
- 「Webhook送信」が「送信」になっていることを確認
- メッセージを送信すると、「Webhook送信」の回数が増えることを確認

---

## 🐛 トラブルシューティング

### 「検証」ボタンでエラーが出る場合

1. **Renderサービスが起動しているか確認**
   - Renderダッシュボードでサービスが「Live」になっているか確認
   - ログにエラーがないか確認

2. **URLが正しいか確認**
   - 最後に `/callback` が付いているか確認
   - `https://` で始まっているか確認
   - スペースや余分な文字が入っていないか確認

3. **サービスがスリープしていないか確認**
   - 無料プランでは15分間アクセスがないとスリープします
   - スリープから復帰するまで数秒かかります
   - 一度アクセスしてから検証を試してください

4. **ポートが正しく設定されているか確認**
   - アプリケーションがポート8080で起動しているか確認
   - Renderのログで「Running on port 8080」と表示されているか確認

### メッセージを送っても応答がない場合

1. **環境変数が正しく設定されているか確認**
   - `LINE_CHANNEL_ACCESS_TOKEN`
   - `LINE_CHANNEL_SECRET`
   - `OPENAI_API_KEY`
   - すべて設定されているか確認

2. **Renderのログを確認**
   - エラーメッセージがないか確認
   - Webhookが受信されているか確認

3. **「応答メッセージ」が無効になっているか確認**
   - LINE Developers Consoleで「応答メッセージ」を「無効」に設定

---

## 📌 重要なポイント

- ⚠️ Webhook URLは必ず `/callback` で終わる必要があります
- ⚠️ サービスURLが変更された場合は、Webhook URLも更新が必要です
- ⚠️ Renderの無料プランでは、スリープからの復帰に時間がかかることがあります

---

## 🔄 URLが変更された場合

Renderでサービスを削除・再作成した場合など、URLが変更された場合は：
1. 新しいURLを確認（Renderダッシュボードで確認）
2. LINE Developers ConsoleでWebhook URLを新しいURLに更新
3. 「検証」ボタンで確認

