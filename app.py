import streamlit as st
from openai import OpenAI
import requests
import streamlit.components.v1 as components
import base64
from supabase import create_client, Client

# --- 1. ПОДКЛЮЧЕНИЕ К БАЗЕ ---
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="wide")

# --- 2. ЛОГИКА РЕГИСТРАЦИИ И ВХОДА ---
def login_page():
    st.title("🌙 Добро пожаловать в NomNom Stories")
    
    tab1, tab2 = st.tabs(["Вход", "Регистрация"])
    
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Пароль", type="password", key="login_pass")
        if st.button("Войти", type="primary"):
            # Проверяем пользователя в базе
            res = supabase.table("users").select("*").eq("email", email).eq("password", password).execute()
            if len(res.data) > 0:
                st.session_state["logged_in"] = True
                st.session_state["user_email"] = email
                st.rerun()
            else:
                st.error("Неверный email или пароль")

    with tab2:
        new_email = st.text_input("Новый Email", key="reg_email")
        new_password = st.text_input("Придумайте пароль", type="password", key="reg_pass")
        confirm_pass = st.text_input("Повторите пароль", type="password", key="reg_confirm")
        
        if st.button("Создать аккаунт"):
            if new_password != confirm_pass:
                st.error("Пароли не совпадают")
            elif len(new_password) < 6:
                st.warning("Пароль должен быть не менее 6 символов")
            else:
                try:
                    supabase.table("users").insert({"email": new_email, "password": new_password}).execute()
                    st.success("Аккаунт создан! Теперь войдите во вкладке 'Вход'")
                except:
                    st.error("Этот email уже зарегистрирован")

# --- 3. ОСНОВНОЕ ПРИЛОЖЕНИЕ ---
if not st.session_state.get("logged_in", False):
    login_page()
else:
    # Твой основной "Скелет" приложения
    with st.sidebar:
        st.success(f"Вы вошли как: {st.session_state['user_email']}")
        if st.button("Выйти"):
            st.session_state["logged_in"] = False
            st.rerun()
        
        st.divider()
        VOICES = {"Марина (Женский)": "ymDCYd8puC7gYjxIamPt", "Николай (Мужской)": "8JVbfL6oEdmuxKn5DK2C"}
        selected_voice = st.selectbox("Голос", list(VOICES.keys()))
        music_vol = st.slider("Громкость музыки", 0.0, 1.0, 0.2)

    # (Далее идет твой код генерации сказки, OpenAI и музыки, который мы отладили)
    st.title("🌟 Создай свою сказку")
    
    # ... (весь остальной функционал генерации остается прежним)
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    ELEVEN_KEY = st.secrets["ELEVENLABS_API_KEY"]
    
    name = st.text_input("Имя ребенка", value="Даша")
    details = st.text_area("О чем сегодня расскажем?")
    
    if st.button("✨ СГЕНЕРИРОВАТЬ ✨", type="primary", use_container_width=True):
        with st.spinner("Магия в процессе..."):
            # Код генерации сказки...
            try:
                # Генерируем текст и звук как раньше
                st.write("Сказка создается для тебя...")
                # ... (здесь твой рабочий код генерации)
                st.balloons()
            except Exception as e:
                st.error(f"Ошибка: {e}")
