import base64
import html
import re

import streamlit as st
import streamlit.components.v1 as components

from ai_engine import generate_image, generate_story_text, get_speech_b64
from database import check_user, delete_story, get_user_stories, save_story, update_audio
from styles import apply_styles

st.set_page_config(
    page_title="NomNom Stories",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_styles()


def inject_app_icons():
    try:
        with open("logo.jpg", "rb") as file:
            icon_b64 = base64.b64encode(file.read()).decode()

        components.html(
            f"""
            <script>
            (function() {{
                let docRef = document;
                try {{
                    if (window.parent && window.parent.document) {{
                        docRef = window.parent.document;
                    }}
                }} catch (error) {{
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
        with open("bg_music.mp3", "rb") as file:
            return base64.b64encode(file.read()).decode()
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
            }} catch (error) {{
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

            bg.volume = 0.16;

            function startBg() {{
                try {{
                    const playPromise = bg.play();
                    if (playPromise) {{
                        playPromise.catch(() => {{}});
                    }}
                }} catch (error) {{}}
            }}

            if (!docRef.body.dataset.nomnomBgBound) {{
                ["click", "touchstart", "keydown"].forEach(function(eventName) {{
                    docRef.addEventListener(eventName, startBg, {{ passive: true }});
                }});
                docRef.body.dataset.nomnomBgBound = "1";
            }}

            startBg();
        }})();
        </script>
        """,
        height=0,
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
            } catch (error) {
                docRef = document;
            }

            const bg = docRef.getElementById("nomnom-bg-music");
            if (bg) {
                try {
                    bg.pause();
                    bg.currentTime = 0;
                } catch (error) {}
            }
        })();
        </script>
        """,
        height=0,
    )


def short_story_title(title, fallback_title="Story", max_len=24):
    title = (title or fallback_title).replace("\n", " ").strip()
    return title if len(title) <= max_len else title[: max_len - 1] + "…"


def extract_story_parts(full_text, fallback_title):
    cleaned = (full_text or "").replace("\r\n", "\n").strip()
    cleaned = cleaned.replace(":::writing", "").replace("###", "").strip()
    cleaned = re.sub(r"^#{1,6}\s*", "", cleaned, flags=re.MULTILINE)

    first_line, _, rest = cleaned.partition("\n")
    title = first_line.strip().strip("\"'“”«»")
    title = re.sub(r"^(title|заголовок|titlu)\s*[:\-]\s*", "", title, flags=re.IGNORECASE)
    title = title or fallback_title
    body = rest.strip() if rest.strip() else cleaned

    return title, body


def validate_story_request(child_name, skills, copy_pack):
    errors = []

    if not child_name.strip():
        errors.append(copy_pack.get("error_child_name", "Enter the child's name."))
    if not skills:
        errors.append(copy_pack.get("error_skills", "Choose at least one skill or theme."))

    return errors


def render_story_library(stories, copy_pack, prefix="lib"):
    if not stories or not getattr(stories, "data", None):
        st.caption(copy_pack.get("no_saved_stories", "No saved stories yet"))
        return

    for story in stories.data:
        full_title = story.get("title") or copy_pack.get("story_fallback", "Story")
        short_title = short_story_title(full_title, copy_pack.get("story_fallback", "Story"))

        col_story, col_delete = st.columns([6, 1], gap="small")

        with col_story:
            if st.button(
                short_title,
                key=f"{prefix}_story_{story['id']}",
                use_container_width=True,
                help=full_title,
            ):
                st.session_state.view_story = story
                st.session_state.page_mode = "view"
                st.rerun()

        with col_delete:
            if st.button(
                "🗑",
                key=f"{prefix}_del_{story['id']}",
                help=copy_pack.get("delete_help", "Delete"),
            ):
                if delete_story(story["id"]):
                    if (
                        st.session_state.view_story
                        and st.session_state.view_story.get("id") == story["id"]
                    ):
                        st.session_state.view_story = None
                        st.session_state.page_mode = "form"
                    st.rerun()


lang_dict = {
    "Русский": {
        "title": "NomNom Stories",
        "subtitle": "Тёплые сказки на ночь, которые мягко развивают важные навыки.",
        "login_badge": "Для родителей",
        "login_subtitle": "Соберите свою спокойную библиотеку историй для сна, поддержки и роста.",
        "login_btn": "Войти",
        "login_error": "Не удалось войти. Проверь email и пароль.",
        "email_label": "Email",
        "password_label": "Пароль",
        "child_name": "Имя ребёнка",
        "child_placeholder": "Например: Даша",
        "default_child_name": "Даша",
        "skills_label": "Какие навыки поддержим этой сказкой?",
        "skills_help": "Лучше выбрать 1-2 темы, чтобы история получилась цельной и мягкой.",
        "duration": "Длительность",
        "duration_btn_suffix": "мин",
        "details": "О чём сейчас важно рассказать?",
        "details_placeholder": "Например: ребёнок боится темноты, скучает по детскому саду или учится делиться игрушками.",
        "details_help": "Можно описать ситуацию, любимых животных, настроение ребёнка или желаемый финал.",
        "btn_create": "Создать сказку",
        "btn_create_hint": "Мы сделаем историю тёплой, безопасной и подходящей для чтения перед сном.",
        "sidebar_library": "Мои сказки",
        "sidebar_voice": "Голос рассказчика",
        "sidebar_new": "Новая сказка",
        "sidebar_tagline": "Сказки для сна, близости и маленьких важных побед.",
        "voice_settings": "Озвучка",
        "ready_story": "Сказка готова",
        "back_btn": "← Назад",
        "empty_story_text": "Текст сказки пустой или не сохранился.",
        "no_saved_stories": "Пока нет сохранённых сказок",
        "section_for_whom": "Для кого сказка",
        "section_language": "Язык истории",
        "section_skill": "Навык или тема",
        "section_format": "Что добавить",
        "section_duration": "Сколько будет длиться чтение",
        "section_details": "Детали сюжета",
        "section_summary": "Что получится",
        "spinner_magic": "Плетём историю...",
        "spinner_voice": "Добавляем голос...",
        "spinner_cover": "Рисуем обложку...",
        "error_save_story": "Не удалось сохранить сказку.",
        "error_gen_story": "Не удалось сгенерировать текст сказки.",
        "story_fallback": "Сказка",
        "delete_help": "Удалить",
        "error_prefix": "Ошибка",
        "account_label": "Аккаунт",
        "section_parent_note": "Каждая история создаётся с мягкой развивающей линией, без жёстких нравоучений и лишней тревоги.",
        "summary_template": "История для {child_name} на {time_val} мин: {skills}.",
        "summary_default_skills": "мягкая поддержка и спокойствие",
        "opt_img": "Добавить иллюстрацию",
        "opt_audio": "Добавить озвучку",
        "voice_hint": "Выберите голос, если хотите сразу получить аудиоверсию сказки.",
        "view_hint": "Можно читать самим или включить озвучку, если нужен спокойный ритуал перед сном.",
        "error_child_name": "Напиши имя ребёнка.",
        "error_skills": "Выбери хотя бы один навык или тему.",
        "language_selector": "Язык",
        "voices": {
            "Марина": "ymDCYd8puC7gYjxIamPt",
            "Николай": "8JVbfL6oEdmuxKn5DK2C",
            "Алиса": "EXAVITQu4vr4xnSDxMaL",
        },
        "skills": [
            "Честность",
            "Смелость",
            "Доброта",
            "Трудолюбие",
            "Вежливость",
            "Гигиена",
            "Дружба",
            "Усидчивость",
        ],
    },
    "English": {
        "title": "NomNom Stories",
        "subtitle": "Warm bedtime stories that gently support emotional growth and everyday skills.",
        "login_badge": "For parents",
        "login_subtitle": "Build a calm little library of stories for sleep, connection, and confidence.",
        "login_btn": "Log in",
        "login_error": "Login failed. Please check your email and password.",
        "email_label": "Email",
        "password_label": "Password",
        "child_name": "Child's name",
        "child_placeholder": "For example: Emma",
        "default_child_name": "Emma",
        "skills_label": "Which skills should this story gently support?",
        "skills_help": "Choosing 1-2 themes usually creates the most focused and soothing story.",
        "duration": "Duration",
        "duration_btn_suffix": "min",
        "details": "What feels important right now?",
        "details_placeholder": "For example: the child is afraid of the dark, misses preschool, or is learning to share toys.",
        "details_help": "You can mention favorite animals, a current struggle, bedtime mood, or the ending you hope for.",
        "btn_create": "Create story",
        "btn_create_hint": "We will make it gentle, age-appropriate, and comfortable for bedtime.",
        "sidebar_library": "My stories",
        "sidebar_voice": "Narrator voice",
        "sidebar_new": "New story",
        "sidebar_tagline": "Bedtime stories for closeness, calm, and small brave steps.",
        "voice_settings": "Narration",
        "ready_story": "Your story is ready",
        "back_btn": "← Back",
        "empty_story_text": "The story text is empty or was not saved.",
        "no_saved_stories": "No saved stories yet",
        "section_for_whom": "Who is this story for",
        "section_language": "Story language",
        "section_skill": "Skill or theme",
        "section_format": "What to include",
        "section_duration": "Reading length",
        "section_details": "Story details",
        "section_summary": "What you'll get",
        "spinner_magic": "Weaving your story...",
        "spinner_voice": "Adding narration...",
        "spinner_cover": "Painting the cover...",
        "error_save_story": "Failed to save the story.",
        "error_gen_story": "Failed to generate the story text.",
        "story_fallback": "Story",
        "delete_help": "Delete",
        "error_prefix": "Error",
        "account_label": "Account",
        "section_parent_note": "Each story is built to model the chosen skill gently, without fear, shame, or heavy-handed moralizing.",
        "summary_template": "A {time_val}-minute story for {child_name}: {skills}.",
        "summary_default_skills": "gentle support and calm",
        "opt_img": "Add illustration",
        "opt_audio": "Add narration",
        "voice_hint": "Choose a voice if you want an audio version right away.",
        "view_hint": "You can read it yourself or play the narration when bedtime needs a softer rhythm.",
        "error_child_name": "Please enter the child's name.",
        "error_skills": "Choose at least one skill or theme.",
        "language_selector": "Language",
        "voices": {
            "Alice": "EXAVITQu4vr4xnSDxMaL",
            "Nicholas": "8JVbfL6oEdmuxKn5DK2C",
        },
        "skills": [
            "Honesty",
            "Bravery",
            "Kindness",
            "Hard work",
            "Politeness",
            "Hygiene",
            "Friendship",
            "Patience",
        ],
    },
    "Română": {
        "title": "NomNom Stories",
        "subtitle": "Povești de seară calde, care sprijină blând emoțiile și obiceiurile bune.",
        "login_badge": "Pentru părinți",
        "login_subtitle": "Construiește o bibliotecă liniștită de povești pentru somn, apropiere și creștere.",
        "login_btn": "Autentificare",
        "login_error": "Autentificarea a eșuat. Verifică emailul și parola.",
        "email_label": "Email",
        "password_label": "Parolă",
        "child_name": "Numele copilului",
        "child_placeholder": "De exemplu: Ana",
        "default_child_name": "Ana",
        "skills_label": "Ce dorim să susținem blând prin această poveste?",
        "skills_help": "Cel mai bine este să alegi 1-2 teme pentru o poveste coerentă și liniștitoare.",
        "duration": "Durată",
        "duration_btn_suffix": "min",
        "details": "Ce este important acum?",
        "details_placeholder": "De exemplu: copilului îi este teamă de întuneric, îi este dor de grădiniță sau învață să împartă jucăriile.",
        "details_help": "Poți menționa animale preferate, o provocare actuală, starea de seară sau finalul dorit.",
        "btn_create": "Creează povestea",
        "btn_create_hint": "Vom crea o poveste caldă, sigură și potrivită pentru seară.",
        "sidebar_library": "Poveștile mele",
        "sidebar_voice": "Vocea naratorului",
        "sidebar_new": "Poveste nouă",
        "sidebar_tagline": "Povești pentru liniște, apropiere și mici pași curajoși.",
        "voice_settings": "Narațiune",
        "ready_story": "Povestea este gata",
        "back_btn": "← Înapoi",
        "empty_story_text": "Textul poveștii este gol sau nu a fost salvat.",
        "no_saved_stories": "Încă nu există povești salvate",
        "section_for_whom": "Pentru cine este povestea",
        "section_language": "Limba poveștii",
        "section_skill": "Abilitate sau temă",
        "section_format": "Ce includem",
        "section_duration": "Durata lecturii",
        "section_details": "Detalii ale poveștii",
        "section_summary": "Ce vei primi",
        "spinner_magic": "Țesем povestea...",
        "spinner_voice": "Adăugăm vocea...",
        "spinner_cover": "Desenăm coperta...",
        "error_save_story": "Povestea nu a putut fi salvată.",
        "error_gen_story": "Textul poveștii nu a putut fi generat.",
        "story_fallback": "Poveste",
        "delete_help": "Șterge",
        "error_prefix": "Eroare",
        "account_label": "Cont",
        "section_parent_note": "Fiecare poveste modelează blând tema aleasă, fără frică, rușinare sau morală apăsătoare.",
        "summary_template": "O poveste de {time_val} minute pentru {child_name}: {skills}.",
        "summary_default_skills": "sprijin blând și liniște",
        "opt_img": "Adaugă ilustrație",
        "opt_audio": "Adaugă narațiune",
        "voice_hint": "Alege o voce dacă vrei și varianta audio a poveștii.",
        "view_hint": "O poți citi tu sau poți porni narațiunea când seara are nevoie de mai multă liniște.",
        "error_child_name": "Te rog să introduci numele copilului.",
        "error_skills": "Alege cel puțin o abilitate sau o temă.",
        "language_selector": "Limbă",
        "voices": {
            "Alina": "EXAVITQu4vr4xnSDxMaL",
            "Marcel": "8JVbfL6oEdmuxKn5DK2C",
        },
        "skills": [
            "Onestitate",
            "Curaj",
            "Bunătate",
            "Hărnicie",
            "Politețe",
            "Igienă",
            "Prietenie",
            "Răbdare",
        ],
    },
}


if "time_val" not in st.session_state:
    st.session_state.time_val = 5
if "view_story" not in st.session_state:
    st.session_state.view_story = None
if "sel_lang" not in st.session_state:
    st.session_state.sel_lang = "Русский"
if "page_mode" not in st.session_state:
    st.session_state.page_mode = "form"


lang_options = list(lang_dict.keys())


if not st.session_state.get("logged_in", False):
    stop_bg_music()

    current_lang = st.session_state.get("sel_lang", "Русский")
    copy_pack = lang_dict.get(current_lang, lang_dict["Русский"])

    _, center, _ = st.columns([1, 2, 1])
    with center:
        selected_lang = st.selectbox(
            copy_pack.get("language_selector", "Language"),
            lang_options,
            index=lang_options.index(current_lang),
            key="login_lang_selector",
            label_visibility="collapsed",
        )
        if selected_lang != current_lang:
            st.session_state.sel_lang = selected_lang
            st.rerun()

        st.markdown(
            f"""
            <div class="hero-badge">{copy_pack.get("login_badge", "")}</div>
            <div class="hero-title">🌙 NomNom Stories</div>
            <div class="hero-subtitle">{copy_pack.get("login_subtitle", "")}</div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("login_form"):
            email = st.text_input(copy_pack.get("email_label", "Email"))
            password = st.text_input(copy_pack.get("password_label", "Password"), type="password")

            if st.form_submit_button(
                copy_pack.get("login_btn", "Log in"),
                type="primary",
                use_container_width=True,
            ):
                if check_user(email, password):
                    st.session_state.logged_in = True
                    st.session_state.user_email = email.strip()
                    st.session_state.page_mode = "form"
                    st.rerun()
                else:
                    st.error(copy_pack.get("login_error", "Login failed"))

else:
    copy_pack = lang_dict.get(st.session_state.sel_lang, lang_dict["Русский"])
    stories = get_user_stories(st.session_state.user_email)

    with st.sidebar:
        try:
            st.image("logo.jpg", width=88)
        except Exception:
            pass

        st.markdown(
            f"""
            <div class="sidebar-brand">🌙 {copy_pack.get("title", "NomNom Stories")}</div>
            <div class="sidebar-subbrand">{copy_pack.get("sidebar_tagline", "")}</div>
            """,
            unsafe_allow_html=True,
        )

        st.success(f'{copy_pack.get("account_label", "Account")}: {st.session_state.user_email}')

        with st.expander(copy_pack.get("sidebar_library", "Stories"), expanded=False):
            render_story_library(stories, copy_pack, prefix="side")

        st.divider()

        st.markdown(
            f'<div class="section-label">{copy_pack.get("voice_settings", "Voice settings")}</div>',
            unsafe_allow_html=True,
        )
        st.caption(copy_pack.get("voice_hint", ""))

        voice_name = st.selectbox(
            copy_pack.get("sidebar_voice", "Voice"),
            list(copy_pack.get("voices", {}).keys()),
            key="voice_select",
        )
        voice_id = copy_pack.get("voices", {}).get(voice_name)

        if st.button(
            copy_pack.get("sidebar_new", "New story"),
            use_container_width=True,
            type="primary",
            key="sidebar_new_story_btn",
        ):
            st.session_state.view_story = None
            st.session_state.page_mode = "form"
            st.rerun()

    if st.session_state.page_mode == "view" and st.session_state.view_story:
        story = st.session_state.view_story
        mount_bg_music()

        top_left, top_right = st.columns([1, 6])

        with top_left:
            if st.button(
                copy_pack.get("back_btn", "← Back"),
                use_container_width=True,
                key="back_story_btn",
            ):
                st.session_state.view_story = None
                st.session_state.page_mode = "form"
                st.rerun()

        with top_right:
            st.markdown(
                f"""
                <div class="hero-badge">{copy_pack.get("ready_story", "Story ready")}</div>
                <div class="hero-title story-title">{html.escape(story.get("title", copy_pack.get("story_fallback", "Story")))}</div>
                <div class="hero-subtitle">{copy_pack.get("view_hint", "")}</div>
                """,
                unsafe_allow_html=True,
            )

        if story.get("audio_base64"):
            try:
                st.audio(base64.b64decode(story["audio_base64"]))
            except Exception:
                pass

        if story.get("image_url"):
            st.image(story["image_url"], use_container_width=True)

        story_text = (story.get("story_text") or "").strip()
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
                unsafe_allow_html=True,
            )
        else:
            st.warning(copy_pack.get("empty_story_text", "Story text is empty."))

    else:
        stop_bg_music()

        _, center, _ = st.columns([1, 2, 1])

        with center:
            st.markdown(
                f"""
                <div class="hero-badge">{copy_pack.get("title", "NomNom Stories")}</div>
                <div class="hero-title">🌙 NomNom Stories</div>
                <div class="hero-subtitle">{copy_pack.get("subtitle", "")}</div>
                """,
                unsafe_allow_html=True,
            )
            st.caption(copy_pack.get("section_parent_note", ""))

            st.markdown(
                f'<div class="section-label">{copy_pack.get("section_for_whom", "For whom")}</div>',
                unsafe_allow_html=True,
            )
            child_name = st.text_input(
                copy_pack.get("child_name", "Child's name"),
                value=copy_pack.get("default_child_name", ""),
                placeholder=copy_pack.get("child_placeholder", ""),
            )

            st.markdown(
                f'<div class="section-label">{copy_pack.get("section_language", "Language")}</div>',
                unsafe_allow_html=True,
            )
            new_lang = st.selectbox(
                copy_pack.get("language_selector", "Language"),
                lang_options,
                index=lang_options.index(st.session_state.sel_lang),
                key="lang_selector_center",
                label_visibility="collapsed",
            )
            if new_lang != st.session_state.sel_lang:
                st.session_state.sel_lang = new_lang
                st.rerun()

            st.markdown(
                f'<div class="section-label">{copy_pack.get("section_skill", "Skill")}</div>',
                unsafe_allow_html=True,
            )
            skills = st.multiselect(
                copy_pack.get("skills_label", "Skills"),
                copy_pack.get("skills", []),
                default=[copy_pack.get("skills", [""])[0]] if copy_pack.get("skills") else [],
                label_visibility="collapsed",
            )
            st.caption(copy_pack.get("skills_help", ""))

            st.markdown(
                f'<div class="section-label">{copy_pack.get("section_format", "Format")}</div>',
                unsafe_allow_html=True,
            )
            format_left, format_right = st.columns(2)
            with format_left:
                use_img = st.checkbox(
                    copy_pack.get("opt_img", "Add illustration"),
                    value=True,
                    key="use_img_checkbox",
                )
            with format_right:
                use_audio = st.checkbox(
                    copy_pack.get("opt_audio", "Add narration"),
                    value=False,
                    key="use_audio_checkbox",
                )

            st.markdown(
                f'<div class="section-label">{copy_pack.get("section_duration", "Duration")}</div>',
                unsafe_allow_html=True,
            )
            duration_columns = st.columns(3)
            for index, minutes in enumerate([3, 5, 10]):
                if duration_columns[index].button(
                    f'{minutes} {copy_pack.get("duration_btn_suffix", "min")}',
                    key=f"t_{minutes}",
                    type="primary" if st.session_state.time_val == minutes else "secondary",
                    use_container_width=True,
                ):
                    st.session_state.time_val = minutes
                    st.rerun()

            st.markdown(
                f'<div class="section-label">{copy_pack.get("section_details", "Details")}</div>',
                unsafe_allow_html=True,
            )
            details = st.text_area(
                copy_pack.get("details", "Story details"),
                label_visibility="collapsed",
                placeholder=copy_pack.get("details_placeholder", ""),
            )
            st.caption(copy_pack.get("details_help", ""))

            selected_skills = ", ".join(skills) if skills else copy_pack.get("summary_default_skills", "")
            story_summary = copy_pack.get("summary_template", "{skills}").format(
                child_name=child_name.strip() or copy_pack.get("default_child_name", ""),
                time_val=st.session_state.time_val,
                skills=selected_skills,
            )
            st.markdown(
                f'<div class="soft-info-chip">{html.escape(story_summary)}</div>',
                unsafe_allow_html=True,
            )

            st.caption(copy_pack.get("btn_create_hint", ""))

            if st.button(
                copy_pack.get("btn_create", "Create story"),
                type="primary",
                use_container_width=True,
                key="create_story_btn",
            ):
                errors = validate_story_request(child_name, skills, copy_pack)
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    try:
                        with st.spinner(copy_pack.get("spinner_magic", "Creating...")):
                            full_text = generate_story_text(
                                child_name.strip(),
                                st.session_state.sel_lang,
                                skills,
                                details.strip(),
                                st.session_state.time_val,
                            )

                        if not full_text:
                            st.error(copy_pack.get("error_gen_story", "Failed to generate story."))
                        else:
                            title, story_body = extract_story_parts(
                                full_text,
                                copy_pack.get("story_fallback", "Story"),
                            )

                            image_url = None
                            if use_img:
                                with st.spinner(copy_pack.get("spinner_cover", "Generating image...")):
                                    image_url = generate_image(
                                        title=title,
                                        child_name=child_name.strip(),
                                        lang=st.session_state.sel_lang,
                                        skills=skills,
                                        details=details.strip(),
                                    )

                            result = save_story(
                                {
                                    "user_email": st.session_state.user_email,
                                    "child_name": child_name.strip(),
                                    "title": title,
                                    "story_text": story_body,
                                    "image_url": image_url,
                                }
                            )

                            if result and getattr(result, "data", None):
                                current_story = result.data[0]
                                story_id = current_story["id"]

                                current_story["title"] = title
                                current_story["story_text"] = story_body
                                current_story["image_url"] = image_url

                                if use_audio and voice_id:
                                    with st.spinner(copy_pack.get("spinner_voice", "Generating voice...")):
                                        audio_b64 = get_speech_b64(story_body, voice_id)
                                    if audio_b64:
                                        update_audio(story_id, audio_b64)
                                        current_story["audio_base64"] = audio_b64

                                st.session_state.view_story = current_story
                                st.session_state.page_mode = "view"
                                st.rerun()
                            else:
                                st.error(copy_pack.get("error_save_story", "Failed to save story."))

                    except Exception as error:
                        st.error(f'{copy_pack.get("error_prefix", "Error")}: {error}')
