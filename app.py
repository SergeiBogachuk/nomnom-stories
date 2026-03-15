import streamlit as st
import base64
import html
import streamlit.components.v1 as components

from styles import apply_styles
from database import check_user, get_user_stories, save_story, update_audio, delete_story
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
            return f'''
                <audio autoplay loop id="bg_music">
                    <source src="data:audio/mp3;base64,{data}" type="audio/mp3">
                </audio>
                <script>
                    document.getElementById("bg_music").volume = 0.1;
                </script>
            '''
    except:
        return ""


lang_dict = {
    "Русский": {
        "title": "✨ NomNom Stories",
        "child_name": "Имя ребенка",
        "skills_label": "🎯 Чему научим сегодня?",
        "duration": "⏳ Длительность:",
        "details": "✍️ О чем будет сказка?",
        "btn_create": "🚀 СОЗДАТЬ МАГИЮ ✨",
        "sidebar_library": "📚 Мои сказки",
        "sidebar_voice": "🔊 Голос",
        "sidebar_new": "➕ Новая сказка",
        "opt_img": "🎨 Текст + Картинка",
        "opt_audio": "🎧 Только Аудио",
        "voices": {
            "Марина": "ymDCYd8puC7gYjxIamPt",
            "Николай": "8JVbfL6oEdmuxKn5DK2C",
            "Алиса": "EXAVITQu4vr4xnSDxMaL"
        },
        "skills": [
            "Честность", "Смелость", "Доброта", "Трудолюбие",
            "Вежливость", "Гигиена", "Дружба", "Усидчивость"
        ]
    },
    "English": {
        "title": "✨ NomNom Stories",
        "child_name": "Child's Name",
        "skills_label": "🎯 What to teach today?",
        "duration": "⏳ Duration:",
        "details": "✍️ What is the story about?",
        "btn_create": "🚀 CREATE MAGIC ✨",
        "sidebar_library": "📚 My Stories",
        "sidebar_voice": "🔊 Voice",
        "sidebar_new": "➕ New Story",
        "opt_img": "🎨 Text + Image",
        "opt_audio": "🎧 Audio Only",
        "voices": {
            "Alice": "EXAVITQu4vr4xnSDxMaL",
            "Nicholas": "8JVbfL6oEdmuxKn5DK2C"
        },
        "skills": [
            "Honesty", "Bravery", "Kindness", "Hard work",
            "Politeness", "Hygiene", "Friendship", "Patience"
        ]
    },
    "Română": {
        "title": "✨ NomNom Stories",
        "child_name": "Numele copilului",
        "skills_label": "🎯 Ce învățăm astăzi?",
        "duration": "⏳ Durată:",
        "details": "✍️ Despre ce va fi povestea?",
        "btn_create": "🚀 CREEAZĂ MAGIE ✨",
        "sidebar_library": "📚 Poveștile mele",
        "sidebar_voice": "🔊 Voce",
        "sidebar_new": "➕ Poveste nouă",
        "opt_img": "🎨 Text + Imagine",
        "opt_audio": "🎧 Doar Audio",
        "voices": {
            "Alina": "EXAVITQu4vr4xnSDxMaL",
            "Marcel": "8JVbfL6oEdmuxKn5DK2C"
        },
        "skills": [
            "Onestitate", "Curaj", "Bunătate", "Hărnicie",
            "Politețe", "Igienă", "Prietenie", "Răbdare"
        ]
    }
}


if not st.session_state.get("logged_in", False):
    _, center, _ = st.columns([1, 2, 1])
    with center:
        st.title("🌟 Вход")
        with st.form("login_form"):
            e = st.text_input("Email")
            p = st.text_input("Пароль", type="password")

            if st.form_submit_button("Войти", type="primary", use_container_width=True):
                if check_user(e, p):
                    st.session_state.logged_in = True
                    st.session_state.user_email = e
                    st.rerun()
                else:
                    st.error("Ошибка входа")

else:
    if "time_val" not in st.session_state:
        st.session_state.time_val = 5
    if "view_story" not in st.session_state:
        st.session_state.view_story = None
    if "sel_lang" not in st.session_state:
        st.session_state.sel_lang = "Русский"

    T = lang_dict[st.session_state.sel_lang]

    with st.sidebar:
        st.success(f"Аккаунт: {st.session_state.user_email}")

        with st.expander(T["sidebar_library"]):
            stories = get_user_stories(st.session_state.user_email)
            for s in stories.data:
                col_story, col_del = st.columns([4, 1])

                with col_story:
                    if st.button(s.get("title") or "Сказка", key=f"s_{s['id']}", use_container_width=True):
                        st.session_state.view_story = s
                        st.rerun()

                with col_del:
                    if st.button("🗑️", key=f"del_{s['id']}", help="Удалить"):
                        if delete_story(s["id"]):
                            st.session_state.view_story = None
                            st.rerun()

        st.divider()

        voice_name = st.selectbox(T["sidebar_voice"], list(T["voices"].keys()))
        voice_id = T["voices"][voice_name]

        if st.button(T["sidebar_new"]):
            st.session_state.view_story = None
            st.rerun()

    if st.session_state.view_story:
        s = st.session_state.view_story

        st.title(f"📖 {s.get('title', 'Сказка')}")
        components.html(get_bg_music_html(), height=0)

        if s.get("audio_base64"):
            st.audio(base64.b64decode(s["audio_base64"]))

        if s.get("image_url"):
            st.image(s["image_url"], use_container_width=True)

        story_text = s.get("story_text", "")
        story_text = story_text.strip() if story_text else ""

        if story_text:
            safe_story = html.escape(story_text).replace("\n", "<br>")
            st.markdown(
                f"""
                <div class="story-output" style="
                    white-space: pre-wrap;
                    color: #222222;
                    background: #ffffff;
                    padding: 20px;
                    border-radius: 16px;
                    line-height: 1.7;
                    font-size: 18px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                    margin-top: 16px;
                ">
                    {safe_story}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning("Текст сказки пустой или не сохранился.")

    else:
        _, center, _ = st.columns([1, 2, 1])

        with center:
            st.title(T["title"])

            cn = st.text_input(T["child_name"], value="Даша")

            lang_list = list(lang_dict.keys())
            st.info(f"📍 {T['title']} - {st.session_state.sel_lang}")

            new_lang = st.selectbox(
                "🌍 Language / Язык",
                lang_list,
                index=lang_list.index(st.session_state.sel_lang),
                key="lang_selector_center"
            )

            if new_lang != st.session_state.sel_lang:
                st.session_state.sel_lang = new_lang
                st.rerun()

            skills = st.multiselect(T["skills_label"], T["skills"], default=[T["skills"][0]])

            c1, c2 = st.columns(2)
            with c1:
                use_img = st.checkbox(T["opt_img"], value=True)
            with c2:
                use_audio = st.checkbox(T["opt_audio"], value=False)

            st.write(T["duration"])

            t_cols = st.columns(3)
            for i, t in enumerate([3, 5, 10]):
                if t_cols[i].button(
                    f"{t} min",
                    key=f"t_{t}",
                    type="primary" if st.session_state.time_val == t else "secondary",
                    use_container_width=True
                ):
                    st.session_state.time_val = t
                    st.rerun()

            details = st.text_area(T["details"])

            if st.button(T["btn_create"], type="primary", use_container_width=True):
                with st.spinner("✨ Колдуем..."):
                    try:
                        full_txt = generate_story_text(
                            cn,
                            st.session_state.sel_lang,
                            skills,
                            details,
                            st.session_state.time_val
                        )

                        if full_txt:
                            full_txt = full_txt.strip()

                            first_line, sep, rest = full_txt.partition("\n")
                            ttl = first_line.strip() or "Сказка"
                            story_body = rest.strip() if rest.strip() else full_txt

                            url = generate_image(ttl) if use_img else None

                            res = save_story({
                                "user_email": st.session_state.user_email,
                                "child_name": cn,
                                "title": ttl,
                                "story_text": story_body,
                                "image_url": url
                            })

                            if res and len(res.data) > 0:
                                current_story = res.data[0]
                                new_id = current_story["id"]

                                current_story["title"] = ttl
                                current_story["story_text"] = story_body
                                current_story["image_url"] = url

                                if use_audio:
                                    with st.spinner("🔊 Озвучиваем..."):
                                        audio_b64 = get_speech_b64(story_body, voice_id)
                                        if audio_b64:
                                            update_audio(new_id, audio_b64)
                                            current_story["audio_base64"] = audio_b64

                                st.session_state.view_story = current_story
                                st.rerun()
                            else:
                                st.error("Не удалось сохранить сказку.")

                        else:
                            st.error("Не удалось сгенерировать текст сказки.")

                    except Exception as e:
                        st.error(f"Ошибка: {e}")
