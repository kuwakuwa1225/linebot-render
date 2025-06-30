import os
from supabase import create_client
from linebot import LineBotApi
from datetime import datetime
import pytz

# 日本時間に変換
jst = pytz.timezone("Asia/Tokyo")
now_jst = datetime.now(jst)
today = ["月", "火", "水", "木", "金", "土", "日"][now_jst.weekday()]
now_time = now_jst.strftime("%H:%M")

# 環境変数の取得
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

# SupabaseとLINE Botの初期化
supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

def notify():
    try:
        # Supabaseから今日・今の時間のデータを取得
        res = supabase.table("subjects")\
            .select("name, user_id")\
            .eq("day_of_week", today)\
            .eq("time", now_time + ":00")\
            .execute()

        # ヒットしたデータに通知送信
        for item in res.data:
            line_bot_api.push_message(
                item["user_id"],
                {"type": "text", "text": f"⏰ リマインダー\n科目: {item['name']}"}
            )
            print(f"✅ 通知送信: {item['name']} → {item['user_id']}")
            
    except Exception as e:
        print(f"❌ 通知失敗: {e}")

# 実行
notify()
