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

        /* ГЛАВНОЕ ИСПРАВЛЕНИЕ: БЛОК ВХОДА И СОЗДАНИЯ */
        [data-testid="stForm"], .stForm {
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(15px) !important;
            border: 1px solid rgba(56, 189, 248, 0.5) !important;
            padding: 40px !important;
            border-radius: 20px !important;
            
            /* Фиксируем нормальную ширину */
            min-width: 350px !important; 
            max-width: 500px !important;
            margin: 50px auto !important;
            display: block !important;
        }

        /* Чтобы поля внутри формы не сжимались */
        div[data-testid="stForm"] div[data-testid="stVerticalBlock"] > div {
            width: 100% !important;
        }

        /* Поля ввода */
        .stTextInput input {
            background-color: rgba(30, 41, 59, 0.9) !important;
            color: white !important;
            height: 50px !important;
            border: 1px solid #38bdf8 !important;
            font-size: 16px !important;
        }

        /* Кнопки */
        button[kind="primaryFormSubmit"], button[kind="primary"] {
            background: linear-gradient(135deg, #38bdf8 0%, #1e40af 100%) !important;
            border: none !important;
            height: 55px !important;
            font-weight: bold !important;
            width: 100% !important;
        }

        /* Текст */
        p, label, span, h1 { 
            color: #ffffff !important; 
            font-weight: 600 !important;
        }

        .story-output {
            background: #ffffff !important;
            color: #1e293b !important;
            padding: 30px !important;
            border-radius: 20px !important;
            max-width: 800px;
            margin: auto;
        }
        </style>
        """, unsafe_allow_html=True)
