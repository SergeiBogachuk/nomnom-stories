import streamlit as st
from openai import OpenAI

# 1. Настройка страницы
st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="centered")

# --- СЛОВАРЬ ПЕРЕВОДОВ ---
translations = {
    "Русский": {
        "title": "🌟 NomNom Stories",
        "subtitle": "Превращаем капризы в сказочные уроки",
        "settings": "👶 Настройки героя",
        "name_label": "Имя",
        "voice_label": "🎙️ Выбери голос",
        "length_label": "⏳ Длительность",
        "lengths": ["3 мин", "10 мин", "20 мин"],
        "theme_header": "🎯 Тема",
        "themes": ["🛡️ Храбрость", "🍎 Привычки", "🤝 Отношения"],
        "details_label": "✍️ Детали:",
        "details_ph": "Например: Полет на луну...",
        "btn_main": "✨ СОЗДАТЬ ВОЛШЕБНУЮ ИСТОРИЮ ✨",
        "proc": "Пишем ОЧЕНЬ длинную историю в несколько глав... Пожалуйста, подождите (до 1-2 минут)...",
    },
    "English": {
        "title": "🌟 NomNom Stories",
        "subtitle": "Turning tantrums into fairy tale lessons",
        "settings": "👶 Hero Settings",
        "name_label": "Name",
        "voice_label": "🎙️ Voice",
        "length_label": "⏳ Duration",
        "lengths": ["3 min", "10 min", "20 min"],
        "theme_header": "🎯 Theme",
        "themes": ["🛡️ Bravery", "🍎 Habits", "🤝 Relations"],
        "details_label": "✍️ Details:",
        "details_ph": "Example: Flying to the moon...",
        "btn_main": "✨ CREATE MAGIC STORY ✨",
        "proc": "Writing a VERY long multi-chapter story... Please wait (up to 1-2 mins)...",
    }
}

st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #f8fafc; }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%) !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.5);
    }
    .story-output { background: #fdfbf7; color: #1e293b; padding: 35px; border-radius: 25px; font-size: 1.2em; margin-top: 20px; white-space: pre-wrap;}
    </style>
    """, unsafe_allow_html=True)

if 'theme_idx' not in st.session_state: st.session_state.theme_idx = 0

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

lang = st.selectbox("🌍 Language", ["Русский", "English"], index=0)
t = translations[lang]

st.title(t["title"])
st.write(f"<p style='text-align: center;'>{t['subtitle']}</p>", unsafe_allow_html=True)

# --- НАСТРОЙКИ ---
st.markdown(f"### {t['settings']}")
c1, c2, c3 = st.columns([1, 1, 1.2])
with c1: name = st.text_input(t["name_label"], value="Даша")
with c2: voice = st.selectbox(t["voice_label"], ["alloy", "echo", "fable", "onyx", "nova", "shimmer"], index=4)
with c3: story_len = st.select_slider(t["length_label"], options=t["lengths"], value=t["lengths"][0])

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

details = st.text_area(t["details_label"], placeholder=t["details_ph"])

if st.button(t['btn_main'], type="primary", use_container_width=True):
    with st.spinner(t['proc']):
        try:
            curr_theme = t['themes'][st.session_state.theme_idx]
            
            # --- ЛОГИКА ГЕНЕРАЦИИ ДЛИННОГО ТЕКСТА ---
            # Мы заставляем ИИ писать частями или очень подробно
            if story_len == t["lengths"][0]: # 3 мин
                multiplier = "Напиши сказку на 500 слов."
            elif story_len == t["lengths"][1]: # 10 мин
                multiplier = "Напиши ОЧЕНЬ подробную сказку на 1500 слов. Используй много описаний чувств, звуков, долгое вступление и плавное развитие сюжета."
            else: # 20 мин
                multiplier = "Напиши ГИГАНТСКУЮ сказку на 3000 слов. Это должна быть целая аудиокнига с 3 главами. Каждую сцену описывай максимально детально, как будто замедленное кино."

            full_prompt = f"{multiplier} Имя ребенка: {name}. Тема: {curr_theme}. Детали: {details}. Язык: {lang}. Стиль: Убаюкивающий, Pixar."
            
            res = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role":"user","content":full_prompt}],
                temperature=0.7 # Чуть больше креативности для длины
            )
            story_text = res.choices[0].message.content
            
            # Картинка
            img_res = client.images.generate(model="dall-e-3", prompt=f"Magical book illustration for kids: {curr_theme}, {name}.")
            
            # Озвучка (Важно: OpenAI TTS имеет лимит символов. Если текст супер-длинный, берем пока максимум)
            audio_res = client.audio.speech.create(model="tts-1", voice=voice, input=story_text[:4096])

            st.image(img_res.data[0].url, use_container_width=True)
            st.audio(audio_res.content)
            st.markdown(f'<div class="story-output">{story_text}</div>', unsafe_allow_html=True)
            st.balloons()
            
        except Exception as e:
            st.error(f"Error: {e}")
