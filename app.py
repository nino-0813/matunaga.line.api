import os
import logging
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction
from openai import OpenAI
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

app = Flask(__name__)

# ロギング設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# LINE Botの設定
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

# OpenAI APIの設定
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# エステサロンのプロンプト設定
SYSTEM_PROMPT = """あなたは「二の腕痩せ・二の腕ケア」に特化したエステサロンのプロフェッショナルAIです。

【役割】
・二の腕の悩みを10年以上見てきたエステのプロフェッショナル
・お客さんの不安を和らげる信頼できる相談役
・専門知識を持ちながら、やさしく寄り添う

【話し方】
・1回の返信は2〜4行まで
・専門用語は使わず、わかりやすい言葉で
・やさしく、安心感のある口調
・友達すぎず、先生すぎない、ちょうど良い距離感

【会話の流れ】
1. ユーザーの質問や悩みに答える（具体的に）
2. 二の腕専門の視点から的確なアドバイスを一言
3. 回答の最後に、次のステップにつながる自然な言葉で終わる

【選択肢の提案について】
・ユーザーの質問に答えた後、2つの選択肢を提示します
・選択肢は「もっと詳しく知りたい」「別の角度から聞きたい」など、自然で興味を引くものにする
・二の腕に関連する内容で、次の会話につながるものにする

【禁止事項】
・長文説明（簡潔に）
・医療的な断定（「治る」などは言わない）
・過度な効果保証（「必ず」などは使わない）
・押し売り表現（「ぜひ」「絶対」など）
・一般的すぎる回答（専門性を持って）

【目的】
お客さんが「この人に相談してよかった」「もっと話したい」「的確にアドバイスしてくれる」と感じる会話を続けること。"""

def get_ai_response(user_message, conversation_history=[], custom_prompt=None):
    """OpenAI APIを使用してAI応答を取得"""
    try:
        prompt = custom_prompt if custom_prompt else SYSTEM_PROMPT
        messages = [
            {"role": "system", "content": prompt}
        ]
        
        # 会話履歴を追加（最近の5つのメッセージのみ）
        for history in conversation_history[-10:]:  # 直近10件
            messages.append(history)
        
        # 現在のユーザーメッセージを追加
        messages.append({"role": "user", "content": user_message})
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=200  # 2-4行の短い返答に合わせて調整
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        logger.error(f"OpenAI API エラー: {str(e)}")
        return "申し訳ございません。一時的なエラーが発生しました。しばらく経ってから再度お試しください。"

# 会話履歴を保存（実際の本番環境ではデータベースを使用することを推奨）
conversation_histories = {}

# ユーザーごとの会話回数を保存（選択肢提示回数）
user_conversation_counts = {}

# 初期挨拶メッセージ
INITIAL_GREETING = """こんにちは！二の腕専門のエステサロンです。

二の腕で気になること、なんでもお聞かせください。😊"""

# 温度が高いサイン（早期案内のトリガー）
HIGH_TEMPERATURE_SIGNS = [
    "産後からずっと", "ずっと", "何年も",
    "何をしても変わらない", "変わらない",
    "諦めかけている", "諦め",
    "ちゃんと相談したい", "相談したい",
    "本当に", "全く"
]

# 案内テンプレート
GUIDANCE_AI_DIAGNOSIS = """二の腕が気になる理由は、人によって少し違います🌱  

よければ、リッチメニューの  
『タイプ別AI診断』で  
あなたのタイプを一度整理してみてください。"""

GUIDANCE_COUNSELING = """ここまで教えてくださって、ありがとうございます☺️  

無理に何かを決める場ではなく、  
あなたの状態を整理するためのものなので、  
よければリッチメニューの  
『カウンセリングフォーム』から  
少し教えてもらえたら嬉しいです。"""

def generate_ai_options(conversation_history, conversation_count):
    """AIを使って選択肢を動的に生成（軽い質問形式）"""
    try:
        options_prompt = """あなたは二の腕専門のカウンセラーAIです。ユーザーが次に聞きたくなる「軽い質問」を2つ考えてください。

【対応できる軽い質問の例】
・産後◯年でも大丈夫？
・痛い？
・二の腕だけでいい？
・どれくらい通う？
・運動してなくても平気？

形式：以下のように、2つの質問を1行ずつ出力してください（「1.」「2.」などの番号は不要）：
質問1
質問2

【重要】
・各質問は20文字以内にしてください
・YES/NOで答えられるような軽い質問にしてください
・「予約」「申し込み」「今すぐ」という言葉は使わないでください"""
        
        # 会話履歴を含めて選択肢を生成
        messages = [
            {"role": "system", "content": options_prompt}
        ]
        
        # 最近の会話を追加（選択肢生成のコンテキストとして）
        for history in conversation_history[-6:]:
            messages.append(history)
        
        messages.append({
            "role": "user", 
            "content": f"これまでの会話を踏まえて、ユーザーが次に聞きたくなる軽い質問を2つ生成してください。"
        })
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.8,
            max_tokens=100
        )
        
        options_text = response.choices[0].message.content.strip()
        # 2行に分かれた選択肢を取得
        lines = [line.strip() for line in options_text.split('\n') if line.strip()]
        if len(lines) >= 2:
            # LINEのlabelは20文字以内に制限
            option1 = lines[0][:20] if len(lines[0]) > 20 else lines[0]
            option2 = lines[1][:20] if len(lines[1]) > 20 else lines[1]
            return [(option1, lines[0]), (option2, lines[1])]
        else:
            # フォールバック
            return [
                ("産後でも大丈夫？", "産後でも大丈夫？"),
                ("痛くない？", "痛くない？")
            ]
    except Exception as e:
        logger.error(f"選択肢生成エラー: {str(e)}")
        # フォールバック
        return [
            ("産後でも大丈夫？", "産後でも大丈夫？"),
            ("痛くない？", "痛くない？")
        ]

def check_high_temperature(user_message):
    """温度が高いサインを検知"""
    user_message_lower = user_message.lower()
    for sign in HIGH_TEMPERATURE_SIGNS:
        if sign in user_message_lower:
            return True
    return False

def determine_guidance_type(conversation_history):
    """会話の流れから、AI診断かカウンセリングフォームかを判断"""
    # 会話履歴を分析して判断（簡易版：デフォルトはカウンセリング）
    # より詳細な分析が必要な場合は、AIを使って判断することも可能
    return "counseling"  # デフォルトはカウンセリングフォーム

@app.route("/callback", methods=['POST'])
def callback():
    """LINE Webhookからのコールバックを処理"""
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """テキストメッセージを処理"""
    user_id = event.source.user_id
    user_message = event.message.text
    
    # 会話履歴を取得（存在しない場合は新規作成）
    is_new_user = user_id not in conversation_histories
    if is_new_user:
        conversation_histories[user_id] = []
        user_conversation_counts[user_id] = 0
    
    # 会話回数を取得
    conversation_count = user_conversation_counts.get(user_id, 0)
    
    logger.info(f"ユーザーID: {user_id}, メッセージ: {user_message}, 会話回数: {conversation_count}")
    
    
    # 新規ユーザーの場合、初期挨拶を送信
    if is_new_user:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=INITIAL_GREETING)
        )
        # ユーザーの最初のメッセージを会話履歴に追加（挨拶後に処理）
        conversation_histories[user_id].append({"role": "user", "content": user_message})
        # AI応答を取得
        ai_response = get_ai_response(user_message, conversation_histories[user_id])
        conversation_histories[user_id].append({"role": "assistant", "content": ai_response})
        
        # 選択肢を生成（AIで動的に）
        options = generate_ai_options(conversation_histories[user_id], conversation_count)
        quick_reply = QuickReply(items=[
            QuickReplyButton(action=MessageAction(label=opt[0], text=opt[1]))
            for opt in options
        ])
        
        line_bot_api.push_message(user_id, TextSendMessage(text=ai_response, quick_reply=quick_reply))
        user_conversation_counts[user_id] = 1
        return
    
    # ユーザーメッセージを会話履歴に追加
    conversation_histories[user_id].append({"role": "user", "content": user_message})
    
    # 温度が高いサインをチェック（2回目以降）
    if conversation_count >= 1 and check_high_temperature(user_message):
        # 温度が高い場合は、回数に関係なく案内へ進む
        guidance_type = determine_guidance_type(conversation_histories[user_id])
        if guidance_type == "diagnosis":
            guidance_message = GUIDANCE_AI_DIAGNOSIS
        else:
            guidance_message = GUIDANCE_COUNSELING
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=guidance_message)
        )
        # リセット
        user_conversation_counts[user_id] = 0
        conversation_histories[user_id] = []
        return
    
    # 4往復（会話回数4回）が終わった場合、案内へ進む
    if conversation_count >= 4:
        guidance_type = determine_guidance_type(conversation_histories[user_id])
        if guidance_type == "diagnosis":
            guidance_message = GUIDANCE_AI_DIAGNOSIS
        else:
            guidance_message = GUIDANCE_COUNSELING
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=guidance_message)
        )
        # リセット
        user_conversation_counts[user_id] = 0
        conversation_histories[user_id] = []
        return
    
    # AI応答を取得
    ai_response = get_ai_response(user_message, conversation_histories[user_id])
    
    # 会話履歴を更新
    conversation_histories[user_id].append({"role": "assistant", "content": ai_response})
    
    # 会話回数を増やす
    user_conversation_counts[user_id] = conversation_count + 1
    
    # 選択肢を生成（軽い質問形式）
    options = generate_ai_options(conversation_histories[user_id], user_conversation_counts[user_id])
    quick_reply = QuickReply(items=[
        QuickReplyButton(action=MessageAction(label=opt[0], text=opt[1]))
        for opt in options
    ])
    
    # 会話履歴が長すぎる場合は古いものを削除（最新30件を保持）
    if len(conversation_histories[user_id]) > 30:
        conversation_histories[user_id] = conversation_histories[user_id][-30:]
    
    # LINEに返信（選択肢付き）
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=ai_response, quick_reply=quick_reply)
    )

@app.route("/", methods=['GET'])
def health_check():
    """ヘルスチェック用エンドポイント"""
    return {"status": "ok", "message": "LINE Bot is running"}

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

