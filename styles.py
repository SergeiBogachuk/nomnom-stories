import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        /* Основной фон приложения */
        .stApp { background: #0a0f1e; color: #f8fafc; }
        
        /* Боковая панель (Сайдбар) */
        [data-testid="stSidebar"] { 
            background-color: #111827 !important; 
            border-right: 2px solid #38bdf8; 
        }
        
        /* --- ГЛАВНОЕ: КНОПКА ОТКРЫТИЯ ПАНЕЛИ (ГАМБУРГЕР) --- */
        button[data-testid="baseButton-headerNoPadding"] {
            background-color: #38bdf8 !important;
            border-radius: 8px !important;
            box-shadow: 0px 0px 15px rgba(56, 189, 248, 0.8) !important;
            margin-left: 10px !important;
            margin-top: 5px !important;
        }
        button[data-testid="baseButton-headerNoPadding"] svg {
            fill: #0a0f1e !important;
            width: 30px !important;
            height: 30px !important;
        }

        /* Убираем мутность текста */
        p, label, span, .stMarkdown { 
            color: #ffffff !important; 
            opacity: 1 !important; 
            font-weight: 600 !important;
        }

        /* Кнопки Длительности (3, 5, 10 мин) */
        div[data-testid="stHorizontalBlock"] div.stButton > button {
            height: 60px !important;
            width: 100% !important;
            border-radius: 12px !important;
            border: 2px solid #38bdf8 !important;
            background-color: #1e293b !important;
        }

        /* Активная кнопка времени и кнопка "Создать магию" */
        div.stButton > button[kind="primary"], 
        button[kind="primaryFormSubmit"] {
            background: linear-gradient(135deg, #38bdf8 0%, #1e40af 100%) !important;
            border: none !important;
            color: white !important;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.3) !important;
        }

        /* Кнопка "Новая сказка" в сайдбаре */
        section[data-testid="stSidebar"] .stButton > button {
            color: #ffffff !important;
            background-color: #1e293b !important;
            border: 1px solid #38bdf8 !important;
            opacity: 1 !important;
        }

        /* Поле вывода сказки */
        .story-output { 
            background: #ffffff; 
            color: #1e293b !important; 
            padding: 40px; 
            border-radius: 30px; 
            font-size: 1.25em; 
            line-height: 1.8; 
            white-space: pre-wrap; 
        }
        
        /* Чекбоксы выбора режима */
        .stCheckbox { 
            background: #1e293b; 
            padding: 15px; 
            border-radius: 10px; 
            border: 1px solid #38bdf8; 
            margin-bottom: 10px; 
        }
        </style>
        """, unsafe_allow_html=True)
