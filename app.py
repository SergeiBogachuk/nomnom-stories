import streamlit as st
from openai import OpenAI
import requests
import streamlit.components.v1 as components
import base64

st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="wide")

# --- 1. СИСТЕМА ВХОДА ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    
    if st.session_state["password_correct"]:
        return True

    def password_entered():
        if st.session_state["username"] in st.secrets["passwords"] and \
           st.session_state["password"] == st.secrets["passwords"][st.session_state["username"]]:
            st.session_state["password_correct"] = True
            st.session_state["display_name"] = st.session_state["username"]
            # Очищаем временные поля
            del st.session_state["password"]
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False
            st.error("😕 Неверный логин или пароль")

    st.title("🔑 Вход в NomNom Stories")
    st.text_input("Логин", key="username")
    st.text_input("Пароль", type="password", key="password")
    st.button("Войти", on_click=password_entered)
    return False

# --- 2. ЗАПУСК ПРИЛОЖЕНИЯ ПОСЛЕ ВХОДА ---
if check_password():
    
    # Инициализация OpenAI
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    ELEVEN_KEY = st.secrets["ELEVENLABS_API_KEY"]

    if 'theme_idx' not in st.session_state: st.session_state.theme_idx = 0

    # Настройки в боковой панели
    with st.sidebar:
        # Проверка на наличие имени, чтобы не было KeyError
        user_name = st.session_state.get("display_name", "Друг")
        st.success(f"Привет, **{user_name}**!")
        
        st.header("Настройки звука")
        VOICES = {
            "Марина (Женский)": "ymDCYd8puC7gYjxIamPt", 
            "Николай (Мужской)": "8JVbfL6oEdmuxKn5DK2C"
        }
        selected_voice = st.selectbox("Голос рассказачика", list(VOICES.keys()))
        music_vol = st.slider("Громкость музыки", 0.0, 1.0, 0.25)
        
        st.divider()
        if st.button("Выйти"):
            st.session_state["password_correct"] = False
            st.rerun()

    # Стиль
    st.markdown("""
        <style>
        .stApp { background: #0a0f1e; color: #f8fafc; }
        [data-testid="stSidebar"] { background-color: #111827 !important; border-right: 2px solid #38bdf8; }
        div.stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%) !important;
            border: none !important;
        }
        .story-output { background: #ffffff; color: #1e293b; padding: 40px; border-radius: 30px; font-size: 1.25em; line-height: 1.7; color: black !important; }
        </style>
        """, unsafe_allow_html=True)

    def get_audio_html(file_path):
        try:
            with open(file_path, "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                return f'<audio id="bg_music" loop><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
        except: return ""

    st.title("🌟 NomNom Stories")
    
    col1, col2 = st.columns(2)
    with col1: child_name = st.text_input("Имя ребенка", value="Даша")
    with col2: lang = st.selectbox("Язык", ["Русский", "English"])

    story_minutes = st.select_slider("⏳ Длительность (мин)", options=[3, 5, 10, 15, 20, 30], value=10)

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

    if st.button("✨ СОЗДАТЬ МАГИЧЕСКУЮ СКАЗКУ ✨", type="primary", use_container_width=True):
        num_chapters = max(1, story_minutes // 3)
        with st.spinner("Сказка создается..."):
            try:
                curr_theme = themes[st.session_state.theme_idx]
                
                # Картинка
                img_res = client.images.generate(model="dall-e-3", prompt=f"Cozy Pixar illustration, child {child_name}, thematic: {curr_theme}.")
                st.image(img_res.data[0].url, use_container_width=True)

                # Музыка
                music_html = get_audio_html("bg_music.mp3")
                st.markdown(music_html, unsafe_allow_html=True)
                
                full_story = ""
                for i in range(num_chapters):
                    st.write(f"📖 Глава {i+1}...")
                    ch_res = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": f"Напиши главу {i+1} сказки для {child_name} на тему {curr_theme}. Язык: {lang}."}]
                    )
                    chapter_text = ch_res.choices[0].message.content
                    full_story += f"\n\n### Глава {i+1}\n" + chapter_text
                    
                    # Озвучка ElevenLabs
                    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICES[selected_voice]}"
                    headers = {"xi-api-key": ELEVEN_KEY, "Content-Type": "application/json"}
                    data = {"text": chapter_text, "model_id": "eleven_multilingual_v2"}
                    audio_res = requests.post(url, json=data, headers=headers)
                    
                    if audio_res.status_code == 200:
                        st.audio(audio_res.content, format="audio/mp3")

                components.html(f"""
                    <script>
                    setTimeout(() => {{
                        const music = window.parent.document.getElementById('bg_music');
                        const audios = window.parent.document.querySelectorAll('audio');
                        if (music) {{ music.volume = {music_vol}; music.play(); }}
                        if (audios[0]) audios[0].play();
                        for (let i = 0; i < audios.length - 1; i++) {{
                            audios[i].onended = () => {{ audios[i+1].play(); }};
                        }}
                    }}, 1500);
                    </script>
                """, height=0)

                st.markdown(f'<div class="story-output">{full_story}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Ошибка: {e}")
