import streamlit as st
from openai import OpenAI
import requests

# 1. Настройка страницы
st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="centered")

# --- СТИЛЬ (Нормальные кнопки и уютный дизайн) ---
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #f8fafc; }
    
    /* Кнопки тем: средний размер, удобный для нажатия */
    div.stButton > button {
        height: 70px !important; 
        font-size: 20px !important; 
        border-radius: 15px !important;
        border: 2px solid #334155 !important;
        background-color: #1e293b !important;
        color: white !important;
        margin-bottom: 10px;
        transition: 0.3s;
    }

    /* Подсветка активной темы */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%) !important;
        border: none !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.4) !important;
    }

    /* Главная кнопка запуска */
    .main-btn > div > button {
        height: 80px !important;
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%) !important;
        color: #000 !important;
        font-weight: bold !important;
        font-size: 22px !important;
    }

    .story-output { background: #fdfbf7; color: #1e293b; padding: 35px; border-radius: 25px; font-size: 1.2em; margin-top: 20px; white-space: pre-wrap; line-height: 1.6; border: 1px solid #e2e8f0; }
    </style>
    """, unsafe_allow_html=True)

# 2. Подключение ключей
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ELEVEN_KEY = st.secrets["ELEVENLABS_API_KEY"]

def generate_premium_audio(text):
    # Твой новый Voice ID для Марины
    VOICE_ID = "ymDCYd8puC7gYjxIamPt" 
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {"xi-api-key": ELEVEN_KEY, "Content-Type": "application/json"}
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.6, "similarity_boost": 0.8}
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.content
        else:
            st.error(f"Ошибка озвучки: {response.text}")
            return None
    except Exception as e:
        st.error(f"Ошибка связи с сервером голоса: {e}")
        return None

# --- ИНТЕРФЕЙС ---
if 'theme_idx' not in st.session_state: st.session_state.theme_idx = 0

st.title("🌟 NomNom Stories")
st.write("Сказки, которые помогают расти")

col1, col2 = st.columns(2)
with col1: name = st.text_input("Имя ребенка", value="Даша")
with col2: lang = st.selectbox("Язык сказки", ["Русский", "English"])

story_len = st.select_slider("⏳ Длина истории", options=["3 мин", "10 мин", "20 мин"])

st.divider()

st.subheader("🎯 Выберите тему")
cols = st.columns(3)
themes = ["🛡️ Храбрость", "🍎 Привычки", "🤝 Отношения"]

for i in range(3):
    with cols[i]:
        active = "primary" if st.session_state.theme_idx == i else "secondary"
        if st.button(themes[i], key=f"t_{i}", type=active, use_container_width=True):
            st.session_state.theme_idx = i
            st.rerun()

details = st.text_area("✍️ Опишите ситуацию:", placeholder="Например: Даша боится идти к стоматологу...")

# Кнопка генерации
st.markdown('<div class="main-btn">', unsafe_allow_html=True)
if st.button("✨ СОЗДАТЬ ЖИВУЮ СКАЗКУ ✨", type="primary", use_container_width=True):
    st.markdown('</div>', unsafe_allow_html=True)
    with st.spinner("Марина уже настраивает голос..."):
        try:
            curr_theme = themes[st.session_state.theme_idx]
            
            # Генерация текста
            prompt = f"Напиши добрую, поучительную сказку для {name}. Тема: {curr_theme}. Ситуация: {details}. Язык: {lang}. В конце сказки Марина должна ласково объяснить {name}, почему важно то, о чем была сказка, и поддержать её."
            
            res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
            story_text = res.choices[0].message.content
            
            # Картинка
            img_res = client.images.generate(model="dall-e-3", prompt=f"Cozy Pixar illustration for bedtime story: {curr_theme}, child {name}.")
            
            # Озвучка Мариной
            audio_content = generate_premium_audio(story_text[:4000])

            st.image(img_res.data[0].url, use_container_width=True)
            
            if audio_content:
                st.audio(audio_content, format="audio/mp3")
            
            st.markdown(f'<div class="story-output">{story_text}</div>', unsafe_allow_html=True)
            st.balloons()
            
        except Exception as e:
            st.error(f"Произошла ошибка: {e}")
