import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        /* МАГИЧЕСКИЙ ФОН */
        .stApp {
            background: linear-gradient(rgba(10, 15, 30, 0.7), rgba(10, 15, 30, 0.7)), 
                        url("https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?q=80&w=2013&auto=format&fit=crop") !important;
            background-size: cover !important;
            background-attachment: fixed !important;
        }

        /* ЦЕНТРАЛЬНАЯ КАРТОЧКА (ИСПРАВЛЕНА ШИРИНА) */
        [data-testid="stVerticalBlock"] > div:has(div.stTextInput), .stForm {
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(15px) !important;
            border: 1px solid rgba(56, 189, 248, 0.4) !important;
            padding: 30px !important;
            border-radius: 20px !important;
            width: 100% !important;
            max-width: 450px !important; /* Удобная ширина для логина */
            margin: auto !important;
        }

        /* Поля ввода (Email и Пароль) */
        .stTextInput input {
            background-color: rgba(30, 41, 59, 0.8) !important;
            color: white !important;
            height: 45px !important;
            border: 1px solid #38bdf8 !important;
        }

        /* Кнопка "Войти" */
        button[kind="primaryFormSubmit"] {
            background: linear-gradient(135deg, #38bdf8 0%, #1e40af 100%) !important;
            border: none !important;
            height: 50px !important;
            font-weight: bold !important;
        }

        /* Боковая панель */
        [data-testid="stSidebar"] { 
            background-color: #0f172a !important; 
            border-right: 1px solid #38bdf8 !important; 
        }

        /* Текст сказки */
        .story-output {
            background: #ffffff !important;
            color: #1e293b !important;
            padding: 30px !important;
            border-radius: 20px !important;
            font-size: 1.2rem !important;
            line-height: 1.6 !important;
        }
        </style>
        """, unsafe_allow_html=True)
