import streamlit as st
from openai import OpenAI
import requests

st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="centered")

# --- СТИЛЬ ---
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #f8fafc; }
    div.stButton > button {
        height: 70px !important; font-size: 20px !important; border-radius: 15px !important;
        background-color: #1e293b !important; color: white !important; margin-bottom: 10px;
    }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%) !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.4) !important; border: none !important;
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

# --- ИНТЕРФЕЙС ---
if 'theme_idx' not in st.session_state: st.session_state.theme_idx = 0

st.title("🌟 NomNom Stories")

col1, col2 = st.columns(2)
with col1: name = st.text_input("Имя ребенка", value="Даша")
with col2: lang = st.selectbox("Язык", ["Русский", "English"])

story_minutes = st.select_slider("⏳ Длительность сказки", options=[1, 3, 5, 10, 15, 20, 30, 45, 60], value=15)

st.divider()
themes = ["🛡️ Храбрость", "🍎 Привычки", "🤝 Отношения"]
cols = st.columns(3)
for i in range(3):
    with cols[i]:
        if st.button(themes[i], key=f"t_{i}", type="primary" if st.session_state.theme_idx == i else "secondary", use_container_width=True):
            st.session_state.theme_idx = i
            st.rerun()

details = st.text_area("✍️ Опиши ситуацию:")

if st.button("✨ СОЗДАТЬ БОЛЬШУЮ СКАЗКУ ✨", type="primary", use_container_width=True):
    with st.spinner("Марина пишет книгу по главам... Это займет около минуты."):
        try:
            curr_theme = themes[st.session_state.theme_idx]
            
            # ШАГ 1: Создаем подробный план на 4 главы
            plan_prompt = f"Составь подробный план сказки из 4 глав для {name}. Тема: {curr_theme}. Ситуация: {details}. План должен быть на языке {lang}."
            plan_res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": plan_prompt}])
            plan = plan_res.choices[0].message.content
            
            full_story = ""
            chapters_count = 4 if story_minutes >= 15 else 2 if story_minutes >= 5 else 1
            
            # ШАГ 2: Генерируем каждую главу отдельно для объема
            for i in range(chapters_count):
                chapter_prompt = f"Напиши главу {i+1} сказки для {name} по этому плану: {plan}. Это должна быть очень длинная глава с множеством диалогов и описаний. Если это последняя глава, добавь ласковое поучение в конце. Предыдущий текст: {full_story[-500:]}"
                ch_res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": chapter_prompt}])
                chapter_text = ch_res.choices[0].message.content
                full_story += "\n\n" + chapter_text
            
            # Картинка
            img_res = client.images.generate(model="dall-e-3", prompt=f"Cozy Pixar illustration: {curr_theme}, child {name}.")
            st.image(img_res.data[0].url, use_container_width=True)

            # ШАГ 3: Озвучка Мариной
            st.subheader(f"🎙️ Слушаем сказку по главам:")
            chunks = [full_story[i:i+4000] for i in range(0, len(full_story), 4000)]
            for idx, chunk in enumerate(chunks):
                st.write(f"**Часть {idx+1}**")
                generate_premium_audio(chunk)
            
            st.markdown(f'<div class="story-output">{full_story}</div>', unsafe_allow_html=True)
            st.balloons()
            
        except Exception as e:
            st.error(f"Ошибка: {e}")
