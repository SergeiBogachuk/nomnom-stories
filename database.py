import os
from supabase import create_client

# Твои данные подключения (прописаны напрямую, чтобы не было ошибок)
SUPABASE_URL = "https://gdyhmeshafpdttzjpxjg.supabase.co"
SUPABASE_KEY = "sb_publishable_aqJsR96WyEdflsb4LoQSzg_g2WEyWBd"

# Инициализация клиента
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class _EmptyResult:
    """Объект для возврата пустого результата, если запрос не удался."""
    data = []

def check_user(email, password):
    try:
        res = supabase.table("users").select("*").eq("email", email).eq("password", password).execute()
        return len(res.data) > 0
    except Exception as e:
        print(f"Ошибка в check_user: {e}")
        return False

def get_user_stories(email):
    try:
        return supabase.table("stories").select("*").eq("user_email", email).order("id", desc=True).execute()
    except Exception as e:
        print(f"Ошибка в get_user_stories: {e}")
        return _EmptyResult()

def save_story(story_data):
    # Убираем аудио из данных перед первым сохранением (обход ошибки PGRST204)
    data_to_save = {k: v for k, v in story_data.items() if k != 'audio_base64'}
    try:
        res = supabase.table("stories").insert(data_to_save).execute()
        return res
    except Exception as e:
        print(f"Ошибка в save_story (database.py): {e}")
        return None

def update_audio(story_id, audio_b64):
    try:
        # Точечное обновление колонки аудио по ID сказки
        res = supabase.table("stories").update({"audio_base64": audio_b64}).eq("id", story_id).execute()
        return res
    except Exception as e:
        print(f"Ошибка в update_audio: {e}")
        return None

def delete_story(story_id):
    try:
        supabase.table("stories").delete().eq("id", story_id).execute()
        return True
    except Exception as e:
        print(f"Ошибка при удалении: {e}")
        return False
