import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        /* 1. КОНТРАСТНЫЙ ФОН */
        .stApp {
            background: linear-gradient(rgba(10, 20, 40, 0.85), rgba(10, 20, 40, 0.85)), 
                        url("https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?q=80&w=2013&auto=format&fit=crop") !important;
            background-size: cover !important;
        }

        /* 2. ТЕКСТ - ДЕЛАЕМ ЯРКО-БЕЛЫМ */
        h1, h2, h3, p, label, span, .stMarkdown p {
            color: #FFFFFF !important;
            opacity: 1 !important;
            font-weight: 700 !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        }

        /* 3. САЙДБАР (ЛЕВАЯ ПАНЕЛЬ) */
        [data-testid="stSidebar"] {
            background-color: #050a18 !important;
            border-right: 2px solid #38bdf8 !important;
        }

        /* Кнопки сказок (с эффектом наведения) */
        [data-testid="stSidebar"] button {
            background-color: rgba(56, 189, 248, 0.1) !important;
            border: 1px solid #38bdf8 !important;
            color: #38bdf8 !important;
            transition: all 0.3s ease !important;
        }
        [data-testid="stSidebar"] button:hover {
            background-color: #38bdf8 !important;
            color: #050a18 !important;
            box-shadow: 0px 0px 15px #38bdf8 !important;
            transform: scale(1.02);
        }

        /* 4. КНОПКИ ВНИЗУ (НОВАЯ / ВЫХОД) */
        /* Новая сказка - золотисто-синяя */
        [data-testid="stSidebar"] .stButton:nth-last-child(2) button {
            background: linear-gradient(135deg, #38bdf8, #1e40af) !important;
            color: white !important;
            border: none !important;
        }
        
        /* Выход - четкий красный контур */
        [data-testid="stSidebar"] .stButton:last-child button {
            background: transparent !important;
            border: 2px solid #ff4b4b !important;
            color: #ff4b4b !important;
        }
        [data-testid="stSidebar"] .stButton:last-child button:hover {
            background: #ff4b4b !important;
            color: white !important;
        }

        /* 5. ЦЕНТРАЛЬНЫЙ БЛОК */
        div[data-testid="stVerticalBlock"] > div {
            max-width: 750px !important;
            margin: 0 auto !important;
        }

        /* Поля ввода (делаем их заметными) */
        .stTextInput input, .stTextArea textarea, .stMultiSelect {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: 2px solid #38bdf8 !important;
            color: white !important;
            border-radius: 10px !important;
        }
        
        /* Фикс кнопок времени */
        div[data-testid="stHorizontalBlock"] button {
            background-color: #1e293b !important;
            color: white !important;
            border: 2px solid #38bdf8 !important;
        }
        </style>
        """, unsafe_allow_html=True)
