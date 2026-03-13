import streamlit as st
from openai import OpenAI
import requests
import streamlit.components.v1 as components
import base64
from supabase import create_client, Client

st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="wide")

# --- ПРОВЕРКА КЛЮЧЕЙ (ДИАГНОСТИКА) ---
if "SUPABASE_URL" not in st.secrets or "SUPABASE_KEY" not in st.secrets:
    st.error("🚨 Ошибка: Ключи Supabase не найдены в Secrets!")
    st.write("Доступные ключи:", list(st.secrets.keys())) # Поможет нам понять, что видит приложение
    st.stop()

# Подключение к базе
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- ЛОГИКА РЕГИСТРАЦИИ ---
def login_page():
    st.title("🌙 NomNom Stories")
    tab1, tab2 = st.tabs(["Вход", "Регистрация"])
    
    with tab1:
        email = st.text_input("Email", key="l_email")
        password = st.text_input("Пароль", type="password", key="l_pass")
        if st.button("Войти", type="primary"):
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
        if st.button("Создать аккаунт"):
            try:
                supabase.table("users").insert({"email": n_email, "password": n_pass}).execute()
                st.success("Готово! Теперь войдите во вкладке 'Вход'")
            except Exception as e:
                st.error(f"Ошибка: {e}")

# --- ОСНОВНОЙ КОД ---
if not st.session_state.get("logged_in", False):
    login_page()
else:
    with st.sidebar:
        st.success(f"Привет, {st.session_state['user_email']}")
        if st.button("Выйти"):
            st.session_state["logged_in"] = False
            st.rerun()
        
        st.divider()
        VOICES = {"Марина": "ymDCYd8puC7gYjxIamPt", "Николай": "8JVbfL6oEdmuxKn5DK2C"}
        selected_voice = st.selectbox("Голос", list(VOICES.keys()))
        music_vol = st.slider("Громкость музыки", 0.0, 1.0, 0.2)

    # Клиенты API
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    ELEVEN_KEY = st.secrets["ELEVENLABS_API_KEY"]

    st.title("🌟 Создай свою сказку")
    name = st.text_input("Имя ребенка", value="Даша")
    details = st.text_area("О чем сегодня расскажем?")
    
    if st.button("✨ СГЕНЕРИРОВАТЬ ✨", type="primary", use_container_width=True):
        with st.spinner("Магия в процессе..."):
            try:
                # Картинка
                img_res = client.images.generate(model="dall-e-3", prompt=f"Cozy Pixar style illustration, child {name}.")
                st.image(img_res.data[0].url, use_container_width=True)

                # Музыка
                def get_audio_html(file_path):
                    with open(file_path, "rb") as f:
                        return f'<audio id="bg_music" loop><source src="data:audio/mp3;base64,{base64.b64encode(f.read()).decode()}" type="audio/mp3"></audio>'
                
                st.markdown(get_audio_html("bg_music.mp3"), unsafe_allow_html=True)

                # Текст
                ch_res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": f"Напиши сказку для {name} про {details}."}])
                story_text = ch_res.choices[0].message.content
                
                # Озвучка
                aud_res = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICES[selected_voice]}", 
                                        json={"text": story_text, "model_id": "eleven_multilingual_v2"}, 
                                        headers={"xi-api-key": ELEVEN_KEY})
                
                if aud_res.status_code == 200:
                    st.audio(aud_res.content, format="audio/mp3")

                # Автозапуск
                components.html(f"""
                    <script>
                    setTimeout(() => {{
                        const m = window.parent.document.getElementById('bg_music');
                        const a = window.parent.document.querySelectorAll('audio');
                        if (m) {{ m.volume = {music_vol}; m.play(); }}
                        if (a[0]) a[0].play();
                    }}, 1000);
                    </script>
                """, height=0)

                st.markdown(f'<div style="background:white; color:black; padding:30px; border-radius:20px;">{story_text}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Ошибка: {e}")
