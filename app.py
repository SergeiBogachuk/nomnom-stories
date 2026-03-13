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

def get_audio_bytes(text):
    VOICE_ID = "ymDCYd8puC7gYjxIamPt" # Марина
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
        return None
    except:
        return None

# --- ИНТЕРФЕЙС ---
if 'theme_idx' not in st.session_state: st.session_state.theme_idx = 0

st.title("🌟 NomNom Stories")

col1, col2 = st.columns(2)
with col1: name = st.text_input("Имя ребенка", value="Даша")
with col2: lang = st.selectbox("Язык", ["Русский", "English"])

story_minutes = st.select_slider("⏳ Длительность (минуты)", options=[3, 5, 10, 15, 20, 30, 45, 60], value=15)

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
    num_chapters = max(1, story_minutes // 3)
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    with st.spinner(f"Марина готовит сказку на {story_minutes} минут..."):
        try:
            curr_theme = themes[st.session_state.theme_idx]
            
            # 1. План
            plan_res = client.chat.completions.create(
                model="gpt-4o", 
                messages=[{"role": "user", "content": f"План длинной сказки из {num_chapters} глав для {name}. Тема: {curr_theme}. Ситуация: {details}. Язык: {lang}."}]
            )
            plan = plan_res.choices[0].message.content
            
            full_story = ""
            combined_audio = b"" # ТУТ СОБИРАЕМ ВЕСЬ ЗВУК
            
            # 2. Поочередная генерация
            for i in range(num_chapters):
                status_text.text(f"🖋️ Пишем и озвучиваем главу {i+1} из {num_chapters}...")
                
                ch_res = client.chat.completions.create(
                    model="gpt-4o", 
                    messages=[{"role": "user", "content": f"Напиши главу №{i+1} сказки по плану: {plan}. Пиши МАКСИМАЛЬНО МНОГО текста. Если последняя - ласковый вывод. Прошлое: {full_story[-500:]}"}]
                )
                chapter_text = ch_res.choices[0].message.content
                full_story += f"\n\n### Глава {i+1}\n" + chapter_text
                
                # Добавляем аудио кусочек в общий файл
                audio_part = get_audio_bytes(chapter_text)
                if audio_part:
                    combined_audio += audio_part
                
                progress_bar.progress((i + 1) / num_chapters)

            status_text.text("✅ Всё готово! Приятного прослушивания.")

            # Картинка
            img_res = client.images.generate(model="dall-e-3", prompt=f"Bedtime story: {curr_theme}, child {name}, cozy.")
            st.image(img_res.data[0].url, use_container_width=True)

            # ОДИН ПЛЕЕР ДЛЯ ВСЕГО
            if combined_audio:
                st.subheader("🎙️ Слушать сказку целиком:")
                st.audio(combined_audio, format="audio/mp3")
            
            st.markdown(f'<div class="story-output">{full_story}</div>', unsafe_allow_html=True)
            st.balloons()
            
        except Exception as e:
            st.error(f"Ошибка: {e}")
