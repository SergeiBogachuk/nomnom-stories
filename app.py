import streamlit as st
from openai import OpenAI
import requests
import streamlit.components.v1 as components
import base64

st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="wide")

# --- СОБСТВЕННАЯ СИСТЕМА ВХОДА ---
def check_password():
    def password_entered():
        if st.session_state["username"] in st.secrets["passwords"] and \
           st.session_state["password"] == st.secrets["passwords"][st.session_state["username"]]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # удаляем пароль из памяти для безопасности
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.title("🔑 Вход в NomNom Stories")
        st.text_input("Логин", on_change=password_entered, key="username")
        st.text_input("Пароль", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.title("🔑 Вход в NomNom Stories")
        st.text_input("Логин", on_change=password_entered, key="username")
        st.text_input("Пароль", type="password", on_change=password_entered, key="password")
        st.error("😕 Неверный логин или пароль")
        return False
    else:
        return True

# --- ПРОВЕРКА ВХОДА ---
if check_password():
    # ЕСЛИ ПАРОЛЬ ВЕРЕН - ПОКАЗЫВАЕМ ПРИЛОЖЕНИЕ
    
    with st.sidebar:
        st.success(f"Привет, {st.session_state['username']}!")
        if st.button("Выйти"):
            del st.session_state["password_correct"]
            st.rerun()

    # --- ТВОЙ ОСНОВНОЙ КОД ---
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    ELEVEN_KEY = st.secrets["ELEVENLABS_API_KEY"]

    def get_audio_html(file_path):
        try:
            with open(file_path, "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                return f'<audio id="bg_music" loop><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
        except: return ""

    st.markdown("""
        <style>
        .stApp { background: #0a0f1e; color: #f8fafc; }
        [data-testid="stSidebar"] { background-color: #111827 !important; border-right: 2px solid #38bdf8; }
        .story-output { background: #ffffff; color: #1e293b; padding: 40px; border-radius: 30px; font-size: 1.2em; line-height: 1.7; color: black !important; }
        </style>
        """, unsafe_allow_html=True)

    VOICES = {"Марина (Женский)": "ymDCYd8puC7gYjxIamPt", "Николай (Мужской)": "8JVbfL6oEdmuxKn5DK2C"}

    def generate_premium_audio(text, voice_id):
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {"xi-api-key": ELEVEN_KEY, "Content-Type": "application/json"}
        data = {"text": text, "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.6, "similarity_boost": 0.8}}
        res = requests.post(url, json=data, headers=headers)
        return res.content if res.status_code == 200 else None

    st.title("🌟 NomNom Stories")
    
    col1, col2 = st.columns(2)
    with col1: child_name = st.text_input("Имя ребенка", value="Даша")
    with col2: lang = st.selectbox("Язык", ["Русский", "English"])

    story_minutes = st.select_slider("⏳ Длительность", options=[3, 5, 10, 15, 20, 30], value=10)
    details = st.text_area("✍️ О чем сегодня сказка?")

    if st.button("✨ СОЗДАТЬ СКАЗКУ ✨", type="primary", use_container_width=True):
        num_chapters = max(1, story_minutes // 3)
        with st.spinner("Создаем магию..."):
            try:
                img_res = client.images.generate(model="dall-e-3", prompt=f"Cozy Pixar illustration, child {child_name}.")
                st.image(img_res.data[0].url, use_container_width=True)

                music_html = get_audio_html("bg_music.mp3")
                st.markdown(music_html, unsafe_allow_html=True)
                
                full_story = ""
                for i in range(num_chapters):
                    st.write(f"📖 Глава {i+1}...")
                    ch_res = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": f"Напиши главу {i+1} сказки для {child_name}. Тема: {details}."}]
                    )
                    chapter_text = ch_res.choices[0].message.content
                    full_story += f"\n\n### Глава {i+1}\n" + chapter_text
                    
                    audio_bytes = generate_premium_audio(chapter_text, VOICES[selected_voice] if 'selected_voice' in locals() else VOICES["Марина (Женский)"])
                    if audio_bytes:
                        st.audio(audio_bytes, format="audio/mp3")

                components.html(f"""
                    <script>
                    setTimeout(() => {{
                        const music = window.parent.document.getElementById('bg_music');
                        const audios = window.parent.document.querySelectorAll('audio');
                        if (music) {{ music.volume = 0.2; music.play(); }}
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
