import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        /* 1. ФОН И ОБЩИЙ ВИД */
        .stApp {
            background: linear-gradient(rgba(10, 15, 30, 0.9), rgba(10, 15, 30, 0.9)), 
                        url("https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?q=80&w=2013&auto=format&fit=crop") !important;
            background-size: cover !important;
        }

        /* 2. ЦЕНТРИРОВАНИЕ ВСЕГО КОНТЕНТА */
        /* Ограничиваем ширину центрального блока, чтобы не было длинных полос */
        [data-testid="stVerticalBlock"] > div {
            max-width: 700px !important;
            margin: 0 auto !important;
        }

        /* 3. САЙДБАР (ЛЕВАЯ КОЛОНКА) */
        [data-testid="stSidebar"] {
            background-color: #0f172a !important;
            border-right: 2px solid #38bdf8 !important;
        }

        /* Кнопки сказок в сайдбаре (ЧИСТЫЕ) */
        [data-testid="stSidebar"] button {
            background-color: rgba(56, 189, 248, 0.05) !important;
            border: 1px solid rgba(56, 189, 248, 0.2) !important;
            color: white !important;
            text-align: left !important;
            margin-bottom: 5px !important;
        }

        /* 4. КНОПКИ ВРЕМЕНИ И СОЗДАНИЯ (БЕЗ КРАСНОГО) */
        div[data-testid="stHorizontalBlock"] button {
            background-color: #1e293b !important;
            color: white !important;
            border: 1px solid #38bdf8 !important;
        }
        
        button[kind="primary"], button[kind="primaryFormSubmit"] {
            background: linear-gradient(135deg, #38bdf8 0%, #1e40af 100%) !important;
            border: none !important;
            box-shadow: 0px 4px 15px rgba(56, 189, 248, 0.4) !important;
        }

        /* Кнопка выхода (Мягкий красный, без жести) */
        [data-testid="stSidebar"] .stButton:last-child button {
            border: 1px solid #ff4b4b !important;
            background: rgba(255, 75, 75, 0.1) !important;
            color: #ff4b4b !important;
        }

        /* 5. ПОЛЯ ВВОДА */
        .stTextInput input, .stTextArea textarea {
            background-color: rgba(15, 23, 42, 0.8) !important;
            color: white !important;
            border: 1px solid #38bdf8 !important;
            border-radius: 10px !important;
        }

        /* Убираем белую шапку сверху */
        header[data-testid="stHeader"] { background: transparent !important; }
        </style>
        """, unsafe_allow_html=True)
