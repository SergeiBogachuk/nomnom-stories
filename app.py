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
    .story-output { background: #fdfbf7; color: #1e293b; padding: 35px; border-radius: 25px; font-size: 1.2em; margin-top: 20px; white-space: pre-wrap; line-height: 1.6; }
    .moral-box { background: #e0f2fe; border-left: 5px solid #0ea5e9; padding: 20px; border-radius: 10px; color: #0369a1; margin-top: 20px; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

if 'theme_idx' not in st.session_state: st.session_state.theme_idx = 0

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Переводы
translations = {
    "Русский": {
        "title": "🌟 NomNom Stories",
        "subtitle": "Сказкотерапия: мягко решаем детские капризы",
        "settings": "👶 Профиль ребенка",
        "name_label": "Имя",
        "voice_label": "🎙️ Голос",
        "length_label": "⏳ Длительность",
        "lengths": ["3 мин", "10 мин", "20 мин"],
        "theme_header": "🎯 Что сегодня беспокоит?",
        "themes": ["🛡️ Храбрость", "🍎 Привычки", "🤝 Отношения"],
        "details_label": "✍️ Опишите ситуацию (для психолога):",
        "details_ph": "Например: Ребенок боится идти к стоматологу...",
        "btn_main": "✨ СОЗДАТЬ ТЕРАПЕВТИЧЕСКУЮ СКАЗКУ ✨",
        "proc": "Мастерю поучительную историю... Пожалуйста, подождите.",
        "moral_title": "💡 Смысл этой сказки:",
    },
    "English": {
        "title": "🌟 NomNom Stories",
        "subtitle": "Fairy Tale Therapy: solving tantrums gently",
        "settings": "👶 Child Profile",
        "name_label": "Name",
        "voice_label": "🎙️ Voice",
        "length_label": "⏳ Duration",
        "lengths": ["3 min", "10 min", "20 min"],
        "theme_header": "🎯 Today's focus?",
        "themes": ["🛡️ Bravery", "🍎 Habits", "🤝 Relations"],
        "details_label": "✍️ Describe situation (for psychology focus):",
        "details_ph": "Example: Child is afraid of the dentist...",
        "btn_main": "✨ CREATE THERAPEUTIC STORY ✨",
        "proc": "Crafting a meaningful story... Please wait.",
        "moral_title": "💡 The lesson of this story:",
    }
}

lang = st.selectbox("🌍 Language", ["Русский", "English"], index=0)
t = translations[lang]

st.title(t["title"])
st.write(f"<p style='text-align: center;'>{t['subtitle']}</p>", unsafe_allow_html=True)

# Настройки
st.markdown(f"### {t['settings']}")
c1, c2, c3 = st.columns([1, 1, 1.2])
with c1: name = st.text_input(t["name_label"], value="Даша")
with c2: voice = st.selectbox(t["voice_label"], ["alloy", "echo", "fable", "onyx", "nova", "shimmer"], index=4)
with c3: story_len = st.select_slider(t["length_label"], options=t["lengths"], value=t["lengths"][0])

st.divider()

# Темы
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
            
            # --- ПСИХОЛОГИЧЕСКИЙ ПРОМПТ ---
            system_role = "Ты — детский психолог и сказочник. Твоя цель — написать терапевтическую сказку."
            
            len_instr = "Напиши огромную историю (минимум 2000 слов). Раздели на 4 главы." if story_len == t["lengths"][2] else "Напиши подробную историю."
            
            psych_instr = f"""
            Используй психологические приемы:
            1. В начале сказки герой сталкивается с проблемой: {details}.
            2. Опиши чувства героя (страх, обида, неуверенность).
            3. Герой проходит путь и находит способ справиться.
            4. ВАЖНО: В самом конце, после текста сказки, напиши заголовок 'ИТОГ' и кратко в 3-4 предложениях сформулируй психологический смысл: чему научилась {name} и как это применять в жизни.
            """

            full_prompt = f"{len_instr} {psych_instr} Ребенок: {name}. Тема: {curr_theme}. Язык: {lang}."
            
            res = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_role},
                    {"role": "user", "content": full_prompt}
                ]
            )
            raw_content = res.choices[0].message.content
            
            # Разделяем сказку и итог
            if "ИТОГ" in raw_content:
                story_text, moral = raw_content.split("ИТОГ", 1)
            else:
                story_text, moral = raw_content, ""

            img_res = client.images.generate(model="dall-e-3", prompt=f"Pixar calm illustration: {curr_theme}, soft lighting, child {name}.")
            
            # Озвучка (берем первые 4000 символов — это лимит)
            audio_res = client.audio.speech.create(model="tts-1", voice=voice, input=story_text[:4000])

            st.image(img_res.data[0].url, use_container_width=True)
            st.audio(audio_res.content)
            
            # Вывод сказки
            st.markdown(f'<div class="story-output">{story_text}</div>', unsafe_allow_html=True)
            
            # Вывод итога (в отдельной рамке)
            if moral:
                st.markdown(f'<div class="moral-box"><b>{t["moral_title"]}</b><br>{moral}</div>', unsafe_allow_html=True)
            
            st.balloons()
        except Exception as e:
            st.error(f"Error: {e}")
