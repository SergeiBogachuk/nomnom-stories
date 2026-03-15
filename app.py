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


def inject_app_icons():
    try:
        with open("logo.jpg", "rb") as f:
            icon_b64 = base64.b64encode(f.read()).decode()

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

                const head = docRef.head;
                const iconHref = "data:image/jpeg;base64,{icon_b64}";

                function upsertLink(rel, sizes="") {{
                    let link = head.querySelector(`link[rel="${{rel}}"]`);
                    if (!link) {{
                        link = docRef.createElement("link");
                        link.rel = rel;
                        head.appendChild(link);
                    }}
                    link.href = iconHref;
                    if (sizes) {{
                        link.setAttribute("sizes", sizes);
                    }}
                }}

                function upsertMeta(name, content) {{
                    let meta = head.querySelector(`meta[name="${{name}}"]`);
                    if (!meta) {{
                        meta = docRef.createElement("meta");
                        meta.name = name;
                        head.appendChild(meta);
                    }}
                    meta.content = content;
                }}

                upsertLink("icon", "32x32");
                upsertLink("shortcut icon");
                upsertLink("apple-touch-icon", "180x180");

                upsertMeta("apple-mobile-web-app-capable", "yes");
                upsertMeta("apple-mobile-web-app-title", "NomNom Stories");
                upsertMeta("mobile-web-app-capable", "yes");

                docRef.title = "NomNom Stories";
            }})();
            </script>
            """,
            height=0,
        )
    except Exception:
        pass


inject_app_icons()


def get_bg_music_b64():
    try:
        with open("bg_music.mp3", "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
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

            bg.volume = 0.18;

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


def short_story_title(title, fallback_title="Story", max_len=24):
    title = (title or fallback_title).replace("\n", " ").strip()
    return title if len(title) <= max_len else title[:max_len - 1] + "…"


def render_story_library(stories, T, prefix="lib"):
    if not stories or not getattr(stories, "data", None):
        st.caption(T.get("no_saved_stories", "No saved stories yet"))
        return

    for s in stories.data:
        full_title = s.get("title") or T.get("story_fallback", "Story")
        short_title = short_story_title(full_title, T.get("story_fallback", "Story"))

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
            if st.button("🗑", key=f"{prefix}_del_{s['id']}", help=T.get("delete_help", "Delete")):
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
        "default_child_name": "Даша",
        "skills_label": "🎯 Чему научим сегодня?",
        "duration": "⏳ Длительность:",
        "duration_btn_suffix": "min",
        "details": "✍️ О чем будет сказка?",
        "btn_create": "🚀 СОЗДАТЬ МАГИЮ ✨",
        "sidebar_library": "📚 Мои сказки",
        "sidebar_voice": "🔊 Голос",
        "sidebar_new": "➕ Новая сказка",
        "opt_img": "🎨 Текст + Картинка",
        "opt_audio": "🎧 Только Аудио",
        "account_label": "Аккаунт",
        "sidebar_tagline": "Сказки на ночь для детей",
        "voice_settings": "🎙 Настройки голоса",
        "ready_story": "📖 Готовая сказка",
        "back_btn": "← Назад",
        "empty_story_text": "Текст сказки пустой или не сохранился.",
        "no_saved_stories": "Пока нет сохранённых сказок",
        "section_for_whom": "👶 Для кого сказка?",
        "section_language": "🌍 Язык истории",
        "section_skill": "🎯 Навык или тема",
        "section_format": "🎧 Формат",
        "section_duration": "⏳ Длительность",
        "section_details": "✍️ Детали сюжета",
        "spinner_magic": "✨ Колдуем...",
        "spinner_voice": "🔊 Озвучиваем...",
        "error_save_story": "Не удалось сохранить сказку.",
        "error_gen_story": "Не удалось сгенерировать текст сказки.",
        "story_fallback": "Сказка",
        "delete_help": "Удалить",
        "error_prefix": "Ошибка",
        "login_badge": "🌟 Добро пожаловать",
        "login_subtitle": "Вход в волшебную библиотеку сказок ✨",
        "login_btn": "Войти",
        "login_error": "Ошибка входа",
        "email_label": "Email",
        "password_label": "Пароль",
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
        "default_child_name": "Emma",
        "skills_label": "🎯 What to teach today?",
        "duration": "⏳ Duration:",
        "duration_btn_suffix": "min",
        "details": "✍️ What is the story about?",
        "btn_create": "🚀 CREATE MAGIC ✨",
        "sidebar_library": "📚 My Stories",
        "sidebar_voice": "🔊 Voice",
        "sidebar_new": "➕ New Story",
        "opt_img": "🎨 Text + Image",
        "opt_audio": "🎧 Audio Only",
        "account_label": "Account",
        "sidebar_tagline": "Bedtime stories for children",
        "voice_settings": "🎙 Voice settings",
        "ready_story": "📖 Your story is ready",
        "back_btn": "← Back",
        "empty_story_text": "The story text is empty or was not saved.",
        "no_saved_stories": "No saved stories yet",
        "section_for_whom": "👶 Who is the story for?",
        "section_language": "🌍 Story language",
        "section_skill": "🎯 Skill or theme",
        "section_format": "🎧 Format",
        "section_duration": "⏳ Duration",
        "section_details": "✍️ Story details",
        "spinner_magic": "✨ Creating magic...",
        "spinner_voice": "🔊 Generating voice...",
        "error_save_story": "Failed to save the story.",
        "error_gen_story": "Failed to generate the story text.",
        "story_fallback": "Story",
        "delete_help": "Delete",
        "error_prefix": "Error",
        "login_badge": "🌟 Welcome",
        "login_subtitle": "Enter your magical bedtime stories library ✨",
        "login_btn": "Log in",
        "login_error": "Login failed",
        "email_label": "Email",
        "password_label": "Password",
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
        "default_child_name": "Ana",
        "skills_label": "🎯 Ce învățăm astăzi?",
        "duration": "⏳ Durată:",
        "duration_btn_suffix": "min",
        "details": "✍️ Despre ce va fi povestea?",
        "btn_create": "🚀 CREEAZĂ MAGIE ✨",
        "sidebar_library": "📚 Poveștile mele",
        "sidebar_voice": "🔊 Voce",
        "sidebar_new": "➕ Poveste nouă",
        "opt_img": "🎨 Text + Imagine",
        "opt_audio": "🎧 Doar Audio",
        "account_label": "Cont",
        "sidebar_tagline": "Povești de noapte pentru copii",
        "voice_settings": "🎙 Setări voce",
        "ready_story": "📖 Povestea este gata",
        "back_btn": "← Înapoi",
        "empty_story_text": "Textul poveștii este gol sau nu a fost salvat.",
        "no_saved_stories": "Încă nu există povești salvate",
        "section_for_whom": "👶 Pentru cine este povestea?",
        "section_language": "🌍 Limba poveștii",
        "section_skill": "🎯 Abilitate sau temă",
        "section_format": "🎧 Format",
        "section_duration": "⏳ Durată",
        "section_details": "✍️ Detalii ale poveștii",
        "spinner_magic": "✨ Creăm magie...",
        "spinner_voice": "🔊 Generăm vocea...",
        "error_save_story": "Povestea nu a putut fi salvată.",
        "error_gen_story": "Textul poveștii nu a putut fi generat.",
        "story_fallback": "Poveste",
        "delete_help": "Șterge",
        "error_prefix": "Eroare",
        "login_badge": "🌟 Bine ai venit",
        "login_subtitle": "Intră în biblioteca magică de povești ✨",
        "login_btn": "Autentificare",
        "login_error": "Autentificare eșuată",
        "email_label": "Email",
        "password_label": "Parolă",
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

    L = lang_dict.get(st.session_state.get("sel_lang", "Русский"), lang_dict["Русский"])

    _, center, _ = st.columns([1, 2, 1])
    with center:
        st.markdown(
            f"""
            <div class="hero-badge">{L.get("login_badge", "🌟 Welcome")}</div>
            <div class="hero-title">🌙 NomNom Stories</div>
            <div class="hero-subtitle">{L.get("login_subtitle", "")}</div>
            """,
            unsafe_allow_html=True
        )

        with st.form("login_form"):
            e = st.text_input(L.get("email_label", "Email"))
            p = st.text_input(L.get("password_label", "Password"), type="password")

            if st.form_submit_button(L.get("login_btn", "Log in"), type="primary", use_container_width=True):
                if check_user(e, p):
                    st.session_state.logged_in = True
                    st.session_state.user_email = e
                    st.session_state.page_mode = "form"
                    st.rerun()
                else:
                    st.error(L.get("login_error", "Login failed"))

else:
    T = lang_dict.get(st.session_state.sel_lang, lang_dict["Русский"])
    stories = get_user_stories(st.session_state.user_email)

    with st.sidebar:
        try:
            st.image("logo.jpg", width=88)
        except Exception:
            pass

        st.markdown(
            f"""
            <div class="sidebar-brand">🌙 NomNom Stories</div>
            <div class="sidebar-subbrand">{T.get("sidebar_tagline", "")}</div>
            """,
            unsafe_allow_html=True
        )

        st.success(f'{T.get("account_label", "Account")}: {st.session_state.user_email}')

        with st.expander(T.get("sidebar_library", "Stories"), expanded=False):
            render_story_library(stories, T, prefix="side")

        st.divider()

        st.markdown(
            f'<div class="section-label">{T.get("voice_settings", "🎙 Voice settings")}</div>',
            unsafe_allow_html=True
        )

        voice_name = st.selectbox(
            T.get("sidebar_voice", "🔊 Voice"),
            list(T.get("voices", {}).keys()),
            key="voice_select"
        )
        voice_id = T.get("voices", {}).get(voice_name)

        if st.button(
            T.get("sidebar_new", "➕ New Story"),
            use_container_width=True,
            type="primary",
            key="sidebar_new_story_btn"
        ):
            st.session_state.view_story = None
            st.session_state.page_mode = "form"
            st.rerun()

    if st.session_state.page_mode == "view" and st.session_state.view_story:
        s = st.session_state.view_story
        mount_bg_music()

        top1, top2 = st.columns([1, 6])

        with top1:
            if st.button(T.get("back_btn", "← Back"), use_container_width=True, key="back_story_btn"):
                st.session_state.view_story = None
                st.session_state.page_mode = "form"
                st.rerun()

        with top2:
            st.markdown(
                f"""
                <div class="hero-badge">{T.get("ready_story", "📖 Story ready")}</div>
                <div class="hero-title" style="font-size: 2.35rem;">{html.escape(s.get('title', T.get("story_fallback", "Story")))}</div>
                <div class="hero-subtitle">{subtitle_dict.get(st.session_state.sel_lang, "")}</div>
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
            st.warning(T.get("empty_story_text", "Story text is empty."))

    else:
        stop_bg_music()

        _, center, _ = st.columns([1, 2, 1])

        with center:
            st.markdown(
                f"""
                <div class="hero-badge">🌟 NomNom Stories</div>
                <div class="hero-title">🌙 NomNom Stories</div>
                <div class="hero-subtitle">{subtitle_dict.get(st.session_state.sel_lang, "")}</div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="section-label">{T.get("section_for_whom", "👶 For whom?")}</div>',
                unsafe_allow_html=True
            )
            cn = st.text_input(T.get("child_name", "Child's Name"), value=T.get("default_child_name", "Dasha"))

            st.markdown(
                f'<div class="section-label">{T.get("section_language", "🌍 Language")}</div>',
                unsafe_allow_html=True
            )
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
                <div class="soft-info-chip">📍 {T.get('title', 'NomNom Stories')} • {st.session_state.sel_lang}</div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="section-label">{T.get("section_skill", "🎯 Skill")}</div>',
                unsafe_allow_html=True
            )
            skills = st.multiselect(
                T.get("skills_label", "Skills"),
                T.get("skills", []),
                default=[T.get("skills", [""])[0]] if T.get("skills") else [],
                label_visibility="collapsed"
            )

            st.markdown(
                f'<div class="section-label">{T.get("section_format", "🎧 Format")}</div>',
                unsafe_allow_html=True
            )
            c1, c2 = st.columns(2)
            with c1:
                use_img = st.checkbox(T.get("opt_img", "🎨 Text + Image"), value=True, key="use_img_checkbox")
            with c2:
                use_audio = st.checkbox(T.get("opt_audio", "🎧 Audio Only"), value=False, key="use_audio_checkbox")

            st.markdown(
                f'<div class="section-label">{T.get("section_duration", "⏳ Duration")}</div>',
                unsafe_allow_html=True
            )
            t_cols = st.columns(3)
            for i, t in enumerate([3, 5, 10]):
                if t_cols[i].button(
                    f'{t} {T.get("duration_btn_suffix", "min")}',
                    key=f"t_{t}",
                    type="primary" if st.session_state.time_val == t else "secondary",
                    use_container_width=True
                ):
                    st.session_state.time_val = t
                    st.rerun()

            st.markdown(
                f'<div class="section-label">{T.get("section_details", "✍️ Details")}</div>',
                unsafe_allow_html=True
            )
            details = st.text_area(T.get("details", "Story details"), label_visibility="collapsed")

            if st.button(
                T.get("btn_create", "🚀 Create"),
                type="primary",
                use_container_width=True,
                key="create_story_btn"
            ):
                with st.spinner(T.get("spinner_magic", "✨ Creating...")):
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
                            ttl = first_line.strip() or T.get("story_fallback", "Story")
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

                                if use_audio and voice_id:
                                    with st.spinner(T.get("spinner_voice", "🔊 Generating voice...")):
                                        audio_b64 = get_speech_b64(story_body, voice_id)
                                        if audio_b64:
                                            update_audio(new_id, audio_b64)
                                            current_story["audio_base64"] = audio_b64

                                st.session_state.view_story = current_story
                                st.session_state.page_mode = "view"
                                st.rerun()
                            else:
                                st.error(T.get("error_save_story", "Failed to save story."))
                        else:
                            st.error(T.get("error_gen_story", "Failed to generate story."))

                    except Exception as e:
                        st.error(f'{T.get("error_prefix", "Error")}: {e}')
