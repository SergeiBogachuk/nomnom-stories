import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        .stApp { background: #0a0f1e; color: #f8fafc; }
        
        /* Кнопка сайдбара */
        button[kind="headerNoPadding"] {
            background-color: #38bdf8 !important;
            border-radius: 5px !important;
            box-shadow: 0px 0px 10px #38bdf8 !important;
        }

        [data-testid="stSidebar"] { 
            background-color: #111827 !important; 
            border-right: 2px solid #38bdf8; 
        }

        /* ЦЕНТРИРОВАНИЕ И ШИРИНА ПОЛЕЙ */
        /* Ограничиваем ширину основного блока и ставим по центру */
        [data-testid="stVerticalBlock"] > div:has(div.stTextInput), 
        [data-testid="stVerticalBlock"] > div:has(div.stTextArea),
        .stForm {
            max-width: 600px !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }

        /* Делаем текст ярким */
        p, label, span, .stMarkdown { 
            color: #ffffff !important; 
            font-weight: 600 !important;
        }

        /* Кнопки */
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
            max-width: 800px;
            margin: auto;
        }
        </style>
        """, unsafe_allow_html=True)
