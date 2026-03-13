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
    .main-btn > div > button {
        height: 80px !important; background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%) !important;
        color: #000 !important; font-weight: bold !important; font-size: 22px !important;
    }
    .story-output { background: #fdfbf7; color: #1e293b; padding: 35px; border-radius: 25px; font-size: 1.2em; margin-top: 20px; white-space: pre-wrap; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ELEVEN_KEY = st.secrets["ELEVENLABS_API_KEY"]

def generate_premium_audio(text, part_num=None):
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
        label = f"Часть {part_num}" if part_num else "Слушать сказку"
        st.audio(response.content, format="audio/mp3")
    else:
        st.error(f"Ошибка озвучки: {response.text}")

# --- ИНТЕРФЕЙС ---
if 'theme_idx' not in st.session_state: st.session_state.theme_idx = 0

st.title("🌟 NomNom Stories")

col1, col2 = st.columns(2)
with col1: name = st.text_input("Имя ребенка", value="Даша")
with col2: lang = st.selectbox("Язык", ["Русский", "English"])

# Настройка длительности влияет на размер текста
story_len = st.select_slider("⏳ Длительность", options=["3 мин", "10 мин", "20 мин"])

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

details = st.text_area("✍️ Опишите ситуацию:")

if st.button("✨ СОЗДАТЬ ЖИВУЮ СКАЗКУ ✨", type="primary", use_container_width=True):
    with st.spinner("Марина сочиняет длинную историю..."):
        try:
            curr_theme = themes[st.session_state.theme_idx]
            
            # Настройка объема текста в зависимости от выбора
            length_map = {"3 мин": "короткую", "10 мин": "очень длинную и подробную", "20 мин": "максимально длинную, эпическую, со множеством диалогов и деталей"}
            
            prompt = f"Напиши {length_map[story_len]} сказку для {name}. Тема: {curr_theme}. Ситуация: {details}. Язык: {lang}. В конце Марина должна ласково подытожить смысл истории для ребенка."
            
            res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
            story_text = res.choices[0].message.content
            
            # Картинка
            img_res = client.images.generate(model="dall-e-3", prompt=f"Pixar illustration: {curr_theme}, child {name}.")
            st.image(img_res.data[0].url, use_container_width=True)

            # ОЗВУЧКА (разбиваем на части по 4000 символов, чтобы не было ошибок лимита)
            st.subheader("🎙️ Голос Марины:")
            chunks = [story_text[i:i+4000] for i in range(0, len(story_text), 4000)]
            
            for idx, chunk in enumerate(chunks):
                generate_premium_audio(chunk, part_num=idx+1 if len(chunks) > 1 else None)
            
            st.markdown(f'<div class="story-output">{story_text}</div>', unsafe_allow_html=True)
            st.balloons()
            
        except Exception as e:
            st.error(f"Ошибка: {e}")
