import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        .stApp { background: #0a0f1e; color: #f8fafc; }
        [data-testid="stSidebar"] { background-color: #111827 !important; border-right: 2px solid #38bdf8; }
        
        /* Кнопки Длительности */
        div[data-testid="stHorizontalBlock"] div.stButton > button {
            height: 60px !important;
            width: 100% !important;
            border-radius: 12px !important;
            border: 2px solid #38bdf8 !important;
            background-color: #1e293b !important;
        }

        /* Выбранная кнопка (Primary) */
        div[data-testid="stHorizontalBlock"] div.stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #38bdf8 0%, #1e40af 100%) !important;
            border: none !important;
            box-shadow: 0px 0px 15px rgba(56, 189, 248, 0.6) !important;
        }

        div.stButton > button p { color: #FFFFFF !important; font-weight: 800 !important; font-size: 16px !important; }
        
        /* Чекбоксы */
        .stCheckbox label p { 
            color: #FFFFFF !important; 
            font-weight: 800 !important; 
            font-size: 16px !important; 
            text-shadow: 0px 0px 5px rgba(56, 189, 248, 0.5);
        }
        .stCheckbox { background: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #38bdf8; margin-bottom: 10px; }
        
        .story-output { 
            background: #ffffff; 
            color: #1e293b !important; 
            padding: 40px; 
            border-radius: 30px; 
            font-size: 1.25em; 
            line-height: 1.8; 
            white-space: pre-wrap; 
        }
        </style>
        """, unsafe_allow_html=True)
