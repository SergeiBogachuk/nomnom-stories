import streamlit as st
from openai import OpenAI
import requests
import streamlit.components.v1 as components

st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="wide")

# --- СТИЛЬ ---
st.markdown("""
    <style>
    .stApp { background: #0a0f1e; color: #f8fafc; }
    [data-testid="stSidebar"] { background-color: #111827 !important; border-right: 2px solid #38bdf8; }
    div.stButton > button { height: 60px !important; border-radius: 12px !important; }
    /* Прячем плеер фоновой музыки, чтобы не путать пользователя */
    .hidden-audio { display: none; }
    .story-output { background: #ffffff; color: #1e293b; padding: 40px; border-radius: 30px; font-size: 1.25em; line-height: 1.7; box-shadow: 0 10px 40px rgba(0,0,0,0.6); }
    </style>
    """, unsafe_allow_html=True)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ELEVEN_KEY = st.secrets["ELEVENLABS_API_KEY"]

VOICES = {
    "Марина (Женский)": "ymDCYd8puC7gYjxIamPt",
    "Николай (Мужской)": "8JVbfL6oEdmuxKn5DK2C"
}

# ОДНА КЛАССИЧЕСКАЯ МЕЛОДИЯ (Спокойное пианино)
CLASSIC_MUSIC = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3"

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
    st.header("Настройки")
    selected_voice = st.selectbox("Голос", list(VOICES.keys()))
    music_vol = st.slider("Громкость музыки", 0.0, 1.0, 0.2)

st.title("🌟 NomNom Stories")

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

details = st.text_area("✍️ О чем сказка сегодня?")

if st.button("✨ СОЗДАТЬ И ВКЛЮЧИТЬ СКАЗКУ ✨", type="primary", use_container_width=True):
    num_chapters = max(1, story_minutes // 3)
    with st.spinner("Магия классики и слов..."):
        try:
            curr_theme = themes[st.session_state.theme_idx]
            img_res = client.images.generate(model="dall-e-3", prompt=f"Cozy Pixar bedtime illustration: {curr_theme}, child {name}.")
            st.image(img_res.data[0].url, use_container_width=True)

            # --- СКРЫТЫЙ ПЛЕЕР МУЗЫКИ ---
            st.markdown(f'<audio id="bg_music" src="{CLASSIC_MUSIC}" loop></audio>', unsafe_allow_html=True)
            
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

            # --- JS: ЗАПУСКАЕМ МУЗЫКУ И ПЕРВУЮ ГЛАВУ ОДНОВРЕМЕННО ---
            components.html(f"""
                <script>
                setTimeout(() => {{
                    const music = window.parent.document.getElementById('bg_music');
                    const chapters = window.parent.document.querySelectorAll('audio');
                    
                    if (music) {{
                        music.volume = {music_vol};
                        music.play();
                    }}
                    
                    // Первый аудио-плеер (не считая скрытого) - это Глава 1
                    if (chapters[1]) {{
                        chapters[1].play();
                        
                        // Автопереход между главами
                        for (let i = 1; i < chapters.length - 1; i++) {{
                            chapters[i].onended = () => {{ chapters[i+1].play(); }};
                        }}
                    }}
                }}, 1000);
                </script>
            """, height=0)

            st.markdown(f'<div class="story-output">{full_story}</div>', unsafe_allow_html=True)
            st.balloons()
            
        except Exception as e:
            st.error(f"Ошибка: {e}")
