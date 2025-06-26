import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def register_subject(subject_name: str) -> str:
    if not subject_name:
        return "科目名を入力してください。"
    try:
        res = supabase.table("subjects").insert({"name": subject_name}).execute()
        return f"✅ 登録成功: {res.data}" if res.data else f"⚠️ ステータス: {res.status_code}, エラー: {res.error}"
    except Exception as e:
        return f"❌ 例外発生: {str(e)}"

def list_subjects() -> str:
    try:
        response = supabase.table("subjects").select("name").execute()
        if response.data:
            subjects = [item["name"] for item in response.data]
            return "登録されている科目一覧:\n" + "\n".join(subjects)
        else:
            return "登録されている科目はありません。"
    except Exception as e:
        return f"❌ 科目一覧取得エラー: {e}"
