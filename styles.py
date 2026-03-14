import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        /* 1. ФОН И ОБЩИЙ ВИД */
        .stApp {
            background: linear-gradient(rgba(10, 15, 30, 0.85), rgba(10, 15, 30, 0.85)), 
                        url("https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?q=80&w=2013&auto=format&fit=crop") !important;
            background-size: cover !important;
            background-attachment: fixed !important;
        }

        /* 2. КОМПАКТНАЯ ФОРМА ПО ЦЕНТРУ */
        [data-testid="stMainViewContainer"] [data-testid="stVerticalBlock"] > div {
            max-width: 600px !important;
            margin: 0 auto !important;
        }

        /* 3. ЯРКИЙ БЕЛЫЙ ТЕКСТ */
        h1, h2, h3, label p, .stMarkdown p {
            color: #ffffff !important;
            opacity: 1 !important;
            font-weight: 600 !important;
        }

        /* 4. САЙДБАР (ЛЕВАЯ ПАНЕЛЬ) */
        [data-testid="stSidebar"] {
            background-color: #0f172a !important;
            border-right: 1px solid #38bdf8 !important;
        }
        
        [data-testid="stSidebar"] button {
            color: white !important;
            background-color: rgba(56, 189, 248, 0.1) !important;
            border: 1px solid rgba(56, 189, 248, 0.3) !important;
            text-align: left !important;
            margin-bottom: 5px !important;
        }

        /* 5. ПОЛЯ ВВОДА И ТЕКСТ ВНУТРИ */
        .stTextInput input, .stTextArea textarea, [data-baseweb="select"] * {
            background-color: rgba(255, 255, 255, 0.05) !important;
            color: white !important;
            border: 1px solid #38bdf8 !important;
        }

        /* Кнопки времени и создания */
        div[data-testid="stHorizontalBlock"] button {
            background-color: #1e293b !important;
            color: white !important;
            border: 1px solid #38bdf8 !important;
        }
        button[kind="primary"] {
            background: linear-gradient(135deg, #38bdf8, #1e40af) !important;
            border: none !important;
        }
        
        /* Кнопка выхода */
        [data-testid="stSidebar"] .stButton:last-child button {
            border: 1px solid #ff4b4b !important;
            color: #ff4b4b !important;
            background: transparent !important;
        }

        /* --- ФИКС ДЛЯ ВЫБОРА ЯЗЫКА (ЧТОБЫ ЗАКРЫВАЛОСЬ) --- */
        div[data-baseweb="popover"] {
            z-index: 999999 !important;
        }
        div[data-baseweb="select"] {
            cursor: pointer !important;
        }
        .stSelectbox div[role="button"] {
            pointer-events: all !important;
        }
        </style>
        """, unsafe_allow_html=True)
