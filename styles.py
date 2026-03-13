import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        /* --- 1. ОБЩИЙ ВИД И ФОН --- */
        .stApp {
            background: linear-gradient(rgba(10, 15, 30, 0.8), rgba(10, 15, 30, 0.8)), 
                        url("https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?q=80&w=2013&auto=format&fit=crop") !important;
            background-size: cover !important;
            background-attachment: fixed !important;
        }

        /* --- 2. САЙДБАР (ЛЕВАЯ КОЛОНКА) --- */
        [data-testid="stSidebar"] {
            background-color: #0f172a !important;
            border-right: 1px solid #38bdf8 !important;
        }

        /* Список сказок: выравнивание в одну строку */
        [data-testid="stHorizontalBlock"] {
            align-items: center !important;
            gap: 0px !important;
            margin-bottom: -10px !important; /* Уплотняем список */
        }

        /* Кнопка с названием сказки (убираем рамки) */
        [data-testid="stSidebar"] button[kind="secondary"] {
            background: transparent !important;
            border: 1px solid rgba(56, 189, 248, 0.2) !important;
            color: #ffffff !important;
            text-align: left !important;
            padding: 5px 10px !important;
        }

        /* --- 3. УДАЛЯЕМ КВАДРАТИКИ У КОРЗИНЫ (ТОТАЛЬНО) --- */
        button[key*="del_"] {
            border: none !important;
            background: transparent !important;
            background-color: transparent !important;
            box-shadow: none !important;
            outline: none !important;
            color: #ff4b4b !important;
            padding: 0px !important;
            width: 30px !important;
            height: 30px !important;
            margin-top: 5px !important;
        }
        
        /* Убираем рамки при наведении и нажатии */
        button[key*="del_"]:hover, button[key*="del_"]:active, button[key*="del_"]:focus {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            color: #ff6b6b !important;
        }

        /* --- 4. НИЖНЯЯ КНОПКА (ВЫЙТИ) - ФИКС БЕЛОГО ЦВЕТА --- */
        /* Находим последнюю кнопку в сайдбаре */
        [data-testid="stSidebar"] .stButton:last-child button {
            background: rgba(255, 75, 75, 0.1) !important;
            border: 1px solid #ff4b4b !important;
            color: #ff4b4b !important;
        }
        [data-testid="stSidebar"] .stButton:last-child button:hover {
            background: #ff4b4b !important;
            color: white !important;
        }

        /* --- 5. ЦЕНТРАЛЬНЫЙ БЛОК --- */
        .stForm, [data-testid="stForm"] {
            background: rgba(255, 255, 255, 0.05) !important;
            backdrop-filter: blur(15px) !important;
            border: 1px solid rgba(56, 189, 248, 0.3) !important;
            border-radius: 20px !important;
            max-width: 600px !important;
            margin: auto !important;
        }

        /* Кнопки времени 3, 5, 10 - чтобы не были белыми */
        div[data-testid="stHorizontalBlock"] button {
            background-color: #1e293b !important;
            color: white !important;
            border: 1px solid #38bdf8 !important;
        }
        </style>
        """, unsafe_allow_html=True)
