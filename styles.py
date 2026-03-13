import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        /* МАГИЧЕСКИЙ ФОН */
        .stApp {
            background: linear-gradient(rgba(10, 15, 30, 0.8), rgba(10, 15, 30, 0.8)), 
                        url("https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?q=80&w=2013&auto=format&fit=crop") !important;
            background-size: cover !important;
            background-attachment: fixed !important;
        }

        /* САЙДБАР (ЧЕРНЫЙ С СИНЕЙ РАМКОЙ) */
        [data-testid="stSidebar"], section[data-testid="stSidebar"] {
            background-color: #0f172a !important;
            border-right: 1px solid #38bdf8 !important;
        }
        
        /* Текст в сайдбаре */
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
            color: #ffffff !important;
        }

        /* КНОПКИ ВРЕМЕНИ (ИСПРАВЛЕНИЕ БЕЛОГО ЦВЕТА) */
        div[data-testid="stHorizontalBlock"] button {
            background-color: #1e293b !important;
            color: #ffffff !important;
            border: 2px solid #38bdf8 !important;
            height: 55px !important;
            opacity: 1 !important;
        }
        
        /* Подсветка активной кнопки времени */
        div[data-testid="stHorizontalBlock"] button[kind="primary"] {
            background: linear-gradient(135deg, #38bdf8 0%, #1e40af 100%) !important;
            box-shadow: 0px 0px 15px rgba(56, 189, 248, 0.5) !important;
            border: none !important;
        }

        /* КОРЗИНКИ УДАЛЕНИЯ */
        button[key*="del_"] {
            border: none !important;
            background: transparent !important;
            font-size: 20px !important;
        }

        /* ЦЕНТРАЛЬНАЯ КАРТОЧКА */
        .stForm, [data-testid="stForm"] {
            background: rgba(255, 255, 255, 0.05) !important;
            backdrop-filter: blur(15px) !important;
            border: 1px solid rgba(56, 189, 248, 0.3) !important;
            padding: 30px !important;
            border-radius: 20px !important;
        }

        /* Поля ввода и текст */
        .stTextInput input, .stTextArea textarea {
            background-color: rgba(15, 23, 42, 0.8) !important;
            color: white !important;
            border: 1px solid #38bdf8 !important;
        }

        p, label, h1, h2, h3 { 
            color: #ffffff !important; 
            font-weight: 600 !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }
        </style>
        """, unsafe_allow_html=True)
