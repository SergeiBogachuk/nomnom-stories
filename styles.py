import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        /* 1. ФОН ПРИЛОЖЕНИЯ */
        .stApp {
            background: linear-gradient(rgba(10, 15, 30, 0.85), rgba(10, 15, 30, 0.85)), 
                        url("https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?q=80&w=2013&auto=format&fit=crop") !important;
            background-size: cover !important;
            background-attachment: fixed !important;
        }

        /* 2. САЙДБАР (ЛЕВАЯ КОЛОНКА) */
        [data-testid="stSidebar"] {
            background-color: #0f172a !important;
            border-right: 1px solid #38bdf8 !important;
        }

        /* Кнопки сказок (убираем красные рамки) */
        [data-testid="stSidebar"] button {
            border: 1px solid rgba(56, 189, 248, 0.3) !important;
            background: rgba(30, 41, 59, 0.5) !important;
            color: #ffffff !important;
            border-radius: 8px !important;
        }

        /* 3. КОРЗИНКА (НИКАКИХ РАМОК И КВАДРАТОВ) */
        button[key*="del_"] {
            border: none !important;
            background: transparent !important;
            background-color: transparent !important;
            box-shadow: none !important;
            color: rgba(255, 255, 255, 0.3) !important; /* Делаем её тусклой, пока не наведешь */
            margin-top: 5px !important;
        }
        
        button[key*="del_"]:hover {
            color: #ff4b4b !important; /* Краснеет только при наведении */
            background: transparent !important;
            border: none !important;
        }

        /* 4. ЦЕНТРАЛЬНАЯ КАРТОЧКА */
        .stForm, [data-testid="stForm"] {
            background: rgba(255, 255, 255, 0.03) !important;
            backdrop-filter: blur(15px) !important;
            border: 1px solid rgba(56, 189, 248, 0.2) !important;
            border-radius: 20px !important;
        }

        /* Кнопки времени (3, 5, 10 мин) */
        div[data-testid="stHorizontalBlock"] button {
            background-color: #1e293b !important;
            color: white !important;
            border: 1px solid #38bdf8 !important;
        }
        
        div[data-testid="stHorizontalBlock"] button[kind="primary"] {
            background: linear-gradient(135deg, #38bdf8 0%, #1e40af 100%) !important;
            border: none !important;
        }

        /* 5. ИСПРАВЛЕНИЕ КНОПКИ ВЫХОДА */
        [data-testid="stSidebar"] .stButton:last-child button {
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            background: transparent !important;
            color: #ffffff !important;
        }

        /* Текст */
        p, label, h1, span { color: #ffffff !important; font-weight: 500 !important; }
        </style>
        """, unsafe_allow_html=True)
