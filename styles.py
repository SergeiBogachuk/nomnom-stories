import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        .stApp { 
            background: linear-gradient(rgba(10, 15, 30, 0.8), rgba(10, 15, 30, 0.8)), 
                        url("https://images.unsplash.com/photo-1534796636912-3b95b3ab5986?q=80&w=2000&auto=format&fit=crop") !important;
            background-size: cover !important;
            background-attachment: fixed !important;
            color: #f8fafc; 
        }
        
        button[kind="headerNoPadding"] {
            background-color: #38bdf8 !important;
            border-radius: 5px !important;
            box-shadow: 0px 0px 10px #38bdf8 !important;
        }

        [data-testid="stSidebar"] { 
            background-color: #111827 !important; 
            border-right: 2px solid #38bdf8; 
        }

        [data-testid="stVerticalBlock"] > div:has(div.stTextInput), 
        [data-testid="stVerticalBlock"] > div:has(div.stTextArea),
        .stForm {
            max-width: 600px !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }

        /* Обычный интерфейсный текст */
        p, label, span { 
            color: #ffffff !important; 
            font-weight: 600 !important;
        }

        .stMarkdown { 
            color: #ffffff !important; 
        }

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

        /* Карточка сказки */
        .story-output { 
            background: #ffffff !important; 
            color: #1e293b !important; 
            padding: 40px; 
            border-radius: 30px; 
            font-size: 1.25em; 
            line-height: 1.8; 
            max-width: 800px;
            margin: auto;
            white-space: pre-wrap;
            box-shadow: 0 4px 18px rgba(0,0,0,0.12);
        }

        /* ВАЖНО: принудительно делаем весь текст внутри сказки тёмным */
        .story-output,
        .story-output p,
        .story-output span,
        .story-output div,
        .story-output strong,
        .story-output em,
        .story-output li,
        .story-output h1,
        .story-output h2,
        .story-output h3,
        .story-output h4,
        .story-output h5,
        .story-output h6 {
            color: #1e293b !important;
            font-weight: 400 !important;
        }
        </style>
        """, unsafe_allow_html=True)
