import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def register_subject(subject_name: str) -> str:
    if not subject_name:
        return "科目名を入力してください。"
    
    # Supabaseの 'subjects' テーブルに挿入
    response = supabase.table("subjects").insert({"name": subject_name}).execute()
    if response.status_code == 201 or response.status_code == 200:
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
# subject_manager.py

