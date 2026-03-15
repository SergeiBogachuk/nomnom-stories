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


def get_bg_music_b64():
    try:
        with open("bg_music.mp3", "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None


def mount_bg_music():
    bg_b64 = get_bg_music_b64()
    if not bg_b64:
        return

    components.html(
        f"""
        <script>
        (function() {{
            let docRef = document;
            try {{
                if (window.parent && window.parent.document) {{
                    docRef = window.parent.document;
                }}
            }} catch (e) {{
                docRef = document;
            }}

            let bg = docRef.getElementById("nomnom-bg-music");
            if (!bg) {{
                bg = docRef.createElement("audio");
                bg.id = "nomnom-bg-music";
                bg.src = "data:audio/mp3;base64,{bg_b64}";
                bg.loop = true;
                bg.preload = "auto";
                bg.style.display = "none";
                docRef.body.appendChild(bg);
            }}

            bg.volume = 0.08;

            function startBg() {{
                try {{
                    bg.volume = 0.08;
                    const p = bg.play();
                    if (p) p.catch(() => {{}});
                }} catch (e) {{}}
            }}

            if (!docRef.body.dataset.nomnomBgBound) {{
                ["click", "touchstart", "keydown"].forEach(function(evt) {{
                    docRef.addEventListener(evt, startBg);
                }});
                docRef.body.dataset.nomnomBgBound = "1";
            }}

            startBg();
        }})();
        </script>
        """,
        height=0
    )


def stop_bg_music():
    components.html(
        """
        <script>
        (function() {
            let docRef = document;
            try {
                if (window.parent && window.parent.document) {
                    docRef = window.parent.document;
                }
            } catch (e) {
                docRef = document;
            }

            const bg = docRef.getElementById("nomnom-bg-music");
            if (bg) {
                try {
                    bg.pause();
                    bg.currentTime = 0;
                } catch (e) {}
            }
        })();
        </script>
        """,
        height=0
    )


def short_story_title(title, max_len=24):
    title = (title or "Сказка").replace("\n", " ").strip()
    return title if len(title) <= max_len else title[:max_len - 1] + "…"


def render_story_library(stories, prefix="lib"):
    if not stories or not getattr(stories, "data", None):
        st.caption("Пока нет сохранённых сказок")
        return

    for s in stories.data:
        full_title = s.get("title") or "Сказка"
        short_title = short_story_title(full_title)

        col_story, col_del = st.columns([6, 1], gap="small")

        with col_story:
            if st.button(
                short_title,
                key=f"{prefix}_story_{s['id']}",
                use_container_width=True,
                help=full_title
            ):
                st.session_state.view_story = s
                st.session_state.page_mode = "view"
                st.rerun()

        with col_del:
            if st.button("🗑", key=f"{prefix}_del_{s['id']}", help="Удалить"):
                if delete_story(s["id"]):
                    if (
                        st.session_state.view_story
                        and st.session_state.view_story.get("id") == s["id"]
                    ):
                        st.session_state.view_story = None
                        st.session_state.page_mode = "form"
                    st.rerun()


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
        "details": "✍️ Despre ce va fi povesteа?",
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

subtitle_dict = {
    "Русский": "Сказки на ночь с магией, добротой и уютом ✨",
    "English": "Bedtime stories filled with magic, kindness, and wonder ✨",
    "Română": "Povești de noapte pline de magie, bunătate și liniște ✨"
}


if "time_val" not in st.session_state:
    st.session_state.time_val = 5
if "view_story" not in st.session_state:
    st.session_state.view_story = None
if "sel_lang" not in st.session_state:
    st.session_state.sel_lang = "Русский"
if "page_mode" not in st.session_state:
    st.session_state.page_mode = "form"


if not st.session_state.get("logged_in", False):
    stop_bg_music()

    _, center, _ = st.columns([1, 2, 1])
    with center:
        st.markdown(
            """
            <div class="hero-badge">🌟 Добро пожаловать</div>
            <div class="hero-title">🌙 NomNom Stories</div>
            <div class="hero-subtitle">Вход в волшебную библиотеку сказок ✨</div>
            """,
            unsafe_allow_html=True
        )

        with st.form("login_form"):
            e = st.text_input("Email")
            p = st.text_input("Пароль", type="password")

            if st.form_submit_button("Войти", type="primary", use_container_width=True):
                if check_user(e, p):
                    st.session_state.logged_in = True
                    st.session_state.user_email = e
                    st.session_state.page_mode = "form"
                    st.rerun()
                else:
                    st.error("Ошибка входа")

else:
    T = lang_dict[st.session_state.sel_lang]
    stories = get_user_stories(st.session_state.user_email)

    with st.sidebar:
        try:
            st.image("logo.jpg", width=88)
        except:
            pass

        st.markdown(
            """
            <div class="sidebar-brand">🌙 NomNom Stories</div>
            <div class="sidebar-subbrand">Сказки на ночь для детей</div>
            """,
            unsafe_allow_html=True
        )

        st.success(f"Аккаунт: {st.session_state.user_email}")

        with st.expander(T["sidebar_library"], expanded=False):
            render_story_library(stories, prefix="side")

        st.divider()

        st.markdown('<div class="section-label">🎙 Настройки голоса</div>', unsafe_allow_html=True)
        voice_name = st.selectbox(T["sidebar_voice"], list(T["voices"].keys()), key="voice_select")
        voice_id = T["voices"][voice_name]

        if st.button(T["sidebar_new"], use_container_width=True, type="primary", key="sidebar_new_story_btn"):
            st.session_state.view_story = None
            st.session_state.page_mode = "form"
            st.rerun()

    if st.session_state.page_mode == "view" and st.session_state.view_story:
        s = st.session_state.view_story
        mount_bg_music()

        top1, top2 = st.columns([1, 6])

        with top1:
            if st.button("← Назад", use_container_width=True, key="back_story_btn"):
                st.session_state.view_story = None
                st.session_state.page_mode = "form"
                st.rerun()

        with top2:
            st.markdown(
                f"""
                <div class="hero-badge">📖 Готовая сказка</div>
                <div class="hero-title" style="font-size: 2.35rem;">{html.escape(s.get('title', 'Сказка'))}</div>
                <div class="hero-subtitle">{subtitle_dict[st.session_state.sel_lang]}</div>
                """,
                unsafe_allow_html=True
            )

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
                <div class="story-shell">
                    <div class="story-output">
                        {safe_story}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning("Текст сказки пустой или не сохранился.")

    else:
        stop_bg_music()

        _, center, _ = st.columns([1, 2, 1])

        with center:
            st.markdown(
                f"""
                <div class="hero-badge">🌟 Детские сказки на ночь</div>
                <div class="hero-title">🌙 NomNom Stories</div>
                <div class="hero-subtitle">{subtitle_dict[st.session_state.sel_lang]}</div>
                """,
                unsafe_allow_html=True
            )  

            st.markdown('<div class="section-label">👶 Для кого сказка?</div>', unsafe_allow_html=True)
            cn = st.text_input(T["child_name"], value="Даша")

            st.markdown('<div class="section-label">🌍 Язык истории</div>', unsafe_allow_html=True)
            lang_list = list(lang_dict.keys())
            new_lang = st.selectbox(
                "🌍 Language / Язык",
                lang_list,
                index=lang_list.index(st.session_state.sel_lang),
                key="lang_selector_center",
                label_visibility="collapsed"
            )

            if new_lang != st.session_state.sel_lang:
                st.session_state.sel_lang = new_lang
                st.rerun()

            st.markdown(
                f"""
                <div class="soft-info-chip">📍 {T['title']} • {st.session_state.sel_lang}</div>
                """,
                unsafe_allow_html=True
            )

            st.markdown('<div class="section-label">🎯 Навык или тема</div>', unsafe_allow_html=True)
            skills = st.multiselect(
                T["skills_label"],
                T["skills"],
                default=[T["skills"][0]],
                label_visibility="collapsed"
            )

            st.markdown('<div class="section-label">🎧 Формат</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                use_img = st.checkbox(T["opt_img"], value=True, key="use_img_checkbox")
            with c2:
                use_audio = st.checkbox(T["opt_audio"], value=False, key="use_audio_checkbox")

            st.markdown('<div class="section-label">⏳ Длительность</div>', unsafe_allow_html=True)
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

            st.markdown('<div class="section-label">✍️ Детали сюжета</div>', unsafe_allow_html=True)
            details = st.text_area(T["details"], label_visibility="collapsed")

            if st.button(T["btn_create"], type="primary", use_container_width=True, key="create_story_btn"):
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
                                st.session_state.page_mode = "view"
                                st.rerun()
                            else:
                                st.error("Не удалось сохранить сказку.")
                        else:
                            st.error("Не удалось сгенерировать текст сказки.")

                    except Exception as e:
                        st.error(f"Ошибка: {e}")
