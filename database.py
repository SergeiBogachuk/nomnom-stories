def save_story(story_data):
    # Убираем аудио из данных, если оно там есть, чтобы не злить базу
    data_to_save = {k: v for k, v in story_data.items() if k != 'audio_base64'}
    try:
        res = supabase.table("stories").insert(data_to_save).execute()
        return res
    except Exception as e:
        print(f"Ошибка в database.py: {e}")
        return None
