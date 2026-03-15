import streamlit as st
import base64
import streamlit.components.v1 as components

from styles import apply_styles
from database import check_user, get_user_stories, save_story, update_audio
from ai_engine import generate_story_text, generate_image, get_speech_b64

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

lang_dict = {
    "Русский": {
        "title": "✨ NomNom Stories",
        "child_name": "Имя ребенка", "skills_label": "🎯 Чему научим сегодня?",
        "duration": "⏳ Длительность:", "details": "✍️ О чем будет сказка?",
        "btn_create": "🚀 СОЗДАТЬ МАГИЮ ✨", "sidebar_library": "📚 Мои сказки",
        "sidebar_voice": "🔊 Голос", "sidebar_new": "➕ Новая сказка",
        "opt_img": "🎨 Текст + Картинка", "opt_audio": "🎧 Только Аудио",
        "voices": {"Марина": "ymDCYd8puC7gYjxIamPt", "Николай": "8JVbfL6oEdmuxKn5DK2C", "Алиса": "EXAVITQu4vr4xnSDxMaL"},
        "skills": ["Честность", "Смелость", "Доброта", "Трудолюбие", "Вежливость", "Гигиена", "Дружба", "Усидчивость"]
    }
}

# --- ЛОГИКА ВХОДА ---
if not st.session_state.get("logged_in", False):
    _, center, _ = st.columns([1, 2, 1]) # Создаем колонки для центрирования
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
    # --- ОСНОВНОЙ ЭКРАН ---
    if 'time_val' not in st.session_state: st.session_state.time_val = 5
    if 'view_story' not in st.session_state: st.session_state.view_story = None
    if 'sel_lang' not in st.session_state: st.session_state.sel_lang = "Русский"
    T = lang_dict["Русский"]

    with st.sidebar:
        st.success(f"Аккаунт: {st.session_state.user_email}")
        with st.expander(T['sidebar_library']):
            stories = get_user_stories(st.session_state.user_email)
            for s in stories.data:
                if st.button(s.get('title') or "Сказка", key=f"s_{s['id']}", use_container_width=True):
                    st.session_state.view_story = s
                    st.rerun()
        st.divider()
        voice_name = st.selectbox(T['sidebar_voice'], list(T['voices'].keys()))
        voice_id = T['voices'][voice_name]
        if st.button(T['sidebar_new']):
            st.session_state.view_story = None
            st.rerun()

    if st.session_state.view_story:
        # Экран готовой сказки
        s = st.session_state.view_story
        st.title(f"📖 {s.get('title')}")
        components.html(get_bg_music_html(), height=0)
        
        if s.get('audio_base64'):
            st.audio(base64.b64decode(s['audio_base64']))
        else:
            if st.button("🔊 Озвучить", type="primary"):
                with st.spinner("..."):
                    audio_b64 = get_speech_b64(s['story_text'], voice_id)
                    if audio_b64:
                        update_audio(s['id'], audio_b64)
                        st.audio(base64.b64decode(audio_b64))
                        st.rerun()
        
        if s.get('image_url'): st.image(s['image_url'], use_container_width=True)
        st.markdown(f'<div class="story-output">{s["story_text"]}</div>', unsafe_allow_html=True)
            
    else:
        # ЭКРАН СОЗДАНИЯ (Центрируем поля)
        _, center, _ = st.columns([1, 2, 1])
        with center:
            st.title(T['title'])
            cn = st.text_input(T['child_name'], value="Даша")
            skills = st.multiselect(T['skills_label'], T['skills'], default=["Честность"])
            
            c1, c2 = st.columns(2)
            with c1: use_img = st.checkbox(T['opt_img'], value=True)
            with c2: use_audio = st.checkbox(T['opt_audio'], value=False)
            st.session_state.mode_audio = use_audio

            st.write(T['duration'])
            t_cols = st.columns(3)
            for i, t in enumerate([3, 5, 10]):
                if t_cols[i].button(f"{t} min", key=f"t_{t}", type="primary" if st.session_state.time_val == t else "secondary", use_container_width=True):
                    st.session_state.time_val = t
                    st.rerun()

            details = st.text_area(T['details'])

            if st.button(T['btn_create'], type="primary", use_container_width=True):
                with st.spinner("✨ Колдуем..."):
                    try:
                        # 1. Генерируем текст сказки
                        txt = generate_story_text(cn, st.session_state.sel_lang, skills, details, st.session_state.time_val)
                        if not txt:
                            st.error("Ошибка: Текст не создан")
                            st.stop()
                            
                        ttl = txt.split('\n')[0].strip()
                        
                        # 2. Генерируем картинку, только если НЕ выбран режим "Только Аудио"
                        url = None
                        if not use_audio and use_img:
                            url = generate_image(ttl)
                        
                        # 3. ПОДГОТОВКА ДАННЫХ (БЕЗ аудио_base64 для обхода ошибки кэша)
                        clean_story = {
                            "user_email": st.session_state.user_email,
                            "child_name": cn,
                            "title": ttl,
                            "story_text": txt,
                            "image_url": url
                        }
                        
                        # ШАГ 1: Сохраняем основную запись
                        res = save_story(clean_story)
                        
                        # ШАГ 2: Если сохранение успешно, получаем ID и добавляем аудио
                        if res and hasattr(res, 'data') and len(res.data) > 0:
                            new_id = res.data[0]['id']
                            
                            if use_audio:
                                with st.spinner("🔊 Озвучиваем..."):
                                    audio_b64 = get_speech_b64(txt, voice_id)
                                    if audio_b64:
                                        # Используем новую функцию обновления из database.py
                                        update_audio(new_id, audio_b64)
                        
                        # Перезагружаем страницу, чтобы сказка появилась в списке
                        st.rerun()
                        
                    except Exception as e: 
                        st.error(f"Критическая ошибка: {e}")
