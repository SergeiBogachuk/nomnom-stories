import streamlit as st
import base64
import streamlit.components.v1 as components

from styles import apply_styles
from database import check_user, get_user_stories, save_story, update_audio
from ai_engine import generate_story_text, generate_image, get_speech_b64

st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="wide", initial_sidebar_state="expanded")
apply_styles()

# --- ЛОГИКА ВЫХОДА ---
def logout():
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.session_state.view_story = None
    st.rerun()

if not st.session_state.get("logged_in", False):
    _, center, _ = st.columns([1, 2, 1])
    with center:
        st.title("🌟 Вход")
        with st.form("login_form"):
            e = st.text_input("Email")
            p = st.text_input("Пароль", type="password")
            if st.form_submit_button("Войти", type="primary", use_container_width=True):
                if check_user(e, p):
                    st.session_state.logged_in, st.session_state.user_email = True, e
                    st.rerun()
                else: st.error("Ошибка входа")
else:
    if 'time_val' not in st.session_state: st.session_state.time_val = 5
    if 'view_story' not in st.session_state: st.session_state.view_story = None
    
    with st.sidebar:
        st.success(f"Аккаунт: {st.session_state.user_email}")
        with st.expander("📚 Мои сказки"):
            stories = get_user_stories(st.session_state.user_email)
            for s in stories.data:
                if st.button(s.get('title') or "Сказка", key=f"s_{s['id']}", use_container_width=True):
                    st.session_state.view_story = s
                    st.rerun()
        
        if st.button("➕ Новая сказка", use_container_width=True):
            st.session_state.view_story = None
            st.rerun()
            
        st.divider()
        # КНОПКА ВЫХОДА В САЙДБАРЕ
        if st.button("🚪 Выйти из аккаунта", use_container_width=True):
            logout()

    if st.session_state.view_story:
        # Экран чтения
        s = st.session_state.view_story
        st.title(f"📖 {s.get('title')}")
        if s.get('audio_base64'):
            st.audio(base64.b64decode(s['audio_base64']))
        
        if s.get('image_url'): st.image(s['image_url'], use_container_width=True)
        st.markdown(f'<div class="story-output">{s["story_text"]}</div>', unsafe_allow_html=True)
            
    else:
        # ЭКРАН СОЗДАНИЯ
        _, center, _ = st.columns([1, 2, 1])
        with center:
            st.title("✨ Создать сказку")
            cn = st.text_input("Имя ребенка", value="Даша")
            skills = st.multiselect("🎯 Чему научим сегодня?", ["Честность", "Доброта", "Смелость"], default=["Честность"])
            
            c1, c2 = st.columns(2)
            with c1: use_img = st.checkbox("🎨 Текст + Картинка", value=True)
            with c2: use_audio = st.checkbox("🎧 Только Аудио", value=False)

            st.write("⏳ Длительность:")
            t_cols = st.columns(3)
            times = [3, 5, 10]
            for i, t in enumerate(times):
                # Кнопка теперь ВСЕГДА имеет текст, фон исправлен в CSS
                if t_cols[i].button(f"{t} min", key=f"t_{t}", type="primary" if st.session_state.time_val == t else "secondary", use_container_width=True):
                    st.session_state.time_val = t
                    st.rerun()

            details = st.text_area("✍️ О чем будет сказка?")

            if st.button("🚀 СОЗДАТЬ МАГИЮ ✨", type="primary", use_container_width=True):
                with st.spinner("🧙‍♂️ Колдуем..."):
                    try:
                        txt = generate_story_text(cn, "Русский", skills, details, st.session_state.time_val)
                        ttl = txt.split('\n')[0].strip()
                        url = generate_image(ttl) if use_img else None
                        save_story({"user_email": st.session_state.user_email, "child_name": cn, "title": ttl, "story_text": txt, "image_url": url})
                        st.rerun()
                    except Exception as e: st.error(f"Ошибка: {e}")
