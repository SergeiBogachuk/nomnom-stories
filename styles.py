import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        .stApp { background: #0a0f1e; color: #f8fafc; }
        [data-testid="stSidebar"] { background-color: #111827 !important; border-right: 2px solid #38bdf8; }
        
        /* Исправление мутности и прозрачности */
        p, label, span { color: #ffffff !important; opacity: 1 !important; }

        /* Кнопки в сайдбаре (Новая сказка) */
        section[data-testid="stSidebar"] .stButton > button {
            color: #ffffff !important;
            background-color: #1e293b !important;
            border: 1px solid #38bdf8 !important;
        }
        section[data-testid="stSidebar"] .stButton > button:hover {
            background-color: #38bdf8 !important;
            color: #0a0f1e !important;
        }

        /* Кнопки Длительности */
        div[data-testid="stHorizontalBlock"] div.stButton > button {
            height: 60px !important;
            width: 100% !important;
            border-radius: 12px !important;
            border: 2px solid #38bdf8 !important;
            background-color: #1e293b !important;
        }

        div[data-testid="stHorizontalBlock"] div.stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #38bdf8 0%, #1e40af 100%) !important;
            border: none !important;
        }

        div.stButton > button p { color: #FFFFFF !important; font-weight: 800 !important; font-size: 16px !important; }
        
        /* Чекбоксы (Яркость) */
        .stCheckbox { background: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #38bdf8; margin-bottom: 10px; }
        .stCheckbox label p { color: #FFFFFF !important; font-weight: 800 !important; }
        
        .story-output { background: #ffffff; color: #1e293b !important; padding: 40px; border-radius: 30px; font-size: 1.25em; line-height: 1.8; white-space: pre-wrap; }
        </style>
        """, unsafe_allow_html=True)
