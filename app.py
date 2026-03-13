import streamlit as st
from openai import OpenAI
import requests
import streamlit.components.v1 as components

st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="centered")

# --- УЛУЧШЕННЫЙ СТИЛЬ ---
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #f8fafc; }
    
    /* Боковое меню */
    [data-testid="stSidebar"] { background-color: #1e293b; border-right: 1px solid #38bdf8; }
    
    /* Кнопки тем */
    div.stButton > button {
        height: 70px !important; font-size: 20px !important; border-radius: 15px !important;
        background-color: #1e293b !important; color: white !important; 
        border: 1px solid #334155 !important; transition: 0.3s;
    }
    div.stButton > button:hover { border-color: #38bdf8; transform: translateY(-2px); }
    
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%) !important;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.3) !important; border: none !important;
    }

    .story-output { background: #fdfbf7; color: #1e293b; padding: 35px; border-radius: 25px; font-size: 1.2em; margin-top: 20px; line-height: 1.6; border: 1px solid #e2e8f0; }
    .music-box { background: #0f172a; padding: 15px; border-radius: 15px; border: 1px solid #818cf8; margin-bottom: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ELEVEN_KEY = st.secrets["ELEVENLABS_API_KEY"]

# --- БАЗА ГОЛОСОВ (Сюда добавляй новые ID из ElevenLabs) ---
VOICES = {
    "Марина (Добрая)": "ymDCYd8puC7gYjxIamPt",
    "Johnny (Нежная)": "8JVbfL6oEdmuxKn5DK2C", # Замени на реальный ID, когда выберешь
    "Фея (Волшебная)": "flHkNRp1BlvT73UL6gyz"  # Замени на реальный ID
}

MUSIC_URLS = {
    "Без музыки": None,
    "🌙 Колыбельная": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    "🌲 Лес": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    "🌧️ Дождь": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3"
}

def generate_premium_audio(text, voice_id):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {"xi-api-key": ELEVEN_KEY, "Content-Type": "application/json"}
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.65, "similarity_boost": 0.75}
    }
    res = requests.post(url, json=data, headers=headers)
    return res.content if res.status_code == 200 else None

# --- ИНТЕРФЕЙС ---
if 'theme_idx' not in st.session_state: st.session_state.theme_idx = 0

st.title("🌙 NomNom Stories")

# Настройки в боковой панели
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3094/3094406.png", width=100)
    st.header("Настройки магии")
    
    # ВЫБОР ГОЛОСА
    selected_voice_name = st.selectbox("Кто читает сказку?", list(VOICES.keys()))
    selected_voice_id = VOICES[selected_voice_name]
    
    st.divider()
    bg_music = st.selectbox("Фоновый звук", list(MUSIC_URLS.keys()))
    music_vol = st.slider("Громкость фона", 0.0, 1.0, 0.15)

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

details = st.text_area("✍️ О чем будет сказка сегодня?")

if st.button("✨ СОЗДАТЬ ВОЛШЕБНУЮ СКАЗКУ ✨", type="primary", use_container_width=True):
    num_chapters = max(1, story_minutes // 3)
    progress_bar = st.progress(0)
    
    with st.spinner(f"{selected_voice_name} уже открывает книгу..."):
        try:
            curr_theme = themes[st.session_state.theme_idx]
            plan_res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": f"План сказки из {num_chapters} глав для {name}. Тема: {curr_theme}. Ситуация: {details}."}])
            plan = plan_res.choices[0].message.content
            
            full_story = ""
            
            # Картинка
            img_res = client.images.generate(model="dall-e-3", prompt=f"Cozy Pixar bedtime illustration: {curr_theme}, child {name}.")
            st.image(img_res.data[0].url, use_container_width=True)

            # Музыка
            if MUSIC_URLS[bg_music]:
                st.audio(MUSIC_URLS[bg_music], format="audio/mp3", loop=True)
                st.caption(f"🎵 Сейчас играет: {bg_music} (настрой громкость выше)")

            st.subheader(f"🎙️ Слушаем {selected_voice_name}:")
            
            for i in range(num_chapters):
                ch_res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": f"Напиши главу №{i+1} для {name} по плану: {plan}. Подробно. Прошлое: {full_story[-500:]}"}])
                chapter_text = ch_res.choices[0].message.content
                full_story += f"\n\n### Глава {i+1}\n" + chapter_text
                
                audio_bytes = generate_premium_audio(chapter_text, selected_voice_id)
                if audio_bytes:
                    st.write(f"📖 Глава {i+1}")
                    st.audio(audio_bytes, format="audio/mp3")
                    st.download_button(f"💾 Сохранить Главу {i+1}", audio_bytes, f"story_{i+1}.mp3", "audio/mp3")
                
                progress_bar.progress((i + 1) / num_chapters)

            # Авто-переход
            components.html("""
                <script>
                setInterval(() => {
                    const audios = window.parent.document.querySelectorAll('audio');
                    for (let i = 1; i < audios.length - 1; i++) {
                        audios[i].onended = () => { audios[i+1].play(); };
                    }
                }, 2000);
                </script>
            """, height=0)

            st.markdown(f'<div class="story-output">{full_story}</div>', unsafe_allow_html=True)
            st.balloons()
            
        except Exception as e:
            st.error(f"Ошибка: {e}")
