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
        "title": "✨ NomNom Stories (GPT-5.3 PRO)",
        "child_name": "Имя ребенка",
        "skills_label": "🎯 Чему научим сегодня?",
        "duration": "⏳ Длительность:",
        "details": "✍️ О чем будет сказка?",
        "btn_create": "🚀 СОЗДАТЬ МАГИЮ ✨",
        "sidebar_acc": "Аккаунт",
        "sidebar_library": "📚 Мои сказки",
        "sidebar_voice": "🔊 Голос озвучки",
        "sidebar_new": "➕ Новая сказка",
        "btn_voice_act": "🔊 Прочитать вслух",
        "opt_img": "🎨 Генерировать картинку",
        "opt_audio": "🎧 Авто-озвучка сразу",
        "voices": {"Марина": "ymDCYd8puC7gYjxIamPt", "Николай": "8JVbfL6oEdmuxKn5DK2C", "Алиса": "EXAVITQu4vr4xnSDxMaL"},
        "skills": ["Честность", "Смелость", "Доброта", "Трудолюбие", "Вежливость", "Гигиена", "Дружба", "Усидчивость"]
    },
    "English": {
        "title": "✨ NomNom Stories (GPT-5.3 PRO)",
        "child_name": "Child's Name",
        "skills_label": "🎯 What should we teach?",
        "duration": "⏳ Duration:",
        "details": "✍️ What is the story about?",
        "btn_create": "🚀 CREATE MAGIC ✨",
        "sidebar_acc": "Account",
        "sidebar_library": "📚 My Stories",
        "sidebar_voice": "🔊 Voice Selection",
        "sidebar_new": "➕ New Story",
        "btn_voice_act": "🔊 Read Aloud",
        "opt_img": "🎨 Generate Image",
        "opt_audio": "🎧 Auto-generate Audio",
        "voices": {"Mary": "ymDCYd8puC7gYjxIamPt", "John": "8JVbfL6oEdmuxKn5DK2C", "Alice": "EXAVITQu4vr4xnSDxMaL"},
        "skills": ["Honesty", "Bravery", "Kindness", "Hard work", "Politeness", "Hygiene", "Friendship", "Patience"]
    }
}

st.markdown("""
    <style>
    .stApp { background: #0a0f1e; color: #f8fafc; }
    [data-testid="stSidebar"] { background-color: #111827 !important; border-right: 2px solid #38bdf8; }
    div[data-testid="stHorizontalBlock"] div.stButton > button { height: 60px !important; width: 100% !important; border-radius: 12px !important; border: 2px solid #38bdf8 !important; background-color: #1e293b !important; }
    div[data-testid="stHorizontalBlock"] div.stButton > button[kind="primary"] { background: linear-gradient(135deg, #38bdf8 0%, #1e40af 100%) !important; border: none !important; }
    div.stButton > button p { color: #FFFFFF !important; font-weight: 800 !important; font-size: 16px !important; }
    .stCheckbox label p { color: #FFFFFF !important; font-weight: 800 !important; font-size: 16px !important; }
    .stCheckbox { background: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #38bdf8; margin-bottom: 10px; }
    .story-output { background: #ffffff; color: #1e293b !important; padding: 40px; border-radius: 30px; font-size: 1.25em; line-height: 1.8; white-space: pre-wrap; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FUNCTIONS ---
URL = "https://gdyhmeshafpdttzjpxjg.supabase.co"
KEY = "sb_publishable_aqJsR96WyEdflsb4LoQSzg_g2WEyWBd"
supabase = create_client(URL, KEY)

def get_bg_music_html():
    try:
        with open("bg_music.mp3", "rb") as f:
            data = base64.b64encode(f.read()).decode()
            return f'<audio autoplay loop id="bg_music"><source src="data:audio/mp3;base64,{data}" type="audio/mp3"></audio><script>document.getElementById("bg_music").volume = 0.1;</script>'
    except: return ""

def get_speech(text, voice_id, api_key):
    res = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}", 
                        json={"text": text, "model_id": "eleven_multilingual_v2"}, 
                        headers={"xi-api-key": api_key})
    return res.content if res.status_code == 200 else None

# --- 4. MAIN ---
if not st.session_state.get("logged_in", False):
    st.title("🌟 NomNom Stories")
    e, p = st.text_input("Email"), st.text_input("Pass", type="password")
    if st.button("Войти", type="primary", use_container_width=True):
        res = supabase.table("users").select("*").eq("email", e).eq("password", p).execute()
        if res.data:
            st.session_state.logged_in, st.session_state.user_email = True, e
            st.rerun()
else:
    AI_MODEL = "gpt-5.3-chat-latest"
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    ELEVEN_KEY = st.secrets["ELEVENLABS_API_KEY"]
    
    if 'time_val' not in st.session_state: st.session_state.time_val = 5
    if 'view_story' not in st.session_state: st.session_state.view_story = None
    if 'sel_lang' not in st.session_state: st.session_state.sel_lang = "Русский"

    T = lang_dict[st.session_state.sel_lang]

    with st.sidebar:
        st.success(f"User: {st.session_state.user_email}")
        with st.expander(T['sidebar_library']):
            stories = supabase.table("stories").select("*").eq("user_email", st.session_state.user_email).order("created_at", desc=True).execute()
            for s in stories.data:
                if st.button(s.get('title') or "Story", key=f"s_{s['id']}", use_container_width=True):
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
        if s.get('image_url'): st.image(s['image_url'], use_container_width=True)
        components.html(get_bg_music_html(), height=0)
        
        # Если аудио уже есть в сессии или нажали кнопку
        if st.button(T['btn_voice_act'], type="primary"):
            data = get_speech(s['story_text'], selected_voice_id, ELEVEN_KEY)
            if data: st.audio(data)
        
        st.markdown(f'<div class="story-output">{s["story_text"]}</div>', unsafe_allow_html=True)
    
    else:
        st.title(T['title'])
        cn = st.text_input(T['child_name'], value="Даша")
        st.session_state.sel_lang = st.selectbox("Язык", ["Русский", "English"], index=0 if st.session_state.sel_lang == "Русский" else 1)
        skills = st.multiselect(T['skills_label'], T['skills'], default=[T['skills'][0]])
        
        c1, c2 = st.columns(2)
        with c1: gen_img = st.checkbox(T['opt_img'], value=True)
        with c2: auto_audio = st.checkbox(T['opt_audio'], value=True) # По умолчанию ВКЛ
        
        st.write(T['duration'])
        t_cols = st.columns(3)
        for i, t in enumerate([3, 5, 10]):
            btn_type = "primary" if st.session_state.time_val == t else "secondary"
            if t_cols[i].button(f"{t} min", key=f"t_{t}", type=btn_type, use_container_width=True):
                st.session_state.time_val = t
                st.rerun()

        details = st.text_area(T['details'])

        if st.button(T['btn_create'], type="primary", use_container_width=True):
            try:
                num_chapters = 1 if st.session_state.time_val <= 3 else (2 if st.session_state.time_val <= 5 else 3)
                full_text = ""
                text_placeholder = st.empty()

                for i in range(num_chapters):
                    chapter_p = f"Write chapter {i+1}/{num_chapters} for a fairy tale for {cn}. Lang: {st.session_state.sel_lang}. Skills: {', '.join(skills)}. Plot: {details}. Continue from: {full_text[-500:]}"
                    if i == 0: chapter_p += " Start with TITLE on 1st line."
                    
                    stream = client.chat.completions.create(model=AI_MODEL, messages=[{"role": "user", "content": chapter_p}], stream=True)
                    for chunk in stream:
                        if chunk.choices[0].delta.content:
                            full_text += chunk.choices[0].delta.content
                            # ЧИСТКА ОТ МУСОРА ПРИ ВЫВОДЕ
                            clean_display = full_text.replace(":::writing", "").replace("###", "").strip()
                            text_placeholder.markdown(f'<div class="story-output">{clean_display}</div>', unsafe_allow_html=True)
                
                # Финальная чистка
                full_text = full_text.replace(":::writing", "").replace("###", "").strip()
                gen_title = full_text.split('\n')[0].strip()
                
                img_url = None
                if gen_img:
                    with st.spinner("🎨"):
                        img_url = client.images.generate(model="dall-e-3", prompt=f"Pixar style: {gen_title}").data[0].url
                
                # АВТО-ОЗВУЧКА
                if auto_audio:
                    with st.spinner("🔊"):
                        audio_data = get_speech(full_text, selected_voice_id, ELEVEN_KEY)
                        if audio_data: st.audio(audio_data)

                supabase.table("stories").insert({
                    "user_email": st.session_state.user_email, "child_name": cn, 
                    "title": gen_title, "story_text": full_text, "image_url": img_url
                }).execute()
                
                st.session_state.view_story = {"title": gen_title, "story_text": full_text, "image_url": img_url}
                st.rerun()
            except Exception as e: st.error(f"Error: {e}")
