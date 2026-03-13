import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        /* МАГИЧЕСКИЙ ФОН */
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1502740479735-539091932788?q=80&w=2070&auto=format&fit=crop");
            background-size: cover;
            background-attachment: fixed;
            color: #f8fafc;
        }
        
        /* Затемнение для читаемости контента */
        .stApp::before {
            content: "";
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(10, 15, 30, 0.7); /* Темная вуаль поверх картинки */
            z-index: -1;
        }

        /* Сайдбар */
        [data-testid="stSidebar"] { 
            background-color: rgba(17, 24, 39, 0.9) !important; 
            border-right: 2px solid #38bdf8; 
        }

        /* Кнопки времени (ФИКС БЕЛОГО ЦВЕТА) */
        div[data-testid="stHorizontalBlock"] div.stButton > button {
            height: 60px !important;
            width: 100% !important;
            border-radius: 12px !important;
            border: 2px solid #38bdf8 !important;
            background-color: #1e293b !important; /* Темный фон кнопки */
            color: #ffffff !important; /* Белый текст всегда */
        }
        
        div[data-testid="stHorizontalBlock"] div.stButton > button:hover {
            border-color: #ffffff !important;
            background-color: #2d3748 !important;
        }

        /* Кнопка Выход */
        .logout-btn {
            margin-top: 50px;
            color: #ff4b4b !important;
            text-align: center;
        }

        /* Центрирование основного блока */
        [data-testid="stVerticalBlock"] > div:has(div.stTextInput), 
        [data-testid="stVerticalBlock"] > div:has(div.stTextArea),
        .stForm {
            max-width: 650px !important;
            margin: auto !important;
            background: rgba(30, 41, 59, 0.5); /* Полупрозрачный фон для формы */
            padding: 30px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }

        .story-output { 
            background: #ffffff; 
            color: #1e293b !important; 
            padding: 40px; 
            border-radius: 30px; 
            font-size: 1.25em; 
            line-height: 1.8;
            max-width: 800px;
            margin: auto;
        }
        </style>
        """, unsafe_allow_html=True)
