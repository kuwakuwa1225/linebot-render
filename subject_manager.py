import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def register_subject(name: str, day: str, time: str, user_id: str) -> str:
    try:
        res = supabase.table("subjects").insert({
            "name": name,
            "day_of_week": day,
            "time": time,
            "user_id": user_id
        }).execute()
        return f"✅ 登録成功: {res.data}" if res.data else f"⚠️ エラー: {res.error}"
    except Exception as e:
        import traceback
        return f"❌ 例外発生:\n{traceback.format_exc()}"

def list_subjects(user_id: str) -> str:
    try:
        res = supabase.table("subjects").select("name", "day_of_week", "time").eq("user_id", user_id).execute()
        if res.data:
            subjects = [f"{s['name']} ({s['day_of_week']} {s['time']})" for s in res.data]
            return "登録されている科目一覧:\n" + "\n".join(subjects)
        else:
            return "登録されている科目はありません。"
    except Exception as e:
        return f"❌ エラー: {str(e)}"
