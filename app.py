from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("ZyXgdJ6lWQoSUFbGn7lKCybo+lRzDxpWvNjRBobYFEMXgnuSXetSELF55G4bB9uxJ5sXCy4ej5sax5+dgHk6tEoszp1G8pWe8gB9BQKBMVJDHrERUz35mcFSBVrA1a/WwfvT7XJvb0cQ9V1PTn+oAwdB04t89/1O/w1cDnyilFU="))
handler = WebhookHandler(os.getenv("2b3e83216a69c25ba3a94db83a5e631d"))

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
    message = event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"あなたのメッセージ：{message}")
    )

if __name__ == "__main__":
    app.run()
