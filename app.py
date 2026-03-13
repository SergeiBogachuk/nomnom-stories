import streamlit as st
from openai import OpenAI

# 1. Настройка страницы
st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="centered")

# --- УЛУЧШЕННЫЙ ДИЗАЙН ---
st.markdown("""
    <style>
    /* Основной фон - глубокий космос */
    .stApp { background: #0f172a; color: #f8fafc; }
    
    /* Стили для кнопок-плиток */
    div.stButton > button {
        border-radius: 20px;
        height: 120px;
        width: 100%;
        border: 2px solid #334155;
        background-color: #1e293b;
        color: #94a3b8;
        transition: all 0.3s ease;
        font-size: 18px !important;
        font-weight: bold;
    }

    /* Эффект при наведении */
    div.stButton > button:hover {
        border-color: #38bdf8;
        color: #38bdf8;
        transform: translateY(-3px);
    }

    /* СТИЛЬ ДЛЯ ВЫБРАННОЙ КНОПКИ */
    /* Мы используем специальный хак, чтобы подсветить кнопку, если ее имя совпадает с выбранной темой */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.5);
        transform: scale(1.02);
    }

    /* Поле вывода сказки - как старинный пергамент */
    .story-output { 
        background: #fdfbf7; 
        color: #1e293b; 
        padding: 35px; 
        border-radius: 25px; 
        font-size: 1.3em; 
        margin-top: 20px;
        box-shadow: inset 0 0 50px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    
    /* Поля ввода */
    .stTextInput input, .stTextArea textarea {
        background-color: #1e293b !important;
        color: white !important;
        border-radius: 10px !important;
        border: 1px solid #334155 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Словарь переводов
translations = {
    "Русский": {
        "themes": ["🛡️ Храбрость", "🍎 Привычки", "🤝 Отношения"],
        "btn_main": "✨ СОЗДАТЬ ВОЛШЕБНУЮ ИСТОРИЮ ✨",
        "settings": "👶 Настройки героя", "name": "Имя", "age": "Возраст",
        "details": "✍️ Добавь подробности:", "proc": "Магия в процессе..."
    },
    "English": {
        "themes": ["🛡️ Bravery", "🍎 Habits", "🤝 Relations"],
        "btn_main": "✨ CREATE MAGIC STORY ✨",
        "settings": "👶 Hero Settings", "name": "Name", "age": "Age",
        "details": "✍️ Add details:", "proc": "Magic in progress..."
    }
}

# Инициализация выбора
if 'theme_idx' not in st.session_state: st.session_state.theme_idx = 0

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Язык
col_l, _ = st.columns([1, 2])
with col_l: lang = st.selectbox("🌍 Language", ["Русский", "English"])
t = translations[lang]

st.title("🌟 NomNom Stories")

# Настройки героя
st.markdown(f"### {t['settings']}")
c_n, c_a, _ = st.columns([1.5, 1.5, 1])
with c_n: name = st.text_input(t['name'], value="Даша")
with c_a: age = st.slider(t['age'], 1, 12, 5)

st.divider()

# ВЫБОР ТЕМЫ
st.subheader("🎯 Какую тему выберем?")
cols = st.columns(3)

for i in range(3):
    with cols[i]:
        # Если индекс кнопки совпадает с выбранным, делаем ее "primary" (синей)
        is_active = "primary" if st.session_state.theme_idx == i else "secondary"
        if st.button(t['themes'][i], key=f"t_{i}", type=is_active, use_container_width=True):
            st.session_state.theme_idx = i
            st.rerun()

st.divider()
details = st.text_area(t['details'], placeholder="Например: Даша боится пауков...")

# Главная кнопка
if st.button(t['btn_main'], type="primary", use_container_width=True):
    with st.spinner(t['proc']):
        try:
            curr_theme = t['themes'][st.session_state.theme_idx]
            prompt = f"Write a long story for {name} ({age} years old). Theme: {curr_theme}. Details: {details}. Language: {lang}. Pixar style."
            
            res = client.chat.completions.create(model="gpt-4o", messages=[{"role":"user","content":prompt}])
            story = res.choices[0].message.content
            
            img_res = client.images.generate(model="dall-e-3", prompt=f"Pixar illustration: {curr_theme}, child {name}, {age} years old.")
            audio_res = client.audio.speech.create(model="tts-1", voice="alloy", input=story[:4000])

            st.image(img_res.data[0].url, use_container_width=True)
            st.audio(audio_res.content)
            st.markdown(f'<div class="story-output">{story}</div>', unsafe_allow_html=True)
            st.balloons()
        except Exception as e:
            st.error(f"Error: {e}")
