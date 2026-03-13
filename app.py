import streamlit as st
from openai import OpenAI
import requests
import streamlit.components.v1 as components

st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="wide")

# --- СТИЛЬ (Фикс исчезновения контента) ---
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #f8fafc; }
    [data-testid="stSidebar"] { background-color: #1e293b; }
    
    div.stButton > button {
        height: 70px !important; font-size: 20px !important; border-radius: 15px !important;
        background-color: #1e293b !important; color: white !important; 
    }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%) !important;
        border: none !important;
    }
    .story-output { background: #fdfbf7; color: #1e293b; padding: 35px; border-radius: 25px; font-size: 1.2em; margin-top: 20px; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ELEVEN_KEY = st.secrets["ELEVENLABS_API_KEY"]

VOICES = {
    "Марина ": "ymDCYd8puC7gYjxIamPt",
    "Papa ": "8JVbfL6oEdmuxKn5DK2C"
}

# Ссылки на более качественную музыку
MUSIC_URLS = {
    "🌙 Волшебная колыбельная": "https://www.mboxdrive.com/lullaby_piano.mp3",
    "🌲 Глубокий лес": "https://www.mboxdrive.com/forest_night.mp3",
    "🌧️ Уютный дождь": "https://www.mboxdrive.com/soft_rain.mp3",
    "✨ Без музыки": None
}

def generate_premium_audio(text, voice_id):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {"xi-api-key": ELEVEN_KEY, "Content-Type": "application/json"}
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.7, "similarity_boost": 0.75}
    }
    res = requests.post(url, json=data, headers=headers)
    return res.content if res.status_code == 200 else None

# --- ИНТЕРФЕЙС ---
if 'theme_idx' not in st.session_state: st.session_state.theme_idx = 0
if 'generated' not in st.session_state: st.session_state.generated = False

st.title("🌙 NomNom Stories")

with st.sidebar:
    st.header("🎭 Мастерская")
    selected_voice = st.selectbox("Голос", list(VOICES.keys()))
    bg_music = st.selectbox("Фоновая музыка", list(MUSIC_URLS.keys()))
    st.info("💡 Если хочешь сменить музыку, выбери её ДО генерации сказки.")

col1, col2 = st.columns(2)
with col1: name = st.text_input("Имя ребенка", value="Даша")
with col2: lang = st.selectbox("Язык", ["Русский", "English"])

story_minutes = st.select_slider("⏳ Длительность", options=[3, 5, 10, 15, 20, 30, 45, 60], value=10)

st.divider()
themes = ["🛡️ Храбрость", "🍎 Привычки", "🤝 Отношения"]
cols = st.columns(3)
for i in range(3):
    with cols[i]:
        if st.button(themes[i], key=f"t_{i}", type="primary" if st.session_state.theme_idx == i else "secondary", use_container_width=True):
            st.session_state.theme_idx = i
            st.rerun()

details = st.text_area("✍️ О чем расскажем сегодня?")

# КНОПКА ЗАПУСКА
if st.button("✨ СОЗДАТЬ И ВКЛЮЧИТЬ СКАЗКУ ✨", type="primary", use_container_width=True):
    num_chapters = max(1, story_minutes // 3)
    
    with st.spinner("Марина и эльфы готовят сказку..."):
        try:
            curr_theme = themes[st.session_state.theme_idx]
            plan_res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": f"План сказки из {num_chapters} глав для {name}. Тема: {curr_theme}. Ситуация: {details}."}])
            plan = plan_res.choices[0].message.content
            
            # Картинка
            img_res = client.images.generate(model="dall-e-3", prompt=f"Cozy Pixar bedtime illustration: {curr_theme}, child {name}.")
            st.image(img_res.data[0].url, use_container_width=True)

            # --- МУЗЫКА И ГОЛОС (Автозапуск через JS) ---
            audio_html = ""
            if MUSIC_URLS[bg_music]:
                audio_html += f'<audio id="bg_music" src="{MUSIC_URLS[bg_music]}" loop></audio>'
            
            full_story = ""
            for i in range(num_chapters):
                ch_res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": f"Напиши главу №{i+1} для {name} по плану: {plan}. Подробно. Прошлое: {full_story[-500:]}"}])
                chapter_text = ch_res.choices[0].message.content
                full_story += f"\n\n### Глава {i+1}\n" + chapter_text
                
                audio_bytes = generate_premium_audio(chapter_text, VOICES[selected_voice])
                if audio_bytes:
                    st.write(f"📖 Глава {i+1}")
                    st.audio(audio_bytes, format="audio/mp3")

            # МАГИЧЕСКИЙ СКРИПТ: включает музыку сразу и переключает главы
            components.html(f"""
                <script>
                const audios = window.parent.document.querySelectorAll('audio');
                if (audios.length > 0) {{
                    // Включаем музыку (она первая в списке)
                    audios[0].volume = 0.15;
                    audios[0].play();
                    
                    // Включаем первую главу (она вторая)
                    if (audios[1]) audios[1].play();
                    
                    // Настройка автоперехода между главами
                    for (let i = 1; i < audios.length - 1; i++) {{
                        audios[i].onended = () => {{ audios[i+1].play(); }};
                    }}
                }}
                </script>
            """, height=0)

            st.markdown(f'<div class="story-output">{full_story}</div>', unsafe_allow_html=True)
            st.balloons()
            
        except Exception as e:
            st.error(f"Ошибка: {e}")
