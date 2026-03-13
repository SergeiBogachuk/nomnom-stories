import streamlit as st
from openai import OpenAI
import requests
import base64

# Инициализация клиента OpenAI (мозги GPT-5.3)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_story_text(child_name, lang, skills, details, time_val):
    """Генерирует длинную сказку по главам"""
    num_chapters = 1 if time_val <= 3 else (2 if time_val <= 5 else 3)
    full_text = ""
    model = "gpt-5.3-chat-latest"
    
    for i in range(num_chapters):
        prompt = f"Write chapter {i+1}/{num_chapters} for a fairy tale for {child_name}. Lang: {lang}. Themes: {', '.join(skills)}. Plot: {details}. Continue from: {full_text[-500:]}"
        if i == 0: prompt += " Title on 1st line."
        
        res = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}])
        full_text += res.choices[0].message.content

    # Чистка текста от технического мусора
    full_text = full_text.replace(":::writing", "").replace("###", "").strip()
    return full_text

def generate_image(title):
    """Создает обложку в стиле Pixar"""
    try:
        response = client.images.generate(
            model="dall-e-3", 
            prompt=f"High-quality Pixar style illustration: {title}"
        )
        return response.data[0].url
    except:
        return None

def get_speech_b64(text, voice_id):
    """Превращает текст в аудио и кодирует в base64 для экономии баллов"""
    api_key = st.secrets["ELEVENLABS_API_KEY"]
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    res = requests.post(url, 
                        json={"text": text, "model_id": "eleven_multilingual_v2"}, 
                        headers={"xi-api-key": api_key})
    
    if res.status_code == 200:
        return base64.b64encode(res.content).decode()
    return None
