import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        /* 1. ФОН */
        .stApp {
            background: linear-gradient(rgba(10, 20, 40, 0.85), rgba(10, 20, 40, 0.85)), 
                        url("https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?q=80&w=2013&auto=format&fit=crop") !important;
            background-size: cover !important;
        }

        /* 2. СЖИМАЕМ ДЛИННЫЕ ЛИНИИ (Центрируем контент) */
        [data-testid="stMainViewContainer"] [data-testid="stVerticalBlock"] > div {
            max-width: 650px !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }

        /* 3. ИСПРАВЛЯЕМ САЙДБАР (Список сказок) */
        [data-testid="stSidebar"] {
            background-color: #050a18 !important;
        }

        /* Убираем рамки и квадраты вокруг кнопок в сайдбаре */
        [data-testid="stSidebar"] button {
            border: none !important;
            background: transparent !important;
            box-shadow: none !important;
            color: white !important;
            text-align: left !important;
            justify-content: flex-start !important;
            padding: 5px 0px !important;
        }

        /* Кнопка-корзинка (🗑️) без рамок */
        button[key*="del_"] {
            background: transparent !important;
            border: none !important;
            color: #ff4b4b !important;
            padding: 0 !important;
            min-width: 25px !important;
        }

        /* 4. ТЕКСТ В ПОЛЯХ (чтобы было видно, что пишешь) */
        input, textarea {
            color: #1e293b !important; /* Темный текст в белых полях */
            background-color: #ffffff !important;
        }

        /* 5. КНОПКИ ВРЕМЕНИ (чтобы не были белыми) */
        div[data-testid="stHorizontalBlock"] button {
            background-color: #1e293b !important;
            color: white !important;
            border: 1px solid #38bdf8 !important;
            text-align: center !important;
        }
        
        button[kind="primary"] {
            background: linear-gradient(135deg, #38bdf8, #1e40af) !important;
        }

        /* Кнопка ВЫХОД (Красная) */
        [data-testid="stSidebar"] .stButton:last-child button {
            border: 1px solid #ff4b4b !important;
            color: #ff4b4b !important;
            margin-top: 20px !important;
        }
        </style>
        """, unsafe_allow_html=True)
