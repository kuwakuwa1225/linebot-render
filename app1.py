from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# ユーザーごとの科目リスト（メモリ上、Render再起動で消えるので要DB移行検討）
user_subjects = {}

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
    user_id = event.source.user_id
    text = event.message.text.strip()

    if text.startswith("科目登録 "):
        subject = text[len("科目登録 "):].strip()
        if user_id not in user_subjects:
            user_subjects[user_id] = []
        user_subjects[user_id].append(subject)
        reply = f"科目「{subject}」を登録しました！"
    elif text == "科目一覧":
        subjects = user_subjects.get(user_id, [])
        if subjects:
            reply = "登録中の科目一覧：\n" + "\n".join(subjects)
        else:
            reply = "まだ科目が登録されていません。"
    else:
        reply = "「科目登録 [科目名]」か「科目一覧」で操作してください。"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    app.run()
