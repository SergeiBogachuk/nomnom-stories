import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        /* 1. УБИРАЕМ БЕЛУЮ ПОЛОСУ СВЕРХУ */
        header[data-testid="stHeader"] {
            background-color: rgba(0,0,0,0) !important;
            color: white !important;
        }

        /* КНОПКА ОТКРЫТИЯ ПАНЕЛИ (МАЯЧОК) */
        button[kind="headerNoPadding"] {
            background-color: #38bdf8 !important;
            border-radius: 5px !important;
            box-shadow: 0px 0px 15px #38bdf8 !important;
            display: block !important;
        }

        /* 2. ФОН ПРИЛОЖЕНИЯ */
        .stApp {
            background: linear-gradient(rgba(10, 15, 30, 0.85), rgba(10, 15, 30, 0.85)), 
                        url("https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?q=80&w=2013&auto=format&fit=crop") !important;
            background-size: cover !important;
            background-attachment: fixed !important;
        }

        /* 3. САЙДБАР */
        [data-testid="stSidebar"] {
            background-color: #0f172a !important;
            border-right: 1px solid #38bdf8 !important;
        }

        /* КОРЗИНКИ: ПОЛНОЕ УДАЛЕНИЕ КВАДРАТОВ */
        button[key*="del_"] {
            border: none !important;
            outline: none !important;
            background: transparent !important;
            background-color: transparent !important;
            box-shadow: none !important;
            color: #ff4b4b !important;
            padding: 0 !important;
            width: 30px !important;
            height: 30px !important;
        }
        button[key*="del_"]:hover, button[key*="del_"]:active {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }

        /* 4. КНОПКИ ВНИЗУ САЙДБАРА */
        /* Кнопка "Новая сказка" */
        [data-testid="stSidebar"] button[kind="primary"] {
            background: linear-gradient(135deg, #38bdf8 0%, #1e40af 100%) !important;
            border: none !important;
            margin-top: 20px !important;
        }

        /* Кнопка "Выход" (КРАСНАЯ) */
        [data-testid="stSidebar"] .stButton:last-child button {
            background-color: rgba(255, 75, 75, 0.2) !important;
            border: 2px solid #ff4b4b !important;
            color: #ff4b4b !important;
            font-weight: bold !important;
            margin-top: 10px !important;
        }
        [data-testid="stSidebar"] .stButton:last-child button:hover {
            background-color: #ff4b4b !important;
            color: white !important;
        }

        /* 5. КНОПКИ ВРЕМЕНИ (ФИКС БЕЛОГО) */
        div[data-testid="stHorizontalBlock"] button {
            background-color: #1e293b !important;
            color: white !important;
            border: 1px solid #38bdf8 !important;
        }
        </style>
        """, unsafe_allow_html=True)
