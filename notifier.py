import os
import datetime
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from supabase import create_client
from linebot import LineBotApi
from dotenv import load_dotenv

load_dotenv()

# 環境変数
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

# SupabaseとLINE初期化
supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

# 曜日対応（日本語 → Pythonのweekday()値に合わせる）
weekdays = ["月", "火", "水", "木", "金", "土", "日"]
today = lambda: weekdays[datetime.datetime.now().weekday()]
now_time = lambda: datetime.datetime.now().strftime("%H:%M")

def notify_subjects():
    today_str = today()
    time_str = now_time()

    print(f"チェック中: {today_str} {time_str}")

    try:
        # Supabaseから対象の授業を取得
        res = supabase.table("subjects")\
            .select("name, user_id")\
            .eq("day_of_week", today_str)\
            .eq("time", time_str + ":00")\
            .execute()

        for item in res.data:
            try:
                line_bot_api.push_message(
                    item["user_id"],
                    {"type": "text", "text": f"⏰ 時間になりました！\n科目: {item['name']}"}
                )
                print(f"通知送信: {item['user_id']} に {item['name']}")
            except Exception as e:
                print(f"通知失敗: {e}")

    except Exception as e:
        print(f"エラー: {e}")

# 毎分実行
scheduler = BlockingScheduler()
scheduler.add_job(notify_subjects, 'cron', minute='*')
scheduler.start()
