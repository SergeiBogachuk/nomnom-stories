import streamlit as st
from openai import OpenAI
import requests
import streamlit.components.v1 as components
import base64
from supabase import create_client, Client

# --- 1. НАСТРОЙКИ ---
st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="wide")

URL = "https://gdyhmeshafpdttzjpxjg.supabase.co"
KEY = "sb_publishable_aqJsR96WyEdflsb4LoQSzg_g2WEyWBd"

try:
    supabase: Client = create_client(URL, KEY)
except:
    st.error("Ошибка базы данных")
    st.stop()

# --- 2. СТИЛЬ (ИСПРАВЛЕННЫЕ КНОПКИ) ---
st.markdown("""
    <style>
    .stApp { background: #0a0f1e; color: #f8fafc; }
    [data-testid="stSidebar"] { background-color: #111827 !important; border-right: 2px solid #38bdf8; }
    
    /* Исправляем кнопки тем */
    div.stButton > button { 
        height: 70px !important; 
        border-radius: 15px !important; 
        font-weight: bold !important;
        color: white !important; /* Текст всегда белый */
        border: 1px solid #38bdf8 !important;
    }
    
    /* Цвет активной кнопки */
    div.stButton > button[kind="primary"] {
        background: #ef4444 !important; /* Красный как на скрине */
    }
    
    /* Цвет неактивной кнопки */
    div.stButton > button[kind="secondary"] {
        background: #1e293b !important;
        color: #94a3b8 !important;
    }

    .story-output { background: #ffffff; color: #1e293b !important; padding: 40px; border-radius: 30px; font-size: 1.25em; line-height: 1.7; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ФУНКЦИИ ---
def login_user(email):
    st.session_state["logged_in"] = True
    st.session_state["user_email"] = email
    st.rerun()

# --- 4. СТРАНИЦА ВХОДА ---
if not st.session_state.get("logged_in", False):
    st.title("🌟 NomNom Stories")
    tab1, tab2 = st.tabs(["Вход", "Регистрация"])
    with tab1:
        email = st.text_input("Email", key="l_email")
        password = st.text_input("Пароль", type="password", key="l_pass")
        if st.button("Войти", type="primary", use_container_width=True):
            res = supabase.table("users").select("*").eq("email", email).eq("password", password).execute()
            if len(res.data) > 0: login_user(email)
            else: st.error("Ошибка входа")
    with tab2:
        n_email = st.text_input("Новый Email", key="r_email")
        n_pass = st.text_input("Пароль", type="password", key="r_pass")
        if st.button("Создать аккаунт и войти", use_container_width=True):
            try:
                supabase.table("users").insert({"email": n_email, "password": n_pass}).execute()
                login_user(n_email)
            except: st.error("Email занят")
else:
    # ГЛАВНЫЙ ЭКРАН
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    ELEVEN_KEY = st.secrets["ELEVENLABS_API_KEY"]
    if 'theme_idx' not in st.session_state: st.session_state.theme_idx = 0

    with st.sidebar:
        st.success(f"Привет, {st.session_state['user_email']}")
        VOICES = {"Марина": "ymDCYd8puC7gYjxIamPt", "Николай": "8JVbfL6oEdmuxKn5DK2C"}
        selected_voice = st.selectbox("Голос", list(VOICES.keys()))
        music_vol = st.slider("Громкость музыки", 0.0, 1.0, 0.2)
        if st.button("Выйти"):
            st.session_state["logged_in"] = False
            st.rerun()

    st.title("✨ Создай Сказку")
    child_name = st.text_input("Имя ребенка", value="Даша")
    lang = st.selectbox("Язык", ["Русский", "English"])
    
    st.divider()
    themes = ["🛡️ Храбрость", "🍎 Привычки", "🤝 Отношения"]
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            t_type = "primary" if st.session_state.theme_idx == i else "secondary"
            if st.button(themes[i], key=f"t_{i}", type=t_type, use_container_width=True):
                st.session_state.theme_idx = i
                st.rerun()

    details = st.text_area("✍️ О чем сегодня сказка?")

    if st.button("🚀 СОЗДАТЬ МАГИЮ ✨", type="primary", use_container_width=True):
        with st.spinner("Сочиняем и сохраняем в базу..."):
            try:
                curr_theme = themes[st.session_state.theme_idx]
                
                # Картинка
                img_res = client.images.generate(model="dall-e-3", prompt=f"Pixar style, {curr_theme}, child {child_name}.")
                img_url = img_res.data[0].url
                st.image(img_url, use_container_width=True)

                # Текст
                ch_res = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": f"Напиши сказку для {child_name} на тему {curr_theme}. Сюжет: {details}. Язык: {lang}."}]
                )
                story_text = ch_res.choices[0].message.content

                # --- СОХРАНЕНИЕ В БАЗУ (НОВОЕ!) ---
                supabase.table("stories").insert({
                    "user_email": st.session_state["user_email"],
                    "child_name": child_name,
                    "theme": curr_theme,
                    "story_text": story_text,
                    "image_url": img_url
                }).execute()

                # Озвучка
                aud_res = requests.post(
                    f"https://api.elevenlabs.io/v1/text-to-speech/{VOICES[selected_voice]}",
                    json={"text": story_text, "model_id": "eleven_multilingual_v2"},
                    headers={"xi-api-key": ELEVEN_KEY}
                )
                if aud_res.status_code == 200:
                    st.audio(aud_res.content, format="audio/mp3")

                st.markdown(f'<div class="story-output">{story_text}</div>', unsafe_allow_html=True)
                st.success("✅ Сказка сохранена в твою личную библиотеку!")
                
            except Exception as e:
                st.error(f"Ошибка: {e}")
