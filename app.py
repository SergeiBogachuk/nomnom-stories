import streamlit as st
from openai import OpenAI

# 1. Настройка страницы
st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="centered")

# --- СЛОВАРЬ ПЕРЕВОДОВ (Полный) ---
translations = {
    "Русский": {
        "title": "🌟 NomNom Stories",
        "subtitle": "Инструмент для родителей: превращаем капризы в сказочные уроки",
        "settings": "👶 Настройки героя",
        "name_label": "Имя",
        "voice_label": "🎙️ Выбери голос",
        "length_label": "⏳ Длительность сказки",
        "lengths": ["Короткая (2-3 мин)", "Средняя (10 мин)", "Длинная (20-25 мин)"],
        "theme_header": "🎯 Тема",
        "themes": ["🛡️ Храбрость", "🍎 Привычки", "🤝 Отношения"],
        "details_label": "✍️ Детали:",
        "details_ph": "Например: Полет на луну на розовом драконе...",
        "btn_main": "✨ СОЗДАТЬ ВОЛШЕБНУЮ ИСТОРИЮ ✨",
        "proc": "Пишем длинную сказку... Это может занять около минуты...",
        "lang_select": "🌍 Выберите язык"
    },
    "English": {
        "title": "🌟 NomNom Stories",
        "subtitle": "Parenting tool: turning tantrums into fairy tale lessons",
        "settings": "👶 Hero Settings",
        "name_label": "Name",
        "voice_label": "🎙️ Choose Voice",
        "length_label": "⏳ Story Length",
        "lengths": ["Short (3 min)", "Medium (10 min)", "Long (20-25 min)"],
        "theme_header": "🎯 Theme",
        "themes": ["🛡️ Bravery", "🍎 Habits", "🤝 Relations"],
        "details_label": "✍️ Details:",
        "details_ph": "Example: Flying to the moon on a pink dragon...",
        "btn_main": "✨ CREATE MAGIC STORY ✨",
        "proc": "Writing a long story... Please wait a minute...",
        "lang_select": "🌍 Choose Language"
    }
}

# --- СТИЛИЗАЦИЯ ---
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #f8fafc; }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%) !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.5);
    }
    .story-output { background: #fdfbf7; color: #1e293b; padding: 35px; border-radius: 25px; font-size: 1.2em; margin-top: 20px;}
    </style>
    """, unsafe_allow_html=True)

# Инициализация состояния темы
if 'theme_idx' not in st.session_state: st.session_state.theme_idx = 0

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Выбор языка
lang = st.selectbox("🌍 Language", ["Русский", "English"], index=0)
t = translations[lang]

st.title(t["title"])
st.write(f"<p style='text-align: center;'>{t['subtitle']}</p>", unsafe_allow_html=True)

# --- НАСТРОЙКИ ---
st.markdown(f"### {t['settings']}")
c1, c2, c3 = st.columns([1, 1, 1.2])
with c1:
    name = st.text_input(t["name_label"], value="Даша")
with c2:
    voice = st.selectbox(t["voice_label"], ["alloy", "echo", "fable", "onyx", "nova", "shimmer"], index=4)
with c3:
    story_len = st.select_slider(t["length_label"], options=t["lengths"], value=t["lengths"][0])

st.divider()

# --- ТЕМЫ ---
st.subheader(t["theme_header"])
cols = st.columns(3)
for i in range(3):
    with cols[i]:
        is_active = "primary" if st.session_state.theme_idx == i else "secondary"
        if st.button(t['themes'][i], key=f"t_{i}", type=is_active, use_container_width=True):
            st.session_state.theme_idx = i
            st.rerun()

# --- ДЕТАЛИ ---
details = st.text_area(t["details_label"], placeholder=t["details_ph"])

# --- ГЕНЕРАЦИЯ ---
if st.button(t['btn_main'], type="primary", use_container_width=True):
    with st.spinner(t['proc']):
        try:
            curr_theme = t['themes'][st.session_state.theme_idx]
            
            # Настройка промпта в зависимости от длины
            len_instr = "Write a VERY long, detailed bedtime story. Use chapters, dialogues, and rich descriptions. Minimum 2000 words." if story_len == t["lengths"][2] else "Write a comprehensive story."
            
            full_prompt = f"{len_instr} Hero name: {name}. Theme: {curr_theme}. Details: {details}. Language: {lang}. Style: Soothing bedtime story."
            
            res = client.chat.completions.create(model="gpt-4o", messages=[{"role":"user","content":full_prompt}])
            story_text = res.choices[0].message.content
            
            # Картинка
            img_res = client.images.generate(model="dall-e-3", prompt=f"Pixar dream world: {curr_theme}, child {name}.")
            
            # Озвучка
            audio_res = client.audio.speech.create(model="tts-1", voice=voice, input=story_text[:4000])

            # Вывод результата
            st.image(img_res.data[0].url, use_container_width=True)
            st.audio(audio_res.content)
            st.markdown(f'<div class="story-output">{story_text}</div>', unsafe_allow_html=True)
            st.balloons()
        except Exception as e:
            st.error(f"Error: {e}")
