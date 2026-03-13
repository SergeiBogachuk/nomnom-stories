import streamlit as st
import base64
from styles import apply_styles
from database import check_user, get_user_stories, save_story, update_audio, delete_story
from ai_engine import generate_story_text, generate_image, get_speech_b64

# --- НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(page_title="NomNom Stories", layout="wide", initial_sidebar_state="expanded")
apply_styles()

# --- ЛОГИКА ВХОДА ---
if not st.session_state.get("logged_in", False):
    st.markdown("<h1 style='text-align: center; color: white;'>🌟 Вход в NomNom</h1>", unsafe_allow_html=True)
    with st.form("login_form"):
        e = st.text_input("Email")
        p = st.text_input("Пароль", type="password")
        if st.form_submit_button("Войти", use_container_width=True):
            if check_user(e, p):
                st.session_state.logged_in, st.session_state.user_email = True, e
                st.rerun()
            else:
                st.error("Неверный логин или пароль")
else:
    # --- ОСНОВНОЙ ИНТЕРФЕЙС ---
    if 'time_val' not in st.session_state: st.session_state.time_val = 5
    if 'view_story' not in st.session_state: st.session_state.view_story = None

    with st.sidebar:
        st.markdown(f"👤 **{st.session_state.user_email}**")
        st.divider()
        
        with st.expander("📚 Мои сказки", expanded=True):
            stories = get_user_stories(st.session_state.user_email)
            for s in stories.data:
                c_btn, c_del = st.columns([5, 1])
                with c_btn:
                    if st.button(s.get('title') or "Сказка", key=f"s_{s['id']}", use_container_width=True):
                        st.session_state.view_story = s
                        st.rerun()
                with c_del:
                    if st.button("🗑️", key=f"d_{s['id']}"):
                        delete_story(s['id'])
                        st.rerun()
        
        st.divider()
        if st.button("➕ Новая сказка", type="primary", use_container_width=True):
            st.session_state.view_story = None
            st.rerun()
        if st.button("🚪 Выйти", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    # --- ЦЕНТРАЛЬНАЯ ЧАСТЬ ---
    if st.session_state.view_story:
        # Экран просмотра сказки
        s = st.session_state.view_story
        st.markdown(f"<h1 style='text-align: center; color: white;'>📖 {s.get('title')}</h1>", unsafe_allow_html=True)
        if s.get('audio_base64'):
            st.audio(base64.b64decode(s['audio_base64']))
        if s.get('image_url'):
            st.image(s['image_url'], use_container_width=True)
        st.markdown(f'<div style="background:white; color:#1e293b; padding:25px; border-radius:15px; font-size:1.1rem;">{s["story_text"]}</div>', unsafe_allow_html=True)
    
    else:
        # Экран создания сказки
        st.markdown("<h1 style='text-align: center; color: white;'>✨ Создать магию</h1>", unsafe_allow_html=True)
        
        # 1. Имя ребенка
        cn = st.text_input("Имя ребенка", value="Даша")
        
        # 2. ВЫБОР ЯЗЫКА (Новый блок!)
        selected_lang = st.selectbox("🌍 Язык сказки", ["Русский", "English", "Română", "Deutsch", "Français", "Español"], index=0)
        
        # 3. Темы
        all_skills = ["Честность", "Доброта", "Смелость", "Дружба", "Гигиена", "Трудолюбие", "Вежливость"]
        skills = st.multiselect("🎯 Чему научим сегодня?", all_skills, default=["Честность"])
        
        # 4. Режимы
        c1, c2 = st.columns(2)
        use_img = c1.checkbox("🎨 С картинкой", value=True)
        use_audio = c2.checkbox("🎧 Только Аудио", value=False)

        # 5. Длительность
        st.write("⏳ Длительность:")
        t_cols = st.columns(3)
        for i, t in enumerate([3, 5, 10]):
            btn_t = "primary" if st.session_state.time_val == t else "secondary"
            if t_cols[i].button(f"{t} min", key=f"t_{t}", type=btn_t, use_container_width=True):
                st.session_state.time_val = t
                st.rerun()

        # 6. Детали
        details = st.text_area("✍️ О чем будет история?")
        
        # 7. КНОПКА ГЕНЕРАЦИИ (Я добавил сюда передачу языка)
        if st.button("🚀 СОЗДАТЬ МАГИЮ", type="primary", use_container_width=True):
            with st.spinner("🧙‍♂️ Колдуем..."):
                try:
                    # Теперь мы передаем selected_lang в функцию
                    txt = generate_story_text(cn, selected_lang, skills, details, st.session_state.time_val)
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
                except Exception as e:
                    st.error(f"Ошибка: {e}")
