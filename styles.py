import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        /* 1. ТЕМНЫЙ ФОН */
        .stApp {
            background: linear-gradient(rgba(10, 15, 30, 0.9), rgba(10, 15, 30, 0.9)), 
                        url("https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?q=80&w=2013&auto=format&fit=crop") !important;
            background-size: cover !important;
        }

        /* 2. КОМПАКТНАЯ ШИРИНА (600px) */
        [data-testid="stMainViewContainer"] [data-testid="stVerticalBlock"] > div {
            max-width: 600px !important;
            margin: 0 auto !important;
        }

        /* 3. ЯРКИЙ БЕЛЫЙ ТЕКСТ */
        label p, .stMarkdown p, h1, h2, h3 {
            color: #ffffff !important;
            font-weight: 600 !important;
            opacity: 1 !important;
        }

        /* 4. САЙДБАР (ЛЕВАЯ ПАНЕЛЬ) */
        [data-testid="stSidebar"] {
            background-color: #050a18 !important;
            border-right: 1px solid #38bdf8 !important;
        }
        
        /* Кнопки сказок (чистые, без рамок) */
        [data-testid="stSidebar"] button {
            background: transparent !important;
            color: white !important;
            border: 1px solid rgba(56, 189, 248, 0.2) !important;
            text-align: left !important;
            margin-bottom: 5px !important;
        }

        /* 5. ПОЛЯ ВВОДА (ЧЕТКИЙ ТЕКСТ) */
        input, textarea, [data-baseweb="select"] * {
            color: #1e293b !important; /* Текст внутри полей - темный */
            background-color: #ffffff !important;
        }
        
        /* Кнопки времени */
        div[data-testid="stHorizontalBlock"] button {
            background-color: #1e293b !important;
            color: white !important;
            border: 1px solid #38bdf8 !important;
        }
        </style>
        """, unsafe_allow_html=True)
