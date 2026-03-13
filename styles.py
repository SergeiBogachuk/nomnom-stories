import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        /* 1. ФОН */
        .stApp {
            background: linear-gradient(rgba(10, 15, 30, 0.9), rgba(10, 15, 30, 0.9)), 
                        url("https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?q=80&w=2013&auto=format&fit=crop") !important;
            background-size: cover !important;
        }

        /* 2. ЦЕНТРИРОВАНИЕ И ШИРИНА */
        [data-testid="stMainViewContainer"] [data-testid="stVerticalBlock"] > div {
            max-width: 650px !important;
            margin: 0 auto !important;
        }

        /* 3. САЙДБАР (ЛЕВАЯ ПАНЕЛЬ) */
        [data-testid="stSidebar"] {
            background-color: #050a18 !important;
        }
        
        /* Кнопки в сайдбаре: реакция на курсор */
        [data-testid="stSidebar"] button {
            background-color: rgba(56, 189, 248, 0.1) !important;
            border: 1px solid rgba(56, 189, 248, 0.3) !important;
            color: white !important;
            transition: 0.2s !important;
        }
        [data-testid="stSidebar"] button:hover {
            border-color: #38bdf8 !important;
            background-color: rgba(56, 189, 248, 0.2) !important;
        }

        /* Кнопка-корзинка (🗑️) без лишних рамок */
        button[key*="d_"] {
            border: none !important;
            background: transparent !important;
            color: #ff4b4b !important;
            box-shadow: none !important;
        }

        /* 4. ТЕКСТ В ПОЛЯХ (ТЕМНЫЙ НА БЕЛОМ) */
        input, textarea, [data-baseweb="select"] span {
            color: #1e293b !important;
        }
        
        /* Заголовки полей (БЕЛЫЕ) */
        label p {
            color: #ffffff !important;
            font-weight: bold !important;
        }

        /* 5. КНОПКИ ВРЕМЕНИ И МАГИИ */
        div[data-testid="stHorizontalBlock"] button {
            background-color: #1e293b !important;
            color: white !important;
            border: 1px solid #38bdf8 !important;
        }
        button[kind="primary"] {
            background: linear-gradient(135deg, #38bdf8, #1e40af) !important;
            border: none !important;
        }
        </style>
        """, unsafe_allow_html=True)
