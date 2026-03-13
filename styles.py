import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        /* 1. ТЕМНЫЙ МАГИЧЕСКИЙ ФОН */
        .stApp {
            background: linear-gradient(rgba(10, 15, 30, 0.85), rgba(10, 15, 30, 0.85)), 
                        url("https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?q=80&w=2013&auto=format&fit=crop") !important;
            background-size: cover !important;
        }

        /* 2. КОМПАКТНАЯ ФОРМА ПО ЦЕНТРУ */
        [data-testid="stMainViewContainer"] [data-testid="stVerticalBlock"] > div {
            max-width: 600px !important;
            margin: 0 auto !important;
        }

        /* 3. БЕЛЫЙ ТЕКСТ НАД ПОЛЯМИ (Чтобы было видно "Имя", "Тема" и т.д.) */
        label p, .stMarkdown p {
            color: #ffffff !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            opacity: 1 !important;
        }

        /* 4. САЙДБАР (ЛЕВАЯ ПАНЕЛЬ) */
        [data-testid="stSidebar"] {
            background-color: #050a18 !important;
            border-right: 1px solid #38bdf8 !important;
        }
        
        /* Убираем квадраты у кнопок в сайдбаре */
        [data-testid="stSidebar"] button {
            border: none !important;
            background: transparent !important;
            color: white !important;
            text-align: left !important;
        }
        
        /* Кнопка ВЫХОД (Спокойный красный контур) */
        [data-testid="stSidebar"] .stButton:last-child button {
            border: 1px solid #ff4b4b !important;
            color: #ff4b4b !important;
        }

        /* 5. ПОЛЯ ВВОДА (ТЕМНЫЕ ВНУТРИ, БЕЛЫЙ ТЕКСТ) */
        .stTextInput input, .stTextArea textarea, .stMultiSelect {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid #38bdf8 !important;
            color: #ffffff !important;
        }
        
        /* Кнопки времени и создания (БЕЗ НЕОНА) */
        div[data-testid="stHorizontalBlock"] button {
            background-color: #1e293b !important;
            color: white !important;
            border: 1px solid #38bdf8 !important;
        }
        button[kind="primary"] {
            background: linear-gradient(135deg, #38bdf8, #1e40af) !important;
            border: none !important;
            box-shadow: none !important;
        }
        </style>
        """, unsafe_allow_html=True)
