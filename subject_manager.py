# subject_manager.py

subjects = []

def register_subject(subject_name):
    subjects.append(subject_name)
    return f"科目「{subject_name}」を登録しました。"

def list_subjects():
    if not subjects:
        return "まだ科目が登録されていません。"
    return "登録された科目:\n" + "\n".join(f"{i+1}. {s}" for i, s in enumerate(subjects))

