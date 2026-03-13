import streamlit as st
from openai import OpenAI
import requests
import streamlit.components.v1 as components
import base64
from supabase import create_client, Client

# --- 1. CONFIG ---
st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="wide")

LOGO = "https://raw.githubusercontent.com/SergeiBogachuk/nomnom-stories/main/logo.jpg"

# --- 2. TRANSLATIONS ---
lang_dict = {
    "Русский": {
        "title": "✨ Мастерская Сказок",
        "child_name": "Имя ребенка",
        "skills_label": "🎯 Чему научим ребенка сегодня?",
        "duration": "⏳ Длительность:",
        "details": "✍️ О чем будет сказка?",
        "btn_create": "🚀 СОЗДАТЬ МАГИЮ ✨",
        "sidebar_acc": "Аккаунт",
        "sidebar_library": "📚 Мои сказки",
        "sidebar_voice": "🔊 Голос озвучки",
        "sidebar_new": "➕ Новая сказка",
        "sidebar_exit": "Выйти",
        "btn_voice_act": "🔊 Прочитать вслух",
        "voices": {"Марина (Женский)": "ymDCYd8puC7gYjxIamPt", "Николай (Мужской)": "8JVbfL6oEdmuxKn5DK2C", "Алиса (Детский)": "EXAVITQu4vr4xnSDxMaL"},
        "skills": ["Честность", "Смелость", "Доброта", "Трудолюбие", "Вежливость", "Гигиена", "Дружба", "Усидчивость"]
    },
    "English": {
        "title": "✨ Story Workshop",
        "child_name": "Child's Name",
        "skills_label": "🎯 What should we teach today?",
        "duration": "⏳ Duration:",
        "details": "✍️ What is the story about?",
        "btn_create": "🚀 CREATE MAGIC ✨",
        "sidebar_acc": "Account",
        "sidebar_library": "📚 My Stories",
        "sidebar_voice": "🔊 Voice Selection",
        "sidebar_new": "➕ New Story",
        "sidebar_exit": "Exit",
        "btn_voice_act": "🔊 Read Aloud",
        "voices": {"Mary (Female)": "ymDCYd8puC7gYjxIamPt", "John (Male)": "8JVbfL6oEdmuxKn5DK2C", "Alice (Child)": "EXAVITQu4vr4xnSDxMaL"},
        "skills": ["Honesty", "Bravery", "Kindness", "Hard work", "Politeness", "Hygiene", "Friendship", "Patience"]
    }
}

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
    span[data-baseweb="tag"] {{ background-color: #38bdf8 !important; color: white !important; }}
    </style>
    <link rel="apple-touch-icon" href="{LOGO}">
    """, unsafe_allow_html=True)

# --- 3. DATABASE ---
URL = "https://gdyhmeshafpdttzjpxjg.supabase.co"
KEY = "sb_publishable_aqJsR96WyEdflsb4LoQSzg_g2WEyWBd"
supabase: Client = create_client(URL, KEY)

# --- 4. AUTH ---
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
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    ELEVEN_KEY = st.secrets["ELEVENLABS_API_KEY"]
    
    if 'time_val' not in st.session_state: st.session_state.time_val = 5
    if 'view_story' not in st.session_state: st.session_state.view_story = None
    if 'sel_lang' not in st.session_state: st.session_state.sel_lang = "Русский"

    T = lang_dict[st.session_state.sel_lang]

    with st.sidebar:
        st.success(f"{T['sidebar_acc']}: {st.session_state.user_email}")
        with st.expander(T['sidebar_library']):
            stories = supabase.table("stories").select("*").eq("user_email", st.session_state.user_email).order("created_at", desc=True).execute()
            for s in stories.data:
                c_b, c_d = st.columns([0.8, 0.2])
                title = s.get('title') or (f"Story for {s['child_name']}" if st.session_state.sel_lang == "English" else f"Сказка для {s['child_name']}")
                if c_b.button(title, key=f"s_{s['id']}", use_container_width=True):
                    st.session_state.view_story = s
                    st.rerun()
                if c_d.button("🗑️", key=f"d_{s['id']}"):
                    supabase.table("stories").delete().eq("id", s['id']).execute()
                    st.rerun()

        st.divider()
        # ТУТ ТЕПЕРЬ ПЕРЕВЕДЕННЫЕ ИМЕНА ГОЛОСОВ
        selected_voice_name = st.selectbox(T['sidebar_voice'], list(T['voices'].keys()))
        selected_voice_id = T['voices'][selected_voice_name]
        
        if st.button(T['sidebar_new']):
            st.session_state.view_story = None
            st.rerun()
        if st.button(T['sidebar_exit']):
            st.session_state.clear()
            st.rerun()

    if st.session_state.view_story:
        s = st.session_state.view_story
        st.title(f"📖 {s.get('title', 'Story')}")
        st.image(s['image_url'], use_container_width=True)
        if st.button(T['btn_voice_act']):
            with st.spinner("..."):
                res = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{selected_voice_id}", 
                                    json={"text": s['story_text'], "model_id": "eleven_multilingual_v2"}, 
                                    headers={"xi-api-key": ELEVEN_KEY})
                if res.status_code == 200: st.audio(res.content)
        st.markdown(f'<div class="story-output">{s["story_text"]}</div>', unsafe_allow_html=True)
    
    else:
        st.title(T['title'])
        col_name, col_lang = st.columns(2)
        with col_name: cn = st.text_input(T['child_name'], value="Даша")
        with col_lang: 
            new_lang = st.selectbox("Language / Язык", ["Русский", "English"], index=0 if st.session_state.sel_lang == "Русский" else 1)
            if new_lang != st.session_state.sel_lang:
                st.session_state.sel_lang = new_lang
                st.rerun()
        
        st.write(T['skills_label'])
        skills = st.multiselect("", T['skills'], default=[T['skills'][2]]) # По умолчанию "Доброта"
        
        st.write(T['duration'])
        t_cols = st.columns(3)
        for i, t in enumerate([3, 5, 10]):
            unit = "min" if st.session_state.sel_lang == "English" else "мин"
            if t_cols[i].button(f"{t} {unit}", key=f"t_{t}", type="primary" if st.session_state.time_val == t else "secondary", use_container_width=True):
                st.session_state.time_val = t
                st.rerun()

        details = st.text_area(T['details'])

        if st.button(T['btn_create'], type="primary", use_container_width=True):
            try:
                prompt = f"Write a fairy tale for {cn} in {st.session_state.sel_lang}. Focus on skills: {', '.join(skills)}. Plot: {details}. Reading time: {st.session_state.time_val} minutes. Put the TITLE on the VERY FIRST line, then the story."
                full_text = ""
                text_placeholder = st.empty()
                stream = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}], stream=True)
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_text += chunk.choices[0].delta.content
                        text_placeholder.markdown(f'<div class="story-output">{full_text}</div>', unsafe_allow_html=True)
                lines = full_text.split('\n')
                gen_title = lines[0].replace('#', '').strip()
                img_url = client.images.generate(model="dall-e-3", prompt=f"Pixar animation style illustration for: {gen_title}").data[0].url
                supabase.table("stories").insert({"user_email": st.session_state.user_email, "child_name": cn, "title": gen_title, "story_text": full_text, "image_url": img_url}).execute()
                st.rerun()
            except Exception as e: st.error(f"Error: {e}")
