import os
from supabase import create_client

SUPABASE_URL = os.getenv("https://mtmlxanzhctzufhraxhy.supabase.co")
SUPABASE_API_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im10bWx4YW56aGN0enZmaHJheGh5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDk3MDIzNzEsImV4cCI6MjA2NTI3ODM3MX0.t2wfk9LwDFK1tuO9MrVhvFvi6frzgyor2FzMalEpsZo")

supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def register_subject(subject_name: str) -> str:
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
