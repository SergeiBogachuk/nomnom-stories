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

# --- 2. ЖЕСТКИЙ СТИЛЬ (ДЛЯ БЕЛЫХ КНОПОК И ДИЗАЙНА) ---
st.markdown("""
    <style>
    .stApp { background: #0a0f1e; color: #f8fafc; }
    [data-testid="stSidebar"] { background-color: #111827 !important; border-right: 2px solid #38bdf8; }
    
    /* Кнопки выбора (Время и Темы) */
    div.stButton > button {
        height: 60px !important;
        border-radius: 12px !important;
        border: 2px solid #38bdf8 !important;
        background-color: #1e293b !important;
    }

    /* ПРИНУДИТЕЛЬНО БЕЛЫЙ ТЕКСТ НА ВСЕХ КНОПКАХ */
    div.stButton > button p {
        color: #FFFFFF !important; 
        font-weight: 800 !important;
        font-size: 16px !important;
    }

    /* Активная кнопка */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #38bdf8 0%, #1e40af 100%) !important;
    }

    .story-output { background: #ffffff; color: #1e293b !important; padding: 40px; border-radius: 30px; font-size: 1.25em; line-height: 1.8; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ФУНКЦИИ ЗВУКА ---
def play_music_js(vol):
    try:
        with open("bg_music.mp3", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            return f"""
            <audio id="bg_music" loop autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            <script>
                var audio = window.parent.document.getElementById('bg_music');
                if(audio) {{ audio.volume = {vol}; audio.play(); }}
            </script>
            """
    except: return ""

# --- 4. ЛОГИКА ВХОДА ---
if not st.session_state.get("logged_in", False):
    st.title("🌟 NomNom Stories")
    tab1, tab2 = st.tabs(["Вход", "Регистрация"])
    with tab1:
        e = st.text_input("Email", key="l_email")
        p = st.text_input("Пароль", type="password", key="l_pass")
        if st.button("Войти", type="primary", use_container_width=True):
            res = supabase.table("users").select("*").eq("email", e).eq("password", p).execute()
            if len(res.data) > 0:
                st.session_state.logged_in = True
                st.session_state.user_email = e
                st.rerun()
    with tab2:
        ne = st.text_input("Новый Email", key="r_email")
        np = st.text_input("Пароль", type="password", key="r_pass")
        if st.button("Создать аккаунт", use_container_width=True):
            supabase.table("users").insert({"email": ne, "password": np}).execute()
            st.session_state.logged_in = True
            st.session_state.user_email = ne
            st.rerun()
else:
    # --- ГЛАВНЫЙ ЭКРАН ---
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    ELEVEN_KEY = st.secrets["ELEVENLABS_API_KEY"]
    
    if 'theme_idx' not in st.session_state: st.session_state.theme_idx = 0
    if 'time_val' not in st.session_state: st.session_state.time_val = 5
    if 'view_story' not in st.session_state: st.session_state.view_story = None
    if 'play_audio' not in st.session_state: st.session_state.play_audio = False

    with st.sidebar:
        st.success(f"Аккаунт: {st.session_state['user_email']}")
        
        # --- СКРЫТЫЙ СПИСОК СКАЗОК (ЭКСКЛЮЗИВНО) ---
        with st.expander("📚 Моя библиотека"):
            res = supabase.table("stories").select("*").eq("user_email", st.session_state["user_email"]).order("created_at", desc=True).execute()
            if res.data:
                for s in res.data:
                    if st.button(f"{s['theme'].split()[0]} | {s['child_name']}", key=f"s_{s['id']}", use_container_width=True):
                        st.session_state.view_story = s
                        st.session_state.play_audio = True # Включаем музыку при просмотре
                        st.rerun()
            else:
                st.write("Пока пусто")

        st.divider()
        VOICES = {"Марина": "ymDCYd8puC7gYjxIamPt", "Николай": "8JVbfL6oEdmuxKn5DK2C"}
        selected_voice = st.selectbox("Голос", list(VOICES.keys()))
        music_vol = st.slider("Громкость музыки", 0.0, 1.0, 0.25)
        
        if st.button("➕ Новая сказка"):
            st.session_state.view_story = None
            st.session_state.play_audio = False
            st.rerun()
        if st.button("Выйти"):
            st.session_state.clear()
            st.rerun()

    # --- ВКЛЮЧАЕМ МУЗЫКУ ТОЛЬКО ЕСЛИ НУЖНО ---
    if st.session_state.play_audio:
        components.html(play_music_js(music_vol), height=0)

    if st.session_state.view_story:
        s = st.session_state.view_story
        st.title(f"📖 Сказка для {s['child_name']}")
        st.image(s['image_url'], use_container_width=True)
        
        if st.button("🔊 Прочитать вслух"):
            with st.spinner("Марина начинает рассказ..."):
                aud_res = requests.post(
                    f"https://api.elevenlabs.io/v1/text-to-speech/{VOICES[selected_voice]}",
                    json={"text": s['story_text'], "model_id": "eleven_multilingual_v2"},
                    headers={"xi-api-key": ELEVEN_KEY}
                )
                if aud_res.status_code == 200:
                    st.audio(aud_res.content, format="audio/mp3")

        st.markdown(f'<div class="story-output">{s["story_text"]}</div>', unsafe_allow_html=True)
    
    else:
        st.title("✨ Мастерская Сказок")
        col1, col2 = st.columns(2)
        with col1: child_name = st.text_input("Имя ребенка", value="Даша")
        with col2: lang = st.selectbox("Язык", ["Русский", "English"])
        
        st.write("⏳ Длительность:")
        t_cols = st.columns(3)
        for i, t in enumerate([3, 5, 10]):
            if t_cols[i].button(f"{t} мин", key=f"t_{t}", type="primary" if st.session_state.time_val == t else "secondary", use_container_width=True):
                st.session_state.time_val = t
                st.rerun()

        st.write("🛡️ Тема:")
        th_cols = st.columns(3)
        themes = ["🛡️ Храбрость", "🍎 Привычки", "🤝 Отношения"]
        for i in range(3):
            if th_cols[i].button(themes[i], key=f"th_{i}", type="primary" if st.session_state.theme_idx == i else "secondary", use_container_width=True):
                st.session_state.theme_idx = i
                st.rerun()

        details = st.text_area("✍️ Краткий сюжет")

        if st.button("🚀 СОЗДАТЬ МАГИЮ ✨", type="primary", use_container_width=True):
            with st.spinner("Волшебство начинается..."):
                try:
                    curr_theme = themes[st.session_state.theme_idx]
                    img_res = client.images.generate(model="dall-e-3", prompt=f"Pixar illustration, {curr_theme}, child {child_name}.")
                    img_url = img_res.data[0].url
                    
                    ch_res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": f"Напиши сказку для {child_name}, тема {curr_theme}, сюжет {details}. Язык {lang}."}])
                    story_text = ch_res.choices[0].message.content
                    
                    supabase.table("stories").insert({"user_email": st.session_state.user_email, "child_name": child_name, "theme": curr_theme, "story_text": story_text, "image_url": img_url}).execute()
                    
                    st.session_state.view_story = {"child_name": child_name, "image_url": img_url, "story_text": story_text}
                    st.session_state.play_audio = True # ВКЛЮЧАЕМ МУЗЫКУ ПОСЛЕ ГЕНЕРАЦИИ
                    st.rerun()
                except Exception as e:
                    st.error(f"Ошибка: {e}")
