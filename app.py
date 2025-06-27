from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from subject_manager import register_subject, list_subjects  # ← 追加

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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    user_id = event.source.user_id  # ← 追加

    if text.startswith("科目登録"):
        subject_name = text.replace("科目登録", "").strip()
        response = register_subject(subject_name, user_id)  # ← 引数追加
    elif text == "科目一覧":
        response = list_subjects(user_id)  # ← 引数追加
    else:
        response = f"あなたのメッセージ: {text}"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response)
    )
def parse_register_command(text: str):
    try:
        _, name, day, time = text.strip().split()
        return name, day, time
    except:
        return None, None, None



if __name__ == "__main__":
    app.run()
