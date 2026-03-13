import streamlit as st
from openai import OpenAI
import requests
import streamlit.components.v1 as components
import base64
from supabase import create_client, Client

# --- 1. CONFIG ---
st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="wide")

# Логотип
LOGO = "https://raw.githubusercontent.com/SergeiBogachuk/nomnom-stories/main/logo.jpg"

st.markdown(f"""
    <style>
    .stApp {{ background: #0a0f1e; color: #f8fafc; }}
    [data-testid="stSidebar"] {{ background-color: #111827 !important; border-right: 2px solid #38bdf8; }}
    div.stButton > button {{
        height: 55px !important;
        border-radius: 12px !important;
        border: 2px solid #38bdf8 !important;
        background-color: #1e293b !important;
    }}
    div.stButton > button p {{ color: #FFFFFF !important; font-weight: 800 !important; font-size: 15px !important; }}
    div.stButton > button[kind="primary"] {{ background: linear-gradient(135deg, #38bdf8 0%, #1e40af 100%) !important; }}
    .story-output {{ background: #ffffff; color: #1e293b !important; padding: 40px; border-radius: 30px; font-size: 1.25em; line-height: 1.8; }}
    </style>
    <link rel="apple-touch-icon" href="{LOGO}">
    """, unsafe_allow_html=True)

# --- 2. БАЗА И API ---
URL = "https://gdyhmeshafpdttzjpxjg.supabase.co"
KEY = "sb_publishable_aqJsR96WyEdflsb4LoQSzg_g2WEyWBd"
supabase: Client = create_client(URL, KEY)

# --- 3. ЛОГИКА АВТОРИЗАЦИИ ---
if not st.session_state.get("logged_in", False):
    st.title("🌟 NomNom Stories")
    t1, t2 = st.tabs(["Вход", "Регистрация"])
    with t1:
        e = st.text_input("Email", key="l_e")
        p = st.text_input("Пароль", type="password", key="l_p")
        if st.button("Войти", type="primary", use_container_width=True):
            res = supabase.table("users").select("*").eq("email", e).eq("password", p).execute()
            if res.data:
                st.session_state.logged_in, st.session_state.user_email = True, e
                st.rerun()
    with t2:
        ne = st.text_input("Новый Email", key="r_e")
        np = st.text_input("Пароль", type="password", key="r_p")
        if st.button("Создать аккаунт", use_container_width=True):
            supabase.table("users").insert({"email": ne, "password": np}).execute()
            st.session_state.logged_in, st.session_state.user_email = True, ne
            st.rerun()
else:
    # --- ГЛАВНЫЙ ЭКРАН ---
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    ELEVEN_KEY = st.secrets["ELEVENLABS_API_KEY"]
    
    # Инициализация
    if 'time_val' not in st.session_state: st.session_state.time_val = 5
    if 'view_story' not in st.session_state: st.session_state.view_story = None

    with st.sidebar:
        st.success(f"Аккаунт: {st.session_state.user_email}")
        with st.expander("📚 Мои сказки"):
            stories = supabase.table("stories").select("*").eq("user_email", st.session_state.user_email).order("created_at", desc=True).execute()
            for s in stories.data:
                c_b, c_d = st.columns([0.8, 0.2])
                title = s.get('title') or f"Сказка для {s['child_name']}"
                if c_b.button(title, key=f"s_{s['id']}", use_container_width=True):
                    st.session_state.view_story = s
                    st.rerun()
                if c_d.button("🗑️", key=f"d_{s['id']}"):
                    supabase.table("stories").delete().eq("id", s['id']).execute()
                    st.rerun()

        st.divider()
        # ВЫБОР ГОЛОСА
        VOICES = {
            "Марина (Женский)": "ymDCYd8puC7gYjxIamPt", 
            "Николай (Мужской)": "8JVbfL6oEdmuxKn5DK2C",
            "Алиса (Детский)": "EXAVITQu4vr4xnSDxMaL"
        }
        selected_voice = st.selectbox("🔊 Выберите голос", list(VOICES.keys()))
        
        if st.button("➕ Новая сказка"):
            st.session_state.view_story = None
            st.rerun()
        if st.button("Выйти"):
            st.session_state.clear()
            st.rerun()

    if st.session_state.view_story:
        s = st.session_state.view_story
        st.title(f"📖 {s.get('title', 'Твоя сказка')}")
        st.image(s['image_url'], use_container_width=True)
        
        if st.button("🔊 Включить озвучку"):
            with st.spinner("Готовим аудио..."):
                res = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICES[selected_voice]}", 
                                    json={"text": s['story_text'], "model_id": "eleven_multilingual_v2"}, 
                                    headers={"xi-api-key": ELEVEN_KEY})
                if res.status_code == 200: st.audio(res.content)
        
        st.markdown(f'<div class="story-output">{s["story_text"]}</div>', unsafe_allow_html=True)
    
    else:
        st.title("✨ Мастерская Сказок")
        
        col_name, col_lang = st.columns(2)
        with col_name: cn = st.text_input("Имя ребенка", value="Даша")
        with col_lang: lang = st.selectbox("Язык", ["Русский", "English"])
        
        # НОВЫЕ ПАРАМЕТРЫ
        st.write("🎯 Чему научим ребенка?")
        skills = st.multiselect("Выберите навыки", 
                                ["Честность", "Смелость", "Доброта", "Трудолюбие", "Вежливость", "Гигиена", "Дружба"],
                                default=["Смелость"])
        
        st.write("⏳ Длительность:")
        t_cols = st.columns(3)
        for i, t in enumerate([3, 5, 10]):
            if t_cols[i].button(f"{t} мин", key=f"t_{t}", type="primary" if st.session_state.time_val == t else "secondary", use_container_width=True):
                st.session_state.time_val = t
                st.rerun()

        details = st.text_area("✍️ Краткий сюжет (о чем должна быть история?)")

        if st.button("🚀 СОЗДАТЬ МАГИЮ ✨", type="primary", use_container_width=True):
            try:
                # 1. Сначала генерируем заголовок и Текст (Потоком для скорости)
                prompt = f"Напиши сказку для {cn} на языке {lang}. Темы: {', '.join(skills)}. Сюжет: {details}. Длительность: {st.session_state.time_val} мин. ПЕРВАЯ СТРОКА - Название, затем текст."
                
                # Заготовка под текст
                full_text = ""
                text_placeholder = st.empty()
                
                # Потоковая генерация через OpenAI
                stream = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    stream=True
                )
                
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        full_text += chunk.choices[0].delta.content
                        text_placeholder.markdown(f'<div class="story-output">{full_text}</div>', unsafe_allow_html=True)

                # 2. Теперь, когда текст готов, генерируем картинку
                lines = full_text.split('\n')
                gen_title = lines[0].replace('#', '').strip()
                
                with st.spinner("Рисуем картинку..."):
                    img_url = client.images.generate(model="dall-e-3", prompt=f"Pixar illustration: {gen_title}").data[0].url
                
                # 3. Сохраняем в базу
                supabase.table("stories").insert({
                    "user_email": st.session_state.user_email,
                    "child_name": cn,
                    "title": gen_title,
                    "story_text": full_text,
                    "image_url": img_url
                }).execute()
                
                st.success("Готово! Сказка сохранена.")
                st.rerun()
                
            except Exception as e:
                st.error(f"Ошибка: {e}")
