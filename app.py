import streamlit as st
from openai import OpenAI
import requests

st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="centered")

# --- СТИЛЬ (Удобные кнопки и ползунок) ---
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #f8fafc; }
    
    /* Кнопки тем: средний удобный размер */
    div.stButton > button {
        height: 70px !important; 
        font-size: 20px !important; 
        border-radius: 15px !important;
        background-color: #1e293b !important;
        color: white !important;
        margin-bottom: 10px;
    }

    /* Активная тема */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%) !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.4) !important;
        border: none !important;
    }

    .story-output { background: #fdfbf7; color: #1e293b; padding: 35px; border-radius: 25px; font-size: 1.2em; margin-top: 20px; white-space: pre-wrap; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ELEVEN_KEY = st.secrets["ELEVENLABS_API_KEY"]

def generate_premium_audio(text):
    VOICE_ID = "ymDCYd8puC7gYjxIamPt" # Марина
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {"xi-api-key": ELEVEN_KEY, "Content-Type": "application/json"}
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.6, "similarity_boost": 0.8}
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        st.audio(response.content, format="audio/mp3")
    else:
        st.error(f"Ошибка озвучки: {response.text}")

# --- ИНТЕРФЕЙС ---
if 'theme_idx' not in st.session_state: st.session_state.theme_idx = 0

st.title("🌟 NomNom Stories")

col1, col2 = st.columns(2)
with col1: 
    name = st.text_input("Имя ребенка", value="Даша")
with col2: 
    lang = st.selectbox("Язык", ["Русский", "English"])

# ВЕРНУЛИ ПОЛЗУНОК, НО СДЕЛАЛИ ЕГО ГИБКИМ (от 1 до 60 минут)
story_minutes = st.select_slider(
    "⏳ Длительность сказки (в минутах)",
    options=[1, 3, 5, 10, 15, 20, 30, 45, 60],
    value=10
)

st.divider()
st.subheader("🎯 Тема сказки")
cols = st.columns(3)
themes = ["🛡️ Храбрость", "🍎 Привычки", "🤝 Отношения"]
for i in range(3):
    with cols[i]:
        active = "primary" if st.session_state.theme_idx == i else "secondary"
        if st.button(themes[i], key=f"t_{i}", type=active, use_container_width=True):
            st.session_state.theme_idx = i
            st.rerun()

details = st.text_area("✍️ Опиши ситуацию:")

if st.button("✨ СОЗДАТЬ ЖИВУЮ СКАЗКУ ✨", type="primary", use_container_width=True):
    with st.spinner(f"Марина готовит сказку на {story_minutes} мин..."):
        try:
            curr_theme = themes[st.session_state.theme_idx]
            
            # Инструкция для ИИ по объему текста
            prompt = f"Напиши сказку для {name} на языке {lang}. Текст должен быть очень объемным, чтобы его чтение заняло {story_minutes} минут. Тема: {curr_theme}. Ситуация: {details}. В самом конце Марина должна нежно подытожить смысл сказки для ребенка."
            
            res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
            story_text = res.choices[0].message.content
            
            # Картинка
            img_res = client.images.generate(model="dall-e-3", prompt=f"Pixar illustration: {curr_theme}, child {name}.")
            st.image(img_res.data[0].url, use_container_width=True)

            # Озвучка Мариной (автоматически разбивает на части по 4000 символов)
            st.subheader(f"🎙️ Слушаем сказку:")
            chunks = [story_text[i:i+4000] for i in range(0, len(story_text), 4000)]
            
            for idx, chunk in enumerate(chunks):
                if len(chunks) > 1:
                    st.write(f"**Часть {idx+1}**")
                generate_premium_audio(chunk)
            
            st.markdown(f'<div class="story-output">{story_text}</div>', unsafe_allow_html=True)
            st.balloons()
            
        except Exception as e:
            st.error(f"Ошибка: {e}")
