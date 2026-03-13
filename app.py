import streamlit as st
from openai import OpenAI
import requests

# 1. Настройка страницы
st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="centered")

# --- СТИЛЬ ---
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #f8fafc; }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%) !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.5);
    }
    .story-output { background: #fdfbf7; color: #1e293b; padding: 35px; border-radius: 25px; font-size: 1.3em; margin-top: 20px; white-space: pre-wrap; line-height: 1.7; }
    </style>
    """, unsafe_allow_html=True)

# 2. Подключение ключей
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ELEVEN_KEY = st.secrets["ELEVENLABS_API_KEY"]

# Функция для ПРЕМИУМ озвучки (ElevenLabs)
def generate_premium_audio(text):
    # ПРОВЕРЬ ЭТОТ ID! Это голос Alice. 
    # Если ты выбрал другой в ElevenLabs, замени эти буквы на свои:
    VOICE_ID = "ymDCYd8puC7gYjxIamPt" 
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVEN_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2", # Лучшая модель для русского языка
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        st.error(f"Ошибка ElevenLabs: {response.text}")
        return None

# --- ИНТЕРФЕЙС ---
if 'theme_idx' not in st.session_state: st.session_state.theme_idx = 0

st.title("🌟 NomNom Stories")
st.write("### Терапевтические сказки с живым голосом")

# Убираем старый выбор голосов, оставляем только настройки героя
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Имя героя", value="Даша")
with col2:
    lang = st.selectbox("Язык", ["Русский", "English"])

story_len = st.select_slider("⏳ Длительность", options=["3 мин", "10 мин", "20 мин"])

st.divider()

# Темы
st.subheader("🎯 Какую тему выберем?")
cols = st.columns(3)
themes = ["🛡️ Храбрость", "🍎 Привычки", "🤝 Отношения"]
for i in range(3):
    with cols[i]:
        active = "primary" if st.session_state.theme_idx == i else "secondary"
        if st.button(themes[i], key=f"t_{i}", type=active, use_container_width=True):
            st.session_state.theme_idx = i
            st.rerun()

details = st.text_area("✍️ Опиши ситуацию (например: почему Даша не хочет спать?)")

# --- ГЕНЕРАЦИЯ ---
if st.button("✨ СОЗДАТЬ ЖИВУЮ СКАЗКУ ✨", type="primary", use_container_width=True):
    with st.spinner("Сочиняем историю и включаем живой голос..."):
        try:
            curr_theme = themes[st.session_state.theme_idx]
            
            # 1. Текст (с твоим пожеланием про итог в конце)
            prompt = f"Напиши очень подробную сказку для {name}. Тема: {curr_theme}. Ситуация: {details}. Язык: {lang}. В самом конце сказки ласково подытожь историю специально для {name}, объяснив смысл того, что произошло."
            
            res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
            story_text = res.choices[0].message.content
            
            # 2. Картинка
            img_res = client.images.generate(model="dall-e-3", prompt=f"Pixar illustration: {curr_theme}, child {name}.")
            
            # 3. ОЗВУЧКА ЧЕРЕЗ ELEVENLABS
            # Мы берем первые 4000 знаков для теста
            audio_content = generate_premium_audio(story_text[:4000])

            st.image(img_res.data[0].url, use_container_width=True)
            
            if audio_content:
                st.audio(audio_content, format="audio/mp3")
            
            st.markdown(f'<div class="story-output">{story_text}</div>', unsafe_allow_html=True)
            st.balloons()
            
        except Exception as e:
            st.error(f"Ошибка: {e}")
