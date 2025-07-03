import os
from supabase import create_client

# Supabase 接続設定（環境変数から取得）
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

# 科目を登録する関数
def register_subject(name: str, day: str, time: str, user_id: str) -> str:
    if not all([name, day, time, user_id]):
        return "⚠️ 科目名・曜日・時間・ユーザーIDのすべてを指定してください。"

    try:
        res = supabase.table("subjects").insert({
            "name": name,
            "day_of_week": day,
            "time": time,
            "user_id": user_id
        }).execute()

        if res.data:
            return f"✅ 科目「{name}」を登録しました。"
        else:
            return "⚠️ 科目の登録に失敗しました。"
    except Exception:
        return "❌ 科目の登録中にエラーが発生しました。"

# ユーザーごとの科目一覧を取得する関数
def list_subjects(user_id: str) -> str:
    if not user_id:
        return "⚠️ ユーザーIDが指定されていません。"

    try:
        res = supabase.table("subjects") \
            .select("name", "day_of_week", "time") \
            .eq("user_id", user_id).execute()

        if res.data:
            subjects = [f"{s['name']}（{s['day_of_week']} {s['time']}）" for s in res.data]
            return "📚 登録されている科目一覧:\n" + "\n".join(subjects)
        else:
            return "📭 登録されている科目はありません。"
    except Exception:
        return "❌ 科目一覧の取得中にエラーが発生しました。"
