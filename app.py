import streamlit as st
from openai import OpenAI
import requests
import streamlit.components.v1 as components

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
    .music-box { background: #1e293b; padding: 15px; border-radius: 15px; border: 1px solid #38bdf8; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ELEVEN_KEY = st.secrets["ELEVENLABS_API_KEY"]

# Прямые ссылки на приятную фоновую музыку (без авторских прав)
MUSIC_URLS = {
    "Без музыки": None,
    "🌙 Колыбельная (Пианино)": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", # Пример ссылки
    "🌲 Звуки леса": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    "🌧️ Легкий дождь": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3"
}

def generate_premium_audio(text):
    VOICE_ID = "ymDCYd8puC7gYjxIamPt" # Марина
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {"xi-api-key": ELEVEN_KEY, "Content-Type": "application/json"}
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.6, "similarity_boost": 0.8}
    }
    res = requests.post(url, json=data, headers=headers)
    return res.content if res.status_code == 200 else None

# --- ИНТЕРФЕЙС ---
if 'theme_idx' not in st.session_state: st.session_state.theme_idx = 0

st.title("🌟 NomNom Stories")

with st.sidebar:
    st.header("⚙️ Настройки атмосферы")
    bg_music = st.selectbox("Фоновая музыка", list(MUSIC_URLS.keys()))
    music_volume = st.slider("Громкость музыки", 0.0, 1.0, 0.2)

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

if st.button("✨ СОЗДАТЬ МАГИЧЕСКУЮ СКАЗКУ ✨", type="primary", use_container_width=True):
    num_chapters = max(1, story_minutes // 3)
    progress_bar = st.progress(0)
    
    with st.spinner(f"Марина и музыканты готовят сказку..."):
        try:
            curr_theme = themes[st.session_state.theme_idx]
            plan_res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": f"План сказки из {num_chapters} глав для {name}. Тема: {curr_theme}. Ситуация: {details}. Язык: {lang}."}])
            plan = plan_res.choices[0].message.content
            
            full_story = ""
            
            # Картинка
            img_res = client.images.generate(model="dall-e-3", prompt=f"Cozy bedtime story illustration: {curr_theme}, child {name}, soft light.")
            st.image(img_res.data[0].url, use_container_width=True)

            # Фоновая музыка (если выбрана)
            if MUSIC_URLS[bg_music]:
                st.markdown(f'<div class="music-box">🎵 Фоновое сопровождение: {bg_music}</div>', unsafe_allow_html=True)
                st.audio(MUSIC_URLS[bg_music], format="audio/mp3", loop=True)

            st.subheader("🎙️ Главы сказки (играют по очереди):")
            
            for i in range(num_chapters):
                ch_res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": f"Напиши главу №{i+1} для {name} по плану: {plan}. ОЧЕНЬ ПОДРОБНО. Прошлое: {full_story[-500:]}"}])
                chapter_text = ch_res.choices[0].message.content
                full_story += f"\n\n### Глава {i+1}\n" + chapter_text
                
                audio_bytes = generate_premium_audio(chapter_text)
                if audio_bytes:
                    st.write(f"**Глава {i+1}**")
                    st.audio(audio_bytes, format="audio/mp3")
                    # Кнопка скачать для каждой главы
                    st.download_button(label=f"💾 Скачать Главу {i+1}", data=audio_bytes, file_name=f"story_{name}_chapter_{i+1}.mp3", mime="audio/mp3")
                
                progress_bar.progress((i + 1) / num_chapters)

            # JavaScript для авто-перехода
            components.html(f"""
                <script>
                const playNext = () => {{
                    const audios = window.parent.document.querySelectorAll('audio');
                    // Индекс 0 - это музыка, начинаем со 1
                    for (let i = 1; i < audios.length - 1; i++) {{
                        audios[i].onended = () => {{
                            audios[i+1].play();
                        }};
                    }}
                }};
                setInterval(playNext, 2000);
                </script>
            """, height=0)

            st.markdown(f'<div class="story-output">{full_story}</div>', unsafe_allow_html=True)
            st.balloons()
            
        except Exception as e:
            st.error(f"Ошибка: {e}")
