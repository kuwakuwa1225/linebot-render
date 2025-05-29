# subject_manager.py
user_subjects = {}

def register_subject(user_id, subject):
    if user_id not in user_subjects:
        user_subjects[user_id] = []
    user_subjects[user_id].append(subject)
    return f"科目「{subject}」を登録しました！"

def list_subjects(user_id):
    subjects = user_subjects.get(user_id, [])
    if subjects:
        return "登録中の科目一覧：\n" + "\n".join(subjects)
    else:
        return "まだ科目が登録されていません。"

