import os
import datetime
from supabase import create_client
from linebot import LineBotApi

# 環境変数から読み込み
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

# 初期化
supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

# 曜日（日本語）
weekdays = ["月", "火", "水", "木", "金", "土", "日"]
today = weekdays[datetime.datetime.now().weekday()]
now = datetime.datetime.now().strftime("%H:%M")

def notify():
    try:
        res = supabase.table("subjects")\
            .select("name, user_id")\
            .eq("day_of_week", today)\
            .eq("time", now + ":00")\
            .execute()
        
        for item in res.data:
            line_bot_api.push_message(
                item["user_id"],
                {"type": "text", "text": f"⏰ リマインダー\n科目: {item['name']}"}
            )
            print(f"通知送信: {item['name']} to {item['user_id']}")

    except Exception as e:
        print("通知失敗:", e)

notify()
