import streamlit as st
from openai import OpenAI
import requests
import streamlit.components.v1 as components
import base64
from supabase import create_client, Client

# --- 1. НАСТРОЙКИ И КЛЮЧИ ---
st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="wide")

# Вставляем ключи напрямую, чтобы точно работало
SUPABASE_URL = "https://gdyhmeshafpdttzjpxjg.supabase.co"
SUPABASE_KEY = "sb_publishable_aqJsR96WyEdflsb4LoQSzg_g2WEyWBd"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"Ошибка подключения к базе: {e}")
    st.stop()

# --- 2. СТИЛИЗАЦИЯ ИНТЕРФЕЙСА ---
st.markdown("""
    <style>
    .stApp { background: #0a0f1e; color: #f8fafc; }
    [data-testid="stSidebar"] { background-color: #111827 !important; border-right: 2px solid #38bdf8; }
    div.stButton > button { height: 70px !important; font-size: 18px !important; border-radius: 15px !important; }
    .story-output { background: #ffffff; color: #1e293b; padding: 40px; border-radius: 30px; font-size: 1.25em; line-height: 1.7; box-shadow: 0 10px 40px rgba(0,0,0,0.6); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ЛОГИКА ВХОДА И РЕГИСТРАЦИИ ---
def login_page():
    st.title("🌟 NomNom Stories")
    tab1, tab2 = st.tabs(["Вход", "Регистрация"])
    
    with tab1:
        email = st.text_input("Email", key="l_email")
        password = st.text_input("Пароль", type="password", key="l_pass")
        if st.button("Войти", type="primary", use_container_width=True):
            res = supabase.table("users").select("*").eq("email", email).eq("password", password).execute()
            if len(res.data) > 0:
                st.session_state["logged_in"] = True
                st.session_state["user_email"] = email
                st.rerun()
            else:
                st.error("Неверный email или пароль")

    with tab2:
        n_email = st.text_input("Новый Email", key="r_email")
        n_pass = st.text_input("Пароль", type="password", key="r_pass")
        if st.button("Создать аккаунт", use_container_width=True):
            try:
                supabase.table("users").insert({"email": n_email, "password": n_pass}).execute()
                st.success("Аккаунт создан! Теперь перейдите на вкладку 'Вход'")
            except Exception as e:
                st.error("Ошибка: скорее всего, этот email уже занят или таблица не настроена.")

# --- 4. ОСНОВНОЙ ФУНКЦИОНАЛ ---
if not st.session_state.get("logged_in", False):
    login_page()
else:
    # Инициализация API
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    ELEVEN_KEY = st.secrets["ELEVENLABS_API_KEY"]
    
    if 'theme_idx' not in st.session_state: st.session_state.theme_idx = 0

    with st.sidebar:
        st.success(f"Привет, {st.session_state['user_email']}!")
        VOICES = {"Марина": "ymDCYd8puC7gYjxIamPt", "Николай": "8JVbfL6oEdmuxKn5DK2C"}
        selected_voice = st.selectbox("Голос", list(VOICES.keys()))
        music_vol = st.slider("Громкость музыки", 0.0, 1.0, 0.2)
        if st.button("Выйти"):
            st.session_state["logged_in"] = False
            st.rerun()

    st.title("✨ Создай Волшебную Сказку")
    
    col1, col2 = st.columns(2)
    with col1: child_name = st.text_input("Имя ребенка", value="Даша")
    with col2: lang = st.selectbox("Язык", ["Русский", "English"])

    story_minutes = st.select_slider("⏳ Длительность", options=[3, 5, 10, 15, 20, 30], value=10)

    st.divider()
    themes = ["🛡️ Храбрость", "🍎 Привычки", "🤝 Отношения"]
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            if st.button(themes[i], key=f"t_{i}", type="primary" if st.session_state.theme_idx == i else "secondary", use_container_width=True):
                st.session_state.theme_idx = i
                st.rerun()

    details = st.text_area("✍️ О чем сегодня сказка?")

    if st.button("🚀 СОЗДАТЬ МАГИЮ ✨", type="primary", use_container_width=True):
        with st.spinner("Сказка сочиняется..."):
            try:
                curr_theme = themes[st.session_state.theme_idx]
                
                # 1. Картинка
                img_res = client.images.generate(model="dall-e-3", prompt=f"Cozy Pixar style bedtime story: {curr_theme}, child {child_name}.")
                st.image(img_res.data[0].url, use_container_width=True)

                # 2. Фоновая музыка (из твоего GitHub)
                def get_audio_html(file_path):
                    with open(file_path, "rb") as f:
                        b64 = base64.b64encode(f.read()).decode()
                        return f'<audio id="bg_music" loop><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
                
                st.markdown(get_audio_html("bg_music.mp3"), unsafe_allow_html=True)

                # 3. Текст сказки
                ch_res = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": f"Напиши сказку для {child_name} на тему {curr_theme}. Сюжет: {details}. Язык: {lang}."}]
                )
                story_text = ch_res.choices[0].message.content
                
                # 4. Озвучка (Марина)
                aud_res = requests.post(
                    f"https://api.elevenlabs.io/v1/text-to-speech/{VOICES[selected_voice]}",
                    json={"text": story_text, "model_id": "eleven_multilingual_v2"},
                    headers={"xi-api-key": ELEVEN_KEY}
                )
                
                if aud_res.status_code == 200:
                    st.audio(aud_res.content, format="audio/mp3")

                # 5. Автозапуск через JS
                components.html(f"""
                    <script>
                    setTimeout(() => {{
                        const m = window.parent.document.getElementById('bg_music');
                        const a = window.parent.document.querySelectorAll('audio');
                        if (m) {{ m.volume = {music_vol}; m.play(); }}
                        if (a[0]) a[0].play();
                    }}, 1500);
                    </script>
                """, height=0)

                st.markdown(f'<div class="story-output">{story_text}</div>', unsafe_allow_html=True)
                st.balloons()
                
            except Exception as e:
                st.error(f"Ошибка: {e}")
