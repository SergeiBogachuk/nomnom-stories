import streamlit as st
import base64
import streamlit.components.v1 as components

# Импортируем наши функции
from styles import apply_styles
from database import check_user, get_user_stories, save_story, update_audio, delete_story
from ai_engine import generate_story_text, generate_image, get_speech_b64

# --- 1. НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(
    page_title="NomNom Stories", 
    page_icon="🌙", 
    layout="wide", 
    initial_sidebar_state="expanded"
)
apply_styles()

def get_bg_music_html():
    try:
        with open("bg_music.mp3", "rb") as f:
            data = base64.b64encode(f.read()).decode()
            return f'<audio autoplay loop id="bg_music"><source src="data:audio/mp3;base64,{data}" type="audio/mp3"></audio><script>document.getElementById("bg_music").volume = 0.1;</script>'
    except: return ""

# --- 2. ЛОГИКА ВХОДА ---
if not st.session_state.get("logged_in", False):
    st.write("") # Отступы для центрирования
    st.write("")
    st.markdown("<h1 style='text-align: center;'>🌟 Вход в NomNom</h1>", unsafe_allow_html=True)
    with st.form("login_form"):
        e = st.text_input("Email")
        p = st.text_input("Пароль", type="password")
        submit = st.form_submit_button("Войти", type="primary", use_container_width=True)
        if submit:
            if check_user(e, p):
                st.session_state.logged_in, st.session_state.user_email = True, e
                st.rerun()
            else: st.error("Ошибка входа")
else:
    # --- 3. ОСНОВНОЙ ИНТЕРФЕЙС ---
    if 'time_val' not in st.session_state: st.session_state.time_val = 5
    if 'view_story' not in st.session_state: st.session_state.view_story = None

    with st.sidebar:
        st.success(f"Аккаунт: {st.session_state.user_email}")
        
        st.write("📚 **Мои сказки**")
        stories = get_user_stories(st.session_state.user_email)
        
        # Список сказок с КОРЗИНКОЙ
        for s in stories.data:
            # Делаем колонки: 5 частей под текст, 1 часть под корзину
            c_left, c_right = st.columns([5, 1])
            with c_left:
                if st.button(s.get('title') or "Сказка", key=f"btn_{s['id']}", use_container_width=True):
                    st.session_state.view_story = s
                    st.rerun()
            with c_right:
                # Специальный отступ сверху, чтобы корзина была вровень с текстом
                st.write(" ") 
                if st.button("🗑️", key=f"del_{s['id']}"):
                    delete_story(s['id'])
                    st.rerun()
        
        st.divider()
        if st.button("➕ Новая сказка", use_container_width=True, type="primary"):
            st.session_state.view_story = None
            st.rerun()
            
        if st.button("🚪 Выйти из аккаунта", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    # --- 4. КОНТЕНТ (ЦЕНТР) ---
    if st.session_state.view_story:
        # Экран чтения сказки
        s = st.session_state.view_story
        st.title(f"📖 {s.get('title')}")
        components.html(get_bg_music_html(), height=0)
        
        # Проверка и воспроизведение аудио
        if s.get('audio_base64'):
            st.audio(base64.b64decode(s['audio_base64']))
            st.info("✨ Играет из памяти (бесплатно)")
        else:
            if st.button("🔊 Озвучить сказку (ElevenLabs)", type="primary"):
                with st.spinner("🎙️ Готовим голос..."):
                    voice_id = "ymDCYd8puC7gYjxIamPt" # Марина по умолчанию
                    audio_b64 = get_speech_b64(s['story_text'], voice_id)
                    if audio_b64:
                        update_audio(s['id'], audio_b64)
                        st.audio(base64.b64decode(audio_b64))
                        st.rerun()
        
        if s.get('image_url'): st.image(s['image_url'], use_container_width=True)
        st.markdown(f'<div class="story-output">{s["story_text"]}</div>', unsafe_allow_html=True)
            
    else:
        # Экран создания новой сказки
        _, center, _ = st.columns([1, 2, 1])
        with center:
            st.title("✨ Создать сказку")
            cn = st.text_input("Имя ребенка", value="Даша")
            skills = st.multiselect("🎯 Тема воспитания:", ["Честность", "Доброта", "Смелость", "Дружба"], default=["Честность"])
            
            c1, c2 = st.columns(2)
            with c1: use_img = st.checkbox("🎨 С картинкой", value=True)
            with c2: use_audio = st.checkbox("🎧 Только Аудио", value=False)

            st.write("⏳ Длительность:")
            t_cols = st.columns(3)
            for i, t in enumerate([3, 5, 10]):
                if t_cols[i].button(f"{t} min", key=f"t_{t}", type="primary" if st.session_state.time_val == t else "secondary", use_container_width=True):
                    st.session_state.time_val = t
                    st.rerun()

            details = st.text_area("✍️ О чем будет история?")

            if st.button("🚀 СОЗДАТЬ МАГИЮ ✨", type="primary", use_container_width=True):
                with st.spinner("🧙‍♂️ Колдуем..."):
                    try:
                        txt = generate_story_text(cn, "Русский", skills, details, st.session_state.time_val)
                        ttl = txt.split('\n')[0].strip()
                        url = generate_image(ttl) if use_img else None
                        
                        save_story({
                            "user_email": st.session_state.user_email, 
                            "child_name": cn, 
                            "title": ttl, 
                            "story_text": txt, 
                            "image_url": url
                        })
                        st.rerun()
                    except Exception as e: st.error(f"Ошибка: {e}")
