import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="centered")

# --- ДИЗАЙН ---
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

if 'theme_idx' not in st.session_state: st.session_state.theme_idx = 0

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Переводы
translations = {
    "Русский": {
        "title": "🌟 NomNom Stories",
        "subtitle": "Умные терапевтические сказки для сна",
        "settings": "👶 Настройки",
        "name_label": "Имя",
        "voice_label": "🎙️ Голос",
        "length_label": "⏳ Длительность",
        "lengths": ["3 мин", "10 мин", "20 мин"],
        "theme_header": "🎯 Тема сказки",
        "themes": ["🛡️ Храбрость", "🍎 Привычки", "🤝 Отношения"],
        "details_label": "✍️ Опишите ситуацию (что важно проговорить?):",
        "btn_main": "✨ СОЗДАТЬ ДЛИННУЮ СКАЗКУ ✨",
        "proc": "Генерируем большую историю и аудио... Это займет время (до 2 мин).",
    },
    "English": {
        "title": "🌟 NomNom Stories",
        "subtitle": "Smart therapeutic bedtime stories",
        "settings": "👶 Settings",
        "name_label": "Name",
        "voice_label": "🎙️ Voice",
        "length_label": "⏳ Duration",
        "lengths": ["3 min", "10 min", "20 min"],
        "theme_header": "🎯 Theme",
        "themes": ["🛡️ Bravery", "🍎 Habits", "🤝 Relations"],
        "details_label": "✍️ Describe situation (core lesson):",
        "btn_main": "✨ CREATE LONG STORY ✨",
        "proc": "Generating long story and audio... Please wait (up to 2 min).",
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

details = st.text_area(t["details_label"], placeholder="Например: Почему важно делиться игрушками...")

if st.button(t['btn_main'], type="primary", use_container_width=True):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    with st.spinner(t['proc']):
        try:
            curr_theme = t['themes'][st.session_state.theme_idx]
            
            # --- ЛОГИКА АВТОМАТИЧЕСКОЙ СБОРКИ ДЛИННОЙ СКАЗКИ ---
            if story_len == t["lengths"][0]: # 3 минуты
                parts = 1
                prompt_style = "Напиши подробную сказку."
            elif story_len == t["lengths"][1]: # 10 минут
                parts = 2
                prompt_style = "Напиши огромную сказку. Это только ПЕРВАЯ ЧАСТЬ длинного повествования."
            else: # 20 минут
                parts = 3
                prompt_style = "Напиши эпическую сказку. Это только НАЧАЛО огромной истории (Часть 1)."

            full_story = ""
            
            # Цикл генерации глав
            for p in range(parts):
                status_text.text(f"Создаем главу {p+1}...")
                
                # Контекст для продолжения
                context = f"Продолжай историю для {name}. Мы уже написали: {full_story[-500:]}" if p > 0 else ""
                
                res = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{
                        "role": "user", 
                        "content": f"{prompt_style} {context} Тема: {curr_theme}. Ситуация: {details}. Язык: {lang}. Стиль Pixar."
                    }]
                )
                full_story += res.choices[0].message.content + "\n\n"
                progress_bar.progress((p + 1) / (parts + 1))

            # --- ДОБАВЛЯЕМ АНАЛИЗ В КОНЦЕ ---
            status_text.text("Добавляем психологический разбор...")
            analysis_prompt = f"Напиши финальный абзац для сказки. Обратись к ребенку по имени {name}. Ласково объясни психологический смысл сказки (почему герой поступил так, что это дало) и подведи итог ситуации {details}. Это должно звучать как мудрое завершение сказки."
            
            analysis_res = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": analysis_prompt}]
            )
            full_story += "\n\n--- МУДРЫЙ ИТОГ ---\n\n" + analysis_res.choices[0].message.content
            
            # Картинка
            img_res = client.images.generate(model="dall-e-3", prompt=f"Cozy Pixar style bedtime illustration: {curr_theme}, {name}.")
            
            # Озвучка (OpenAI имеет лимит 4096 символов на один аудиофайл)
            # Если текст очень длинный, берем основной объем для озвучки
            status_text.text("Превращаем текст в голос...")
            audio_res = client.audio.speech.create(model="tts-1", voice=voice, input=full_story[:4090])

            # Финальный вывод
            st.image(img_res.data[0].url, use_container_width=True)
            st.audio(audio_res.content)
            st.markdown(f'<div class="story-output">{full_story}</div>', unsafe_allow_html=True)
            
            progress_bar.progress(100)
            status_text.text("Готово!")
            st.balloons()

        except Exception as e:
            st.error(f"Error: {e}")
