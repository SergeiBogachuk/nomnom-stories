import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(rgba(10, 20, 40, 0.85), rgba(10, 20, 40, 0.85)), 
                        url("https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?q=80&w=2013&auto=format&fit=crop") !important;
            background-size: cover !important;
        }

        /* ТЕКСТ ВНУТРИ ПОЛЕЙ ВВОДА - ДЕЛАЕМ ТЕМНЫМ ДЛЯ ВИДИМОСТИ */
        input, textarea, [data-baseweb="select"] * {
            color: #1e293b !important;
            font-weight: 500 !important;
        }

        /* Заголовки полей (Имя ребенка, Тема и т.д.) */
        label p {
            color: #ffffff !important;
            font-size: 1.1rem !important;
            text-shadow: 1px 1px 2px #000;
        }

        /* САЙДБАР И ЭКСПАНДЕР (СВОРАЧИВАНИЕ) */
        [data-testid="stSidebar"] { background-color: #050a18 !important; }
        
        /* Стиль выпадающего списка */
        details {
            border: 1px solid #38bdf8 !important;
            border-radius: 10px !important;
            padding: 10px !important;
            background: rgba(56, 189, 248, 0.05) !important;
        }
        summary {
            color: #38bdf8 !important;
            font-weight: bold !important;
            cursor: pointer !important;
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

        /* Кнопка удаления (🗑️) */
        .del-btn {
            color: #ff4b4b !important;
            background: transparent !important;
            border: none !important;
            font-size: 0.9rem !important;
            text-align: right !important;
        }
        </style>
        """, unsafe_allow_html=True)
