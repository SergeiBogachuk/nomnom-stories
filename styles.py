import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        .stApp { background: #0a0f1e; color: #f8fafc; }
        
        /* СИЛОВОЙ МЕТОД: Показываем кнопку сайдбара, если она спрятана */
        header[data-testid="stHeader"] {
            background-color: rgba(0,0,0,0) !important;
        }
        
        /* Та самая кнопка "Гамбургер" (три полоски) */
        button[kind="headerNoPadding"] {
            background-color: #38bdf8 !important;
            border-radius: 5px !important;
            box-shadow: 0px 0px 15px #38bdf8 !important;
            z-index: 999999 !important;
            display: block !important;
        }

        [data-testid="stSidebar"] { 
            background-color: #111827 !important; 
            border-right: 2px solid #38bdf8; 
        }

        /* Текст и яркость */
        p, label, span, .stMarkdown { 
            color: #ffffff !important; 
            opacity: 1 !important; 
            font-weight: 600 !important;
        }

        /* Кнопки и градиент */
        div.stButton > button[kind="primary"], 
        button[kind="primaryFormSubmit"] {
            background: linear-gradient(135deg, #38bdf8 0%, #1e40af 100%) !important;
            border: none !important;
            color: white !important;
        }

        .stCheckbox { 
            background: #1e293b; 
            padding: 15px; 
            border-radius: 10px; 
            border: 1px solid #38bdf8; 
        }

        .story-output { 
            background: #ffffff; 
            color: #1e293b !important; 
            padding: 40px; 
            border-radius: 30px; 
            font-size: 1.25em; 
            line-height: 1.8; 
        }
        </style>
        """, unsafe_allow_html=True)
