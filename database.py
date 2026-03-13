from supabase import create_client

# Твои ключи Supabase
URL = "https://gdyhmeshafpdttzjpxjg.supabase.co"
KEY = "sb_publishable_aqJsR96WyEdflsb4LoQSzg_g2WEyWBd"
supabase = create_client(URL, KEY)

def check_user(email, password):
    """Проверка логина и пароля"""
    res = supabase.table("users").select("*").eq("email", email).eq("password", password).execute()
    return res.data

def get_user_stories(email):
    """Загрузка списка всех сказок пользователя"""
    return supabase.table("stories").select("*").eq("user_email", email).order("created_at", desc=True).execute()

def save_story(data):
    """Сохранение новой сказки"""
    return supabase.table("stories").insert(data).execute()

def update_audio(story_id, audio_b64):
    """Сохранение аудио в базу для экономии баллов ElevenLabs"""
    return supabase.table("stories").update({"audio_base64": audio_b64}).eq("id", story_id).execute()

def delete_story(story_id):
    """Удаление сказки по ID (Корзинка)"""
    return supabase.table("stories").delete().eq("id", story_id).execute()
