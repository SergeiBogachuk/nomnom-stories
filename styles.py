import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        /* МАГИЧЕСКИЙ ФОН НА ВЕСЬ ЭКРАН */
        .stApp {
            background: linear-gradient(rgba(10, 15, 30, 0.7), rgba(10, 15, 30, 0.7)), 
                        url("https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?q=80&w=2013&auto=format&fit=crop") !important;
            background-size: cover !important;
            background-attachment: fixed !important;
        }

        /* ЦЕНТРАЛЬНАЯ КАРТОЧКА */
        [data-testid="stVerticalBlock"] > div:has(div.stTextInput), .stForm {
            background: rgba(255, 255, 255, 0.05) !important;
            backdrop-filter: blur(15px) !important;
            border: 1px solid rgba(56, 189, 248, 0.3) !important;
            padding: 40px !important;
            border-radius: 25px !important;
            max-width: 600px !important;
            margin: auto !important;
        }

        /* КНОПКИ ВРЕМЕНИ (ЯРКИЕ) */
        div.stButton > button {
            background-color: #1e293b !important;
            border: 2px solid #38bdf8 !important;
            color: white !important;
            height: 50px !important;
            font-weight: bold !important;
        }
        
        div.stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #38bdf8 0%, #1e40af 100%) !important;
            box-shadow: 0px 0px 15px rgba(56, 189, 248, 0.5) !important;
        }

        /* КОРЗИНКА (УДАЛЕНИЕ) */
        .delete-btn {
            color: #ff4b4b !important;
            font-size: 0.8em !important;
        }

        /* САЙДБАР */
        [data-testid="stSidebar"] { 
            background-color: #0f172a !important; 
            border-right: 1px solid #38bdf8 !important; 
        }

        /* ТЕКСТ СКАЗКИ (БЕЛАЯ БУМАГА) */
        .story-output {
            background: #ffffff !important;
            color: #1e293b !important;
            padding: 30px !important;
            border-radius: 20px !important;
            font-size: 1.2rem !important;
            line-height: 1.6 !important;
        }
        </style>
        """, unsafe_allow_html=True)
