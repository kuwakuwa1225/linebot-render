from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from subject_manager import register_subject, list_subjects, delete_subject

import os

app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# ステップ登録用の状態管理
user_states = {}

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
    text = event.message.text.strip()
    user_id = event.source.user_id

    state = user_states.get(user_id)

    if text == "科目一覧":
        response = list_subjects(user_id)

    elif text.startswith("科目削除"):
        name = text.replace("科目削除", "").strip()
        if not name:
            response = "❌ 削除形式: 科目削除 科目名（例：科目削除 数学）"
        else:
            response = delete_subject(name, user_id)

    elif text == "科目登録":
        user_states[user_id] = {"step": "name", "data": {}}
        response = "📘 科目名を入力してください："

    elif state:
        step = state["step"]
        data = state["data"]

        if step == "name":
            data["name"] = text
            state["step"] = "day"
            response = "🗓️ 曜日を入力してください（例：月）："

        elif step == "day":
            data["day"] = text
            state["step"] = "time"
            response = "⏰ 時間を入力してください（例：14:30）："

        elif step == "time":
            data["time"] = text
            state["step"] = "classroom"
            response = "🏫 教室を入力してください（例：A101）："

        elif step == "classroom":
            data["classroom"] = text
            response = register_subject(
                name=data["name"],
                day=data["day"],
                time=data["time"],
                classroom=data["classroom"],
                user_id=user_id
            )
            user_states.pop(user_id)

        else:
            response = "⚠️ 不明な状態です。もう一度「科目登録」と送ってください。"
    else:
        response = "❓ コマンドが認識されません。「科目登録」「科目削除」「科目一覧」を試してください。"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response)
    )

if __name__ == "__main__":
    app.run()
