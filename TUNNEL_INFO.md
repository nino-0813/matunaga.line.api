# トンネル情報

## 現在のWebhook URL

**Webhook URL**: `https://nat-kim-joke-todd.trycloudflare.com/callback`

## LINE Developers Consoleでの設定手順

1. [LINE Developers Console](https://developers.line.biz/console/) にアクセス
2. 作成したチャネルを選択
3. 「Messaging API設定」タブを開く
4. 「Webhook URL」欄に以下のURLを入力：
   ```
   https://nat-kim-joke-todd.trycloudflare.com/callback
   ```
5. 「検証」ボタンをクリックして接続を確認
6. 「Webhookの利用」を「利用する」に変更
7. 「応答メッセージ」を「無効」に変更（AIが応答するため）

## 注意事項

- Cloudflare TunnelのURLは起動のたびに変わります
- トンネルを再起動した場合は、新しいURLをLINE Developers Consoleに設定し直してください
- トンネルを停止すると、Webhookが機能しなくなります

## トンネルの停止・再起動

```bash
# 停止
pkill -f cloudflared

# 再起動（新しいURLが生成されます）
cloudflared tunnel --url http://localhost:8080
```

## 現在の状態

- ローカルサーバー: http://localhost:8080
- 公開URL: https://nat-kim-joke-todd.trycloudflare.com
- Webhook URL: https://nat-kim-joke-todd.trycloudflare.com/callback

