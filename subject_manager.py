import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")


supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def register_subject(subject_name: str) -> str:
    try:
        response = supabase.table("subjects").insert({"name": subject_name}).execute()
        return f"DEBUG: status={response.status_code}, data={response.data}, error={response.error}"
    except Exception as e:
        return f"登録エラー: {e}"

    if not subject_name:
        return "科目名を入力してください。"
    # subjectsテーブルに挿入
    response = supabase.table("subjects").insert({"name": subject_name}).execute()
    if response.status_code in (200, 201):
        return f"科目「{subject_name}」を登録しました。"
    else:
        return "科目登録に失敗しました。"

def list_subjects() -> str:
    response = supabase.table("subjects").select("name").execute()
    if response.data:
        subjects = [item["name"] for item in response.data]
        return "登録されている科目一覧:\n" + "\n".join(subjects)
    else:
        return "登録されている科目はありません。"
