import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        /* 1. ОБЩИЙ ФОН */
        .stApp {
            background: linear-gradient(rgba(10, 15, 30, 0.8), rgba(10, 15, 30, 0.8)), 
                        url("https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?q=80&w=2013&auto=format&fit=crop") !important;
            background-size: cover !important;
            background-attachment: fixed !important;
        }

        /* 2. ФОРМА ВХОДА (КОМПАКТНАЯ И ПО ЦЕНТРУ) */
        [data-testid="stForm"], .stForm {
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(15px) !important;
            border: 1px solid rgba(56, 189, 248, 0.5) !important;
            padding: 30px !important;
            border-radius: 20px !important;
            max-width: 450px !important; /* Возвращаем классную ширину */
            margin: 50px auto !important;
            display: block !important;
        }

        /* 3. КНОПКИ ВРЕМЕНИ (3, 5, 10 мин) - УБИРАЕМ БЕЛЫЙ ЦВЕТ */
        div[data-testid="stHorizontalBlock"] button {
            background-color: #1e293b !important;
            color: #ffffff !important;
            border: 2px solid #38bdf8 !important;
            opacity: 1 !important;
        }
        
        /* Выбранная кнопка времени */
        div[data-testid="stHorizontalBlock"] button[kind="primary"] {
            background: linear-gradient(135deg, #38bdf8 0%, #1e40af 100%) !important;
            border: none !important;
            box-shadow: 0px 0px 15px rgba(56, 189, 248, 0.5) !important;
        }

        /* 4. САЙДБАР И КОРЗИНКИ БЕЗ КВАДРАТОВ */
        [data-testid="stSidebar"] {
            background-color: #0f172a !important;
            border-right: 1px solid #38bdf8 !important;
        }

        /* КНОПКА-КОРЗИНКА (ЧИСТАЯ, БЕЗ РАМОК) */
        button[key*="del_"] {
            border: none !important;
            background: transparent !important;
            box-shadow: none !important;
            color: #ff4b4b !important;
            font-size: 1.2rem !important;
            padding: 0 !important;
            width: auto !important;
            min-width: 30px !important;
        }
        
        /* Убираем рамку при наведении на корзинку */
        button[key*="del_"]:hover, button[key*="del_"]:active, button[key*="del_"]:focus {
            background: transparent !important;
            border: none !important;
            color: #ff6b6b !important;
            box-shadow: none !important;
            outline: none !important;
        }

        /* 5. ТЕКСТ */
        p, label, h1, h2, h3, span { 
            color: #ffffff !important; 
            font-weight: 600 !important;
        }

        /* Поля ввода внутри формы */
        .stTextInput input, .stTextArea textarea {
            background-color: rgba(15, 23, 42, 0.9) !important;
            color: white !important;
            border: 1px solid #38bdf8 !important;
        }
        </style>
        """, unsafe_allow_html=True)
