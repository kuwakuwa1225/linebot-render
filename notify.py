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

# JSTの現在時刻を取得
jst = pytz.timezone("Asia/Tokyo")
now = datetime.now(jst)

# 英語の曜日を1文字日本語に変換
weekday_map = {
    "Monday": "月",
    "Tuesday": "火",
    "Wednesday": "水",
    "Thursday": "木",
    "Friday": "金",
    "Saturday": "土",
    "Sunday": "日"
}
current_weekday_eng = now.strftime("%A")
current_weekday = weekday_map[current_weekday_eng]

# Supabaseから今日の予定を取得
res = supabase.table("subjects") \
    .select("*") \
    .eq("day_of_week", current_weekday) \
    .execute()

subjects = res.data or []

# ±10分以内の予定だけ通知
for subject in subjects:
    try:
        subject_time_str = subject["time"]  # 例: "11:30:00"
        subject_time = datetime.strptime(subject_time_str, "%H:%M:%S").replace(
            year=now.year, month=now.month, day=now.day, tzinfo=jst
        )

        print(f"[DEBUG] チェック中: {subject['name']} at {subject_time_str}")
        print(f"[DEBUG] 差分: {abs((subject_time - now).total_seconds())}秒")

        if abs((subject_time - now).total_seconds()) <= 600:
            user_id = subject["user_id"]
            name = subject["name"]
            message = f"⏰ もうすぐ「{name}」の授業です！（{subject_time_str}）"
            line_bot_api.push_message(user_id, TextSendMessage(text=message))

    except Exception as e:
        print("❌ 通知エラー:", e)
        
print(f"[DEBUG] 現在の曜日: {current_weekday}, 現在時刻: {now.strftime('%H:%M')}")
print(f"[DEBUG] Supabaseから{len(subjects)}件の科目を取得")
