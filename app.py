import streamlit as st
from openai import OpenAI
import requests
import streamlit.components.v1 as components
import base64
from supabase import create_client, Client

# --- 1. КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="wide")

# Ссылка на твой логотип в GitHub
LOGO_URL = "https://raw.githubusercontent.com/SergeiBogachuk/nomnom-stories/main/logo.jpg"

# --- 2. СТИЛИ (ТВОЙ ДИЗАЙН + ИКОНКА) ---
st.markdown(f"""
    <head>
        <link rel="apple-touch-icon" href="{LOGO_URL}">
        <link rel="icon" sizes="192x192" href="{LOGO_URL}">
    </head>
    <style>
    .stApp {{ background: #0a0f1e; color: #f8fafc; }}
    [data-testid="stSidebar"] {{ background-color: #111827 !important; border-right: 2px solid #38bdf8; }}
    
    /* Кнопки выбора */
    div.stButton > button {{
        height: 55px !important;
        border-radius: 12px !important;
        border: 2px solid #38bdf8 !important;
        background-color: #1e293b !important;
    }}

    /* ТЕКСТ НА КНОПКАХ - ВСЕГДА БЕЛЫЙ И ЖИРНЫЙ */
    div.stButton > button p {{
        color: #FFFFFF !important; 
        font-weight: 800 !important;
        font-size: 15px !important;
    }}

    div.stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, #38bdf8 0%, #1e40af 100%) !important;
    }}

    .story-output {{ background: #ffffff; color: #1e293b !important; padding: 40px; border-radius: 30px; font-size: 1.25em; line-height: 1.8; }}
    
    /* Скрыть лишние элементы Streamlit */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# --- 3. ПОДКЛЮЧЕНИЕ К БАЗЕ ---
URL = "https://gdyhmeshafpdttzjpxjg.supabase.co"
KEY = "sb_publishable_aqJsR96WyEdflsb4LoQSzg_g2WEyWBd"

try:
    supabase: Client = create_client(URL, KEY)
except:
    st.error("Ошибка базы данных")
    st.stop()

# --- 4. ПОМОЩНИКИ ---
def get_audio_js(vol):
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

# --- 5. ВХОД / РЕГИСТРАЦИЯ ---
if not st.session_state.get("logged_in", False):
    st.title("🌟 NomNom Stories")
    t1, t2 = st.tabs(["Вход", "Регистрация"])
    with t1:
        e = st.text_input("Email", key="login_email")
        p = st.text_input("Пароль", type="password", key="login_pass")
        if st.button("Войти", type="primary", use_container_width=True):
            res = supabase.table("users").select("*").eq("email", e).eq("password", p).execute()
            if res.data:
                st.session_state.logged_in, st.session_state.user_email = True, e
                st.rerun()
    with t2:
        ne = st.text_input("Новый Email", key="reg_email")
        np = st.text_input("Новый Пароль", type="password", key="reg_pass")
        if st.button("Создать аккаунт", use_container_width=True):
            supabase.table("users").insert({"email": ne, "password": np}).execute()
            st.session_state.logged_in, st.session_state.user_email = True, ne
            st.rerun()
else:
    # --- ОСНОВНОЙ ИНТЕРФЕЙС ---
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    ELEVEN_KEY = st.secrets["ELEVENLABS_API_KEY"]
    
    if 'time_val' not in st.session_state: st.session_state.time_val = 5
    if 'theme_idx' not in st.session_state: st.session_state.theme_idx = 0
    if 'view_story' not in st.session_state: st.session_state.view_story = None
    if 'play_music' not in st.session_state: st.session_state.play_music = False

    with st.sidebar:
        st.success(f"Аккаунт: {st.session_state.user_email}")
        
        with st.expander("📚 Моя библиотека"):
            stories = supabase.table("stories").select("*").eq("user_email", st.session_state.user_email).order("created_at", desc=True).execute()
            if stories.data:
                for s in stories.data:
                    col_btn, col_del = st.columns([0.8, 0.2])
                    title = s.get('title') or f"Сказка для {s['child_name']}"
                    if col_btn.button(title, key=f"s_{s['id']}", use_container_width=True):
                        st.session_state.view_story = s
                        st.session_state.play_music = True
                        st.rerun()
                    if col_del.button("🗑️", key=f"del_{s['id']}"):
                        supabase.table("stories").delete().eq("id", s['id']).execute()
                        st.rerun()

        st.divider()
        VOICES = {"Марина": "ymDCYd8puC7gYjxIamPt", "Николай": "8JVbfL6oEdmuxKn5DK2C"}
        voice = st.selectbox("Голос", list(VOICES.keys()))
        vol = st.slider("Громкость", 0.0, 1.0, 0.2)
        
        if st.button("➕ Новая сказка"):
            st.session_state.view_story, st.session_state.play_music = None, False
            st.rerun()
        if st.button("Выйти"):
            st.session_state.clear()
            st.rerun()

    if st.session_state.play_music:
        components.html(get_audio_js(vol), height=0)

    if st.session_state.view_story:
        s = st.session_state.view_story
        title_text = s.get('title') or f"Сказка для {s['child_name']}"
        st.title(f"📖 {title_text}")
        st.image(s['image_url'], use_container_width=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔊 Озвучить"):
                res = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICES[voice]}", json={"text": s['story_text'], "model_id": "eleven_multilingual_v2"}, headers={"xi-api-key": ELEVEN_KEY})
                if res.status_code == 200: st.audio(res.content)
        with c2:
            st.download_button("📩 Скачать текст", s['story_text'], file_name=f"{title_text}.txt")

        st.markdown(f'<div class="story-output">{s["story_text"]}</div>', unsafe_allow_html=True)
    
    else:
        st.title("✨ Мастерская Сказок")
        cn = st.text_input("Имя ребенка", value="Даша")
        
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
            with st.spinner("Создаем шедевр..."):
                try:
                    theme = themes[st.session_state.theme_idx]
                    prompt = f"Напиши сказку для {cn} на тему {theme}. Сюжет: {details}. Напиши красивое НАЗВАНИЕ в самой ПЕРВОЙ строке, а затем текст сказки."
                    ch = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
                    
                    full_resp = ch.choices[0].message.content.split('\n')
                    gen_title = full_resp[0].strip().replace('#', '').replace('*', '')
                    gen_text = '\n'.join(full_resp[1:]).strip()
                    
                    # Картинка
                    img = client.images.generate(model="dall-e-3", prompt=f"Pixar illustration: {gen_title}").data[0].url
                    
                    # Сохранение
                    supabase.table("stories").insert({
                        "user_email": st.session_state.user_email, 
                        "child_name": cn, 
                        "theme": theme, 
                        "story_text": gen_text, 
                        "image_url": img, 
                        "title": gen_title
                    }).execute()
                    
                    st.session_state.view_story = {"title": gen_title, "story_text": gen_text, "image_url": img, "child_name": cn}
                    st.session_state.play_music = True
                    st.rerun()
                except Exception as e: st.error(f"Ошибка: {e}")
