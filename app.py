import streamlit as st
from openai import OpenAI
import requests
import streamlit.components.v1 as components
import base64
from supabase import create_client, Client

# --- 1. CONFIG ---
st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="wide")

# --- 2. TRANSLATIONS ---
lang_dict = {
    "Русский": {
        "title": "✨ Мастерская Сказок",
        "child_name": "Имя ребенка",
        "skills_label": "🎯 Чему научим сегодня?",
        "duration": "⏳ Длительность:",
        "details": "✍️ О чем будет сказка?",
        "btn_create": "🚀 СОЗДАТЬ МАГИЮ ✨",
        "sidebar_acc": "Аккаунт",
        "sidebar_library": "📚 Мои сказки",
        "sidebar_voice": "🔊 Голос озвучки",
        "sidebar_new": "➕ Новая сказка",
        "sidebar_exit": "Выйти",
        "btn_voice_act": "🔊 Прочитать вслух",
        "voices": {"Марина": "ymDCYd8puC7gYjxIamPt", "Николай": "8JVbfL6oEdmuxKn5DK2C", "Алиса": "EXAVITQu4vr4xnSDxMaL"},
        "skills": ["Честность", "Смелость", "Доброта", "Трудолюбие", "Вежливость", "Гигиена", "Дружба", "Усидчивость"]
    },
    "English": {
        "title": "✨ Story Workshop",
        "child_name": "Child's Name",
        "skills_label": "🎯 What should we teach?",
        "duration": "⏳ Duration:",
        "details": "✍️ What is the story about?",
        "btn_create": "🚀 CREATE MAGIC ✨",
        "sidebar_acc": "Account",
        "sidebar_library": "📚 My Stories",
        "sidebar_voice": "🔊 Voice Selection",
        "sidebar_new": "➕ New Story",
        "sidebar_exit": "Exit",
        "btn_voice_act": "🔊 Read Aloud",
        "voices": {"Mary": "ymDCYd8puC7gYjxIamPt", "John": "8JVbfL6oEdmuxKn5DK2C", "Alice": "EXAVITQu4vr4xnSDxMaL"},
        "skills": ["Honesty", "Bravery", "Kindness", "Hard work", "Politeness", "Hygiene", "Friendship", "Patience"]
    }
}

st.markdown("""
    <style>
    .stApp { background: #0a0f1e; color: #f8fafc; }
    [data-testid="stSidebar"] { background-color: #111827 !important; border-right: 2px solid #38bdf8; }
    div.stButton > button { height: 55px !important; border-radius: 12px !important; border: 2px solid #38bdf8 !important; background-color: #1e293b !important; }
    div.stButton > button p { color: #FFFFFF !important; font-weight: 800 !important; font-size: 15px !important; }
    div.stButton > button[kind="primary"] { background: linear-gradient(135deg, #38bdf8 0%, #1e40af 100%) !important; }
    .story-output { background: #ffffff; color: #1e293b !important; padding: 40px; border-radius: 30px; font-size: 1.25em; line-height: 1.8; white-space: pre-wrap; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE & FUNCTIONS ---
URL = "https://gdyhmeshafpdttzjpxjg.supabase.co"
KEY = "sb_publishable_aqJsR96WyEdflsb4LoQSzg_g2WEyWBd"
supabase = create_client(URL, KEY)

def get_bg_music_html():
    try:
        with open("bg_music.mp3", "rb") as f:
            data = base64.b64encode(f.read()).decode()
            return f"""
            <audio id="bg_audio" loop autoplay>
                <source src="data:audio/mp3;base64,{data}" type="audio/mp3">
            </audio>
            <script>
                var audio = document.getElementById('bg_audio');
                audio.volume = 0.2;
                audio.play();
            </script>
            """
    except: return ""

# --- 4. MAIN LOGIC ---
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
                if st.button(s.get('title') or s['child_name'], key=f"s_{s['id']}", use_container_width=True):
                    st.session_state.view_story = s
                    st.rerun()

        st.divider()
        selected_voice_name = st.selectbox(T['sidebar_voice'], list(T['voices'].keys()))
        selected_voice_id = T['voices'][selected_voice_name]
        
        if st.button(T['sidebar_new']):
            st.session_state.view_story = None
            st.rerun()

    if st.session_state.view_story:
        s = st.session_state.view_story
        st.title(f"📖 {s.get('title', 'Story')}")
        st.image(s['image_url'], use_container_width=True)
        
        # ВКЛЮЧАЕМ МУЗЫКУ
        components.html(get_bg_music_html(), height=0)
        
        if st.button(T['btn_voice_act']):
            with st.spinner("..."):
                res = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{selected_voice_id}", 
                                    json={"text": s['story_text'], "model_id": "eleven_multilingual_v2"}, 
                                    headers={"xi-api-key": ELEVEN_KEY})
                if res.status_code == 200: st.audio(res.content)
        
        st.markdown(f'<div class="story-output">{s["story_text"]}</div>', unsafe_allow_html=True)
    
    else:
        st.title(T['title'])
        cn = st.text_input(T['child_name'], value="Даша")
        st.session_state.sel_lang = st.selectbox("Language / Язык", ["Русский", "English"], index=0 if st.session_state.sel_lang == "Русский" else 1)
        
        skills = st.multiselect(T['skills_label'], T['skills'], default=[T['skills'][0]])
        
        t_cols = st.columns(3)
        for i, t in enumerate([3, 5, 10]):
            u = "min" if st.session_state.sel_lang == "English" else "мин"
            if t_cols[i].button(f"{t} {u}", key=f"t_{t}", type="primary" if st.session_state.time_val == t else "secondary", use_container_width=True):
                st.session_state.time_val = t
                st.rerun()

        details = st.text_area(T['details'])

        if st.button(T['btn_create'], type="primary", use_container_width=True):
            try:
                # УСИЛЕННЫЙ ПРОМПТ ДЛЯ ДЛИНЫ
                word_count = st.session_state.time_val * 130 # ~130 слов в минуту
                p = f"""Write a VERY LONG fairy tale for {cn} in {st.session_state.sel_lang}. 
                Target length: MINIMUM {word_count} words. 
                Focus on skills: {', '.join(skills)}. Plot: {details}.
                The story must be detailed, descriptive, and last {st.session_state.time_val} minutes when read aloud.
                Put the TITLE on the very first line."""
                
                with st.spinner("Пишем длинную сказку..."):
                    res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": p}])
                    full_text = res.choices[0].message.content
                
                lines = full_text.split('\n')
                gen_title = lines[0].replace('#', '').strip()
                gen_story = '\n'.join(lines[1:]).strip()
                
                with st.spinner("Рисуем..."):
                    img_url = client.images.generate(model="dall-e-3", prompt=f"Pixar style: {gen_title}").data[0].url
                
                supabase.table("stories").insert({
                    "user_email": st.session_state.user_email, "child_name": cn, 
                    "title": gen_title, "story_text": gen_story, "image_url": img_url
                }).execute()
                
                st.session_state.view_story = {"title": gen_title, "story_text": gen_story, "image_url": img_url, "child_name": cn}
                st.rerun()
            except Exception as e: st.error(f"Error: {e}")
