import streamlit as st
from openai import OpenAI

# 1. Настройка страницы
st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="centered")

# --- СТИЛИЗАЦИЯ ---
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #f8fafc; }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%) !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.5);
    }
    .story-output { background: #fdfbf7; color: #1e293b; padding: 35px; border-radius: 25px; font-size: 1.3em; margin-top: 20px;}
    </style>
    """, unsafe_allow_html=True)

# Инициализация состояния
if 'theme_idx' not in st.session_state: st.session_state.theme_idx = 0

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Переводы для новых функций
translations = {
    "Русский": {
        "themes": ["🛡️ Храбрость", "🍎 Привычки", "🤝 Отношения"],
        "length_label": "⏳ Длительность сказки",
        "lengths": ["Короткая (2-3 мин)", "Средняя (10 мин)", "Длинная (20-25 мин)"],
        "voice_label": "🎙️ Выбери голос",
        "btn_main": "✨ СОЗДАТЬ ВОЛШЕБНУЮ ИСТОРИЮ ✨",
        "proc": "Пишем длинную сказку... Это может занять около минуты..."
    },
    "English": {
        "themes": ["🛡️ Bravery", "🍎 Habits", "🤝 Relations"],
        "length_label": "⏳ Story Length",
        "lengths": ["Short (3 min)", "Medium (10 min)", "Long (20-25 min)"],
        "voice_label": "🎙️ Choose Voice",
        "btn_main": "✨ CREATE MAGIC STORY ✨",
        "proc": "Writing a long story... Please wait a minute..."
    }
}

lang = st.selectbox("🌍 Language", ["Русский", "English"])
t = translations[lang]

st.title("🌟 NomNom Stories")

# --- НАСТРОЙКИ (В ОДИН РЯД) ---
c1, c2, c3 = st.columns([1, 1, 1])
with c1:
    name = st.text_input("Имя", value="Даша")
with c2:
    voice = st.selectbox(t["voice_label"], ["alloy", "echo", "fable", "onyx", "nova", "shimmer"], index=4)
with c3:
    story_len = st.select_slider(t["length_label"], options=t["lengths"], value=t["lengths"][0])

st.divider()

# ТЕМЫ
st.subheader("🎯 Тема")
cols = st.columns(3)
for i in range(3):
    with cols[i]:
        is_active = "primary" if st.session_state.theme_idx == i else "secondary"
        if st.button(t['themes'][i], key=f"t_{i}", type=is_active, use_container_width=True):
            st.session_state.theme_idx = i
            st.rerun()

details = st.text_area("✍️ Детали:", placeholder="Например: Полет на луну на розовом драконе...")

if st.button(t['btn_main'], type="primary", use_container_width=True):
    with st.spinner(t['proc']):
        try:
            curr_theme = t['themes'][st.session_state.theme_idx]
            
            # Настройка промпта в зависимости от длины
            len_instr = "Напиши очень длинную и подробную сказку. Минимум 15-20 абзацев, с диалогами и описанием природы." if story_len == t["lengths"][2] else "Напиши сказку среднего размера."
            
            prompt = f"{len_instr} Герой: {name}. Тема: {curr_theme}. Детали: {details}. Язык: {lang}. Стиль: Успокаивающий, для сна."
            
            res = client.chat.completions.create(model="gpt-4o", messages=[{"role":"user","content":prompt}])
            story = res.choices[0].message.content
            
            # Генерация картинки
            img_res = client.images.generate(model="dall-e-3", prompt=f"Pixar dream world: {curr_theme}, child {name}.")
            
            # Озвучка (с выбранным голосом)
            # Примечание: Если текст будет ОЧЕНЬ длинным, нам в будущем нужно будет делить его на части.
            audio_res = client.audio.speech.create(model="tts-1", voice=voice, input=story[:4000])

            st.image(img_res.data[0].url, use_container_width=True)
            st.audio(audio_res.content)
            st.markdown(f'<div class="story-output">{story}</div>', unsafe_allow_html=True)
            st.balloons()
        except Exception as e:
            st.error(f"Error: {e}")
