from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

from subject_manager import register_subject, list_subjects  # 追加

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
    user_id = event.source.user_id
    text = event.message.text.strip()

    if text.startswith("科目登録 "):
        subject = text[len("科目登録 "):].strip()
        reply = register_subject(user_id, subject)  # 呼び出し
    elif text == "科目一覧":
        reply = list_subjects(user_id)  # 呼び出し
    else:
        reply = "「科目登録 [科目名]」か「科目一覧」で操作してください。"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # RenderがPORTを環境変数で指定
    app.run(host="0.0.0.0", port=port)


