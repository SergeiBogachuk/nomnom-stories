import streamlit as st
import google.generativeai as genai
import requests
import streamlit.components.v1 as components

# 1. Настройка Gemini (Твой новый мозг приложения)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="wide")

# --- ПРЕМИУМ ДИЗАЙН (Без серого браузерного стиля) ---
st.markdown("""
    <style>
    .stApp { background: #0a0f1e; color: #f8fafc; }
    
    /* Стилизация боковой панели */
    [data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 2px solid #38bdf8;
    }
    [data-testid="stSidebar"] .stMarkdown h2 { color: #38bdf8; font-family: 'Arial', sans-serif; }
    
    /* Кнопки тем */
    div.stButton > button {
        height: 60px !important; 
        font-size: 18px !important; 
        border-radius: 12px !important;
        background-color: #1e293b !important; 
        color: white !important; 
        border: 1px solid #334155 !important;
    }
    
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%) !important;
        box-shadow: 0 4px 20px rgba(56, 189, 248, 0.4) !important;
        border: none !important;
    }

    /* Окно выдачи сказки */
    .story-output { 
        background: #ffffff; 
        color: #1e293b; 
        padding: 40px; 
        border-radius: 30px; 
        font-size: 1.25em; 
        margin-top: 25px; 
        line-height: 1.7; 
        box-shadow: 0 10px 40px rgba(0,0,0,0.6);
        font-family: 'Georgia', serif;
    }
    </style>
    """, unsafe_allow_html=True)

# Ключ ElevenLabs (оставляем старый)
ELEVEN_KEY = st.secrets["ELEVENLABS_API_KEY"]

VOICES = {
    "Марина (Женский)": "ymDCYd8puC7gYjxIamPt",
    "Николай (Мужской)": "8JVbfL6oEdmuxKn5DK2C"
}

# Надежные ссылки на музыку (теперь точно без Error)
MUSIC_URLS = {
    "🌙 Волшебная колыбельная": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    "🌲 Глубокий лес": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    "🌧️ Уютный дождь": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3"
}

def generate_premium_audio(text, voice_id):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {"xi-api-key": ELEVEN_KEY, "Content-Type": "application/json"}
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.6, "similarity_boost": 0.8}
    }
    try:
        res = requests.post(url, json=data, headers=headers)
        return res.content if res.status_code == 200 else None
    except:
        return None

# --- ИНТЕРФЕЙС ---
if 'theme_idx' not in st.session_state: st.session_state.theme_idx = 0

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3094/3094406.png", width=80)
    st.header("Настройки")
    selected_voice = st.selectbox("Кто рассказывает?", list(VOICES.keys()))
    bg_music = st.selectbox("Фоновая музыка", list(MUSIC_URLS.keys()))
    music_vol = st.slider("Громкость музыки", 0.1, 1.0, 0.5)

st.title("🌟 NomNom Stories")
st.write("Создаем персональную сказку с помощью **Gemini**")

col1, col2 = st.columns(2)
with col1: name = st.text_input("Имя ребенка", value="Даша")
with col2: lang = st.selectbox("Язык", ["Русский", "English"])

story_minutes = st.select_slider("⏳ Длительность", options=[3, 5, 10, 15, 20, 30, 45, 60], value=10)

st.divider()
themes = ["🛡️ Храбрость", "🍎 Привычки", "🤝 Отношения"]
cols = st.columns(3)
for i in range(3):
    with cols[i]:
        active = "primary" if st.session_state.theme_idx == i else "secondary"
        if st.button(themes[i], key=f"t_{i}", type=active, use_container_width=True):
            st.session_state.theme_idx = i
            st.rerun()

details = st.text_area("✍️ Опиши ситуацию сегодня:")

if st.button("✨ СОЗДАТЬ И ВКЛЮЧИТЬ СКАЗКУ ✨", type="primary", use_container_width=True):
    num_chapters = max(1, story_minutes // 3)
    
    with st.spinner("Gemini сочиняет сказку, а Марина разогревает голос..."):
        try:
            curr_theme = themes[st.session_state.theme_idx]
            
            # 1. План через Gemini
            plan_prompt = f"Напиши план длинной сказки из {num_chapters} глав для {name}. Тема: {curr_theme}. Ситуация: {details}. Язык: {lang}."
            plan_res = model.generate_content(plan_prompt)
            plan = plan_res.text
            
            # Картинка
            img_res = client.images.generate(model="dall-e-3", prompt=f"Cozy Pixar bedtime illustration: {curr_theme}, child {name}.")
            st.image(img_res.data[0].url, use_container_width=True)

            # Фоновая музыка
            st.audio(MUSIC_URLS[bg_music], format="audio/mp3", loop=True)
            
            full_story = ""
            for i in range(num_chapters):
                st.write(f"📖 Записываем главу {i+1}...")
                ch_prompt = f"Напиши главу №{i+1} сказки для {name} по этому плану: {plan}. Пиши МАКСИМАЛЬНО МНОГО текста. Язык: {lang}. Прошлое: {full_story[-500:]}"
                ch_res = model.generate_content(ch_prompt)
                chapter_text = ch_res.text
                full_story += f"\n\n### Глава {i+1}\n" + chapter_text
                
                audio_bytes = generate_premium_audio(chapter_text, VOICES[selected_voice])
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/mp3")

            # СКРИПТ АВТОЗАПУСКА (Музыка + Голос по цепочке)
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
            st.balloons()
            
        except Exception as e:
            st.error(f"Произошла ошибка: {e}")
