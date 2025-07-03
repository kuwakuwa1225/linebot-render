from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from subject_manager import register_subject, list_subjects, delete_subject  # ← ここ追加

import os

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

def parse_register_command(text: str):
    try:
        _, name, day, time = text.strip().split()
        return name, day, time
    except:
        return None, None, None

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    user_id = event.source.user_id

    if text.startswith("科目登録"):
        name, day, time = parse_register_command(text)
        if not all([name, day, time]):
            response = "❌ 登録形式: 科目登録 科目名 曜日 時間（例：科目登録 数学 火 14:30）"
        else:
            response = register_subject(name, day, time, user_id)

    elif text == "科目一覧":
        response = list_subjects(user_id)

    elif text.startswith("科目削除"):
        name = text.replace("科目削除", "").strip()
        if not name:
            response = "❌ 削除形式: 科目削除 科目名（例：科目削除 数学）"
        else:
            response = delete_subject(name, user_id)

    else:
        response = f"あなたのメッセージ: {text}"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response)
    )

if __name__ == "__main__":
    app.run()
