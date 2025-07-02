from datetime import datetime, timedelta
import pytz
import os
from supabase import create_client
from linebot import LineBotApi
from linebot.models import TextSendMessage

# 環境変数の取得
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

# 現在の JST 時刻
jst = pytz.timezone("Asia/Tokyo")
now = datetime.now(jst)
current_weekday = now.strftime("%A")

# 10分後の時刻を計算（＝予定時間が「10分後」なら通知）
target_time = (now + timedelta(minutes=10)).strftime("%H:%M")

# 条件に一致する行を検索
res = supabase.table("subjects") \
    .select("*") \
    .eq("day", current_weekday) \
    .eq("time", target_time) \
    .execute()

subjects = res.data or []

# 通知を送信
for subject in subjects:
    try:
        user_id = subject["user_id"]
        name = subject["name"]
        time = subject["time"]
        message = f"⏰ まもなく {time} から「{name}」の授業です！"
        line_bot_api.push_message(user_id, TextSendMessage(text=message))
    except Exception as e:
        print("❌ LINE通知失敗:", e)
