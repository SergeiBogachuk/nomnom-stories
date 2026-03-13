import streamlit as st
from openai import OpenAI
import requests
import streamlit.components.v1 as components

st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="wide")

# --- ВОЗВРАЩАЕМ КРАСИВЫЙ СТИЛЬ И КНОПКИ ---
st.markdown("""
    <style>
    .stApp { background: #0a0f1e; color: #f8fafc; }
    [data-testid="stSidebar"] { background-color: #111827 !important; border-right: 2px solid #38bdf8; }
    
    div.stButton > button {
        height: 65px !important; font-size: 18px !important; border-radius: 12px !important;
        background-color: #1e293b !important; color: white !important; border: 1px solid #334155 !important;
    }
    
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%) !important;
        border: none !important; box-shadow: 0 4px 20px rgba(56, 189, 248, 0.4) !important;
    }

    .story-output { background: #ffffff; color: #1e293b; padding: 40px; border-radius: 30px; font-size: 1.25em; line-height: 1.7; box-shadow: 0 10px 40px rgba(0,0,0,0.6); }
    </style>
    """, unsafe_allow_html=True)

# Ключи
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ELEVEN_KEY = st.secrets["ELEVENLABS_API_KEY"]

VOICES = {
    "Марина (Женский)": "ymDCYd8puC7gYjxIamPt",
    "Николай (Мужской)": "8JVbfL6oEdmuxKn5DK2C"
}

# Используем самые надежные ссылки на музыку
MUSIC_URLS = {
    "🌙 Волшебная колыбельная": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    "🌲 Глубокий лес": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    "🌧️ Уютный дождь": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3"
}

def generate_premium_audio(text, voice_id):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {"xi-api-key": ELEVEN_KEY, "Content-Type": "application/json"}
    data = {"text": text, "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.6, "similarity_boost": 0.8}}
    try:
        res = requests.post(url, json=data, headers=headers)
        return res.content if res.status_code == 200 else None
    except: return None

# --- ИНТЕРФЕЙС ---
if 'theme_idx' not in st.session_state: st.session_state.theme_idx = 0

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3094/3094406.png", width=80)
    st.header("Настройки")
    selected_voice = st.selectbox("Голос", list(VOICES.keys()))
    bg_music = st.selectbox("Музыка", list(MUSIC_URLS.keys()))
    music_vol = st.slider("Громкость музыки", 0.1, 1.0, 0.4)

st.title("🌟 NomNom Stories")

col1, col2 = st.columns(2)
with col1: name = st.text_input("Имя ребенка", value="Даша")
with col2: lang = st.selectbox("Язык", ["Русский", "English"])

story_minutes = st.select_slider("⏳ Длительность", options=[3, 5, 10, 15, 20, 30, 45, 60], value=10)

# ВОЗВРАЩАЕМ КНОПКИ НАВЫКОВ
st.divider()
themes = ["🛡️ Храбрость", "🍎 Привычки", "🤝 Отношения"]
cols = st.columns(3)
for i in range(3):
    with cols[i]:
        active = "primary" if st.session_state.theme_idx == i else "secondary"
        if st.button(themes[i], key=f"t_{i}", type=active, use_container_width=True):
            st.session_state.theme_idx = i
            st.rerun()

details = st.text_area("✍️ Добавь деталей:")

if st.button("✨ СОЗДАТЬ МАГИЮ ✨", type="primary", use_container_width=True):
    num_chapters = max(1, story_minutes // 3)
    with st.spinner("Создаем сказку..."):
        try:
            curr_theme = themes[st.session_state.theme_idx]
            
            # Картинка
            img_res = client.images.generate(model="dall-e-3", prompt=f"Cozy Pixar illustration: {curr_theme}, child {name}.")
            st.image(img_res.data[0].url, use_container_width=True)

            # Музыка
            st.audio(MUSIC_URLS[bg_music], format="audio/mp3", loop=True)
            
            full_story = ""
            for i in range(num_chapters):
                st.write(f"📖 Глава {i+1}...")
                ch_res = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": f"Напиши главу {i+1} сказки для {name} на тему {curr_theme}. Прошлое: {full_story[-500:]}"}]
                )
                chapter_text = ch_res.choices[0].message.content
                full_story += f"\n\n### Глава {i+1}\n" + chapter_text
                
                audio_bytes = generate_premium_audio(chapter_text, VOICES[selected_voice])
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/mp3")

            # Автозапуск
            components.html(f"""
                <script>
                const audios = window.parent.document.querySelectorAll('audio');
                if (audios.length > 0) {{
                    audios[0].volume = {music_vol};
                    audios[0].play();
                    if (audios[1]) audios[1].play();
                    for (let i = 1; i < audios.length - 1; i++) {{
                        audios[i].onended = () => {{ audios[i+1].play(); }};
                    }}
                }}
                </script>
            """, height=0)

            st.markdown(f'<div class="story-output">{full_story}</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Ошибка: {e}")
