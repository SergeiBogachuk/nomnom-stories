import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        /* ===== Общий фон ===== */
        .stApp {
            background:
                radial-gradient(circle at top, rgba(56, 189, 248, 0.16), transparent 30%),
                radial-gradient(circle at 20% 20%, rgba(99, 102, 241, 0.12), transparent 25%),
                linear-gradient(rgba(5, 10, 24, 0.72), rgba(5, 10, 24, 0.84)),
                url("https://images.unsplash.com/photo-1534796636912-3b95b3ab5986?q=80&w=2000&auto=format&fit=crop") !important;
            background-size: cover !important;
            background-attachment: fixed !important;
            color: #f8fbff !important;
        }

        /* ===== Основной контейнер ===== */
        [data-testid="block-container"] {
            max-width: 760px !important;
            margin-top: 24px !important;
            margin-bottom: 40px !important;
            padding: 2.2rem 2rem 2rem 2rem !important;
            background: linear-gradient(180deg, rgba(10, 18, 40, 0.82), rgba(8, 15, 34, 0.72)) !important;
            border: 1px solid rgba(125, 211, 252, 0.20) !important;
            border-radius: 28px !important;
            box-shadow:
                0 20px 60px rgba(2, 8, 23, 0.45),
                inset 0 1px 0 rgba(255, 255, 255, 0.06) !important;
            backdrop-filter: blur(14px) !important;
        }

        /* ===== Сайдбар ===== */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(6, 13, 31, 0.98), rgba(10, 20, 45, 0.96)) !important;
            border-right: 1px solid rgba(56, 189, 248, 0.22) !important;
            box-shadow: inset -1px 0 0 rgba(255,255,255,0.04) !important;
        }

        [data-testid="stSidebar"] .stAlert {
            border-radius: 18px !important;
            border: 1px solid rgba(125, 211, 252, 0.20) !important;
            background: rgba(34, 197, 94, 0.14) !important;
        }

        [data-testid="stSidebar"] .stButton > button {
            height: 46px !important;
        }

        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stCheckbox label {
            font-weight: 700 !important;
        }

        /* ===== Заголовки ===== */
        h1 {
            text-align: center !important;
            font-size: 3rem !important;
            line-height: 1.1 !important;
            margin-bottom: 0.35rem !important;
            color: #ffffff !important;
            font-weight: 800 !important;
            letter-spacing: -0.03em !important;
        }

        h2, h3 {
            color: #f8fbff !important;
            font-weight: 700 !important;
        }

        .hero-title {
            text-align: center;
            font-size: 3rem;
            font-weight: 800;
            line-height: 1.05;
            margin-bottom: 0.35rem;
            color: #ffffff;
            text-shadow: 0 0 24px rgba(125, 211, 252, 0.18);
        }

        .hero-subtitle {
            text-align: center;
            font-size: 1rem;
            color: #dbeafe;
            opacity: 0.92;
            margin-bottom: 1.6rem;
        }

        .hero-badge {
            width: fit-content;
            margin: 0 auto 12px auto;
            padding: 8px 14px;
            border-radius: 999px;
            background: rgba(56, 189, 248, 0.12);
            border: 1px solid rgba(125, 211, 252, 0.24);
            color: #dff4ff;
            font-size: 0.92rem;
            font-weight: 700;
            letter-spacing: 0.01em;
            box-shadow: 0 8px 24px rgba(2, 8, 23, 0.12);
        }

        .sidebar-brand {
            font-size: 1.25rem;
            font-weight: 800;
            color: #ffffff;
            margin-top: 6px;
            margin-bottom: 2px;
        }

        .sidebar-subbrand {
            font-size: 0.92rem;
            color: #cfe8ff;
            opacity: 0.85;
            margin-bottom: 18px;
        }

        .section-label {
            margin-top: 8px;
            margin-bottom: 8px;
            font-size: 0.98rem;
            font-weight: 700;
            color: #e9f6ff !important;
            letter-spacing: 0.01em;
        }

        .soft-info-chip {
            width: fit-content;
            margin: 8px auto 16px auto;
            padding: 10px 14px;
            border-radius: 16px;
            background: rgba(59, 130, 246, 0.16);
            border: 1px solid rgba(125, 211, 252, 0.24);
            color: #eaf6ff;
            font-weight: 600;
            box-shadow: 0 10px 24px rgba(2, 8, 23, 0.14);
        }

        .story-shell {
            margin-top: 18px;
        }

        /* ===== Обычный текст ===== */
        p, label, span {
            color: #eef6ff !important;
        }

        .stMarkdown p {
            color: #eef6ff !important;
        }

        /* ===== Поля ввода ===== */
        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div,
        .stTextArea textarea {
            background: rgba(15, 23, 42, 0.82) !important;
            border: 1px solid rgba(125, 211, 252, 0.20) !important;
            border-radius: 18px !important;
            color: #ffffff !important;
            box-shadow:
                inset 0 1px 0 rgba(255,255,255,0.04),
                0 8px 28px rgba(2, 8, 23, 0.18) !important;
        }

        .stTextInput input,
        .stTextArea textarea {
            color: #ffffff !important;
        }

        .stTextArea textarea {
            min-height: 130px !important;
        }

        /* ===== Multiselect ===== */
        div[data-baseweb="tag"] {
            background: linear-gradient(135deg, rgba(251, 113, 133, 0.95), rgba(239, 68, 68, 0.95)) !important;
            border-radius: 999px !important;
            border: none !important;
            color: white !important;
            padding-left: 8px !important;
            padding-right: 8px !important;
            font-weight: 700 !important;
        }

        div[data-baseweb="tag"] span {
            color: white !important;
        }

        /* ===== Чекбоксы ===== */
        .stCheckbox {
            background: rgba(15, 23, 42, 0.68) !important;
            padding: 14px 16px !important;
            border-radius: 18px !important;
            border: 1px solid rgba(125, 211, 252, 0.24) !important;
            box-shadow: 0 8px 24px rgba(2, 8, 23, 0.18) !important;
        }

        .stCheckbox:hover {
            border-color: rgba(125, 211, 252, 0.40) !important;
            transform: translateY(-1px);
            transition: 0.2s ease;
        }

        /* ===== Кнопки ===== */
        div.stButton > button {
            border-radius: 18px !important;
            height: 50px !important;
            font-weight: 700 !important;
            border: 1px solid rgba(125, 211, 252, 0.22) !important;
            transition: all 0.2s ease !important;
        }

        div.stButton > button[kind="primary"],
        button[kind="primaryFormSubmit"] {
            background: linear-gradient(135deg, #38bdf8 0%, #2563eb 100%) !important;
            border: none !important;
            color: white !important;
            box-shadow: 0 14px 32px rgba(37, 99, 235, 0.30) !important;
        }

        div.stButton > button[kind="primary"]:hover,
        button[kind="primaryFormSubmit"]:hover {
            transform: translateY(-2px) scale(1.01) !important;
            box-shadow: 0 18px 36px rgba(37, 99, 235, 0.38) !important;
        }

        div.stButton > button[kind="secondary"] {
            background: rgba(15, 23, 42, 0.72) !important;
            color: #eff6ff !important;
        }

        div.stButton > button[kind="secondary"]:hover {
            border-color: rgba(125, 211, 252, 0.45) !important;
            background: rgba(30, 41, 59, 0.88) !important;
        }

        /* ===== Info / success / alerts ===== */
        .stInfo, .stSuccess, .stWarning, .stError {
            border-radius: 18px !important;
            border: 1px solid rgba(125, 211, 252, 0.18) !important;
        }

        .stInfo {
            background: rgba(59, 130, 246, 0.15) !important;
        }

        /* ===== Expander ===== */
        [data-testid="stExpander"] {
            border: 1px solid rgba(125, 211, 252, 0.16) !important;
            border-radius: 18px !important;
            background: rgba(15, 23, 42, 0.35) !important;
        }

        /* ===== Разделители ===== */
        hr {
            border-color: rgba(125, 211, 252, 0.16) !important;
        }

        /* ===== Карточка сказки ===== */
        .story-output {
            background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%) !important;
            color: #1e293b !important;
            padding: 30px !important;
            border-radius: 24px !important;
            font-size: 1.1rem !important;
            line-height: 1.9 !important;
            max-width: 900px !important;
            margin: 20px auto 0 auto !important;
            white-space: pre-wrap !important;
            box-shadow: 0 18px 40px rgba(15, 23, 42, 0.18) !important;
        }

        .story-output,
        .story-output p,
        .story-output span,
        .story-output div,
        .story-output strong,
        .story-output em,
        .story-output li,
        .story-output h1,
        .story-output h2,
        .story-output h3,
        .story-output h4,
        .story-output h5,
        .story-output h6 {
            color: #1e293b !important;
            font-weight: 400 !important;
        }

        /* ===== Картинка сказки ===== */
        [data-testid="stImage"] img {
            border-radius: 24px !important;
            box-shadow: 0 18px 40px rgba(2, 8, 23, 0.26) !important;
        }

        /* ===== Аудио ===== */
        audio {
            width: 100% !important;
            margin-top: 12px !important;
            margin-bottom: 16px !important;
            border-radius: 16px !important;
        }

        /* ===== Мобильная версия ===== */
        @media (max-width: 768px) {
            [data-testid="block-container"] {
                padding: 1.25rem 1rem 1.25rem 1rem !important;
                border-radius: 22px !important;
                margin-top: 10px !important;
            }

            .hero-title, h1 {
                font-size: 2.15rem !important;
            }

            .hero-subtitle {
                font-size: 0.95rem !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)
