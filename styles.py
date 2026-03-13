import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        /* --- 1. ФОН И ЯРКОСТЬ --- */
        .stApp {
            background: linear-gradient(rgba(10, 15, 30, 0.8), rgba(10, 15, 30, 0.8)), 
                        url("https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?q=80&w=2013&auto=format&fit=crop") !important;
            background-size: cover !important;
            background-attachment: fixed !important;
        }
        
        /* Убираем мутность текста */
        p, label, h1, h2, h3, [data-testid="stMarkdownContainer"] p { 
            color: #ffffff !important; 
            opacity: 1 !important;
            font-weight: 600 !important;
        }

        /* --- 2. ЛЕВАЯ КОЛОНКА (САЙДБАР) --- */
        [data-testid="stSidebar"], section[data-testid="stSidebar"] {
            background-color: #0f172a !important;
            border-right: 1px solid #38bdf8 !important;
            padding-right: 10px !important; /* Отступ справа, чтобы не выезжало */
        }
        
        /* Аккаунт: {email} */
        [data-testid="stSidebar"] .stAlert {
            background-color: rgba(56, 189, 248, 0.1) !important;
            border: 1px solid #38bdf8 !important;
            color: white !important;
        }

        /* --- ГЛАВНОЕ ИСПРАВЛЕНИЕ: СИНХРОНИЗАЦИЯ СКАЗОК И КОРЗИНЫ --- */
        /* Находим контейнер, где лежат название сказки и корзина */
        [data-testid="stHorizontalBlock"]:has(button[key*="del_"]) {
            display: flex !important;
            align-items: center !important; /* Центрируем по вертикали */
            justify-content: space-between !important; /* Сказка слева, корзина справа */
            width: 100% !important;
            margin-bottom: 8px !important;
        }
        
        /* Исправление названия сказки (левая колонка в блоке) */
        [data-testid="stHorizontalBlock"]:has(button[key*="del_"]) > div:first-child {
            width: 80% !important;
            flex-grow: 1 !important;
        }

        /* Кнопка с названием сказки */
        [data-testid="stHorizontalBlock"]:has(button[key*="del_"]) > div:first-child button {
            color: #ffffff !important;
            background-color: transparent !important;
            border: none !important;
            text-align: left !important;
            justify-content: flex-start !important;
            padding: 5px 0px !important;
            font-size: 16px !important;
        }
        
        /* Исправление корзины (правая колонка в блоке) */
        [data-testid="stHorizontalBlock"]:has(button[key*="del_"]) > div:last-child {
            width: 30px !important;
            margin-right: 5px !important;
        }

        /* --- ЧИСТАЯ КОРЗИНА БЕЗ КВАДРАТОВ --- */
        button[key*="del_"] {
            color: #ff4b4b !important; /* Красный цвет */
            font-size: 20px !important;
            background: transparent !important; /* Убираем фон */
            border: none !important; /* Убираем рамку */
            padding: 0 !important; /* Убираем отступы */
            width: 30px !important;
            height: 30px !important;
            box-shadow: none !important; /* Убираем тени */
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        
        /* Чтобы при наведении на корзину не появлялась рамка */
        button[key*="del_"]:hover {
            color: #ff6b6b !important;
            background: transparent !important;
            border: none !important;
        }

        /* --- 3. ЦЕНТРАЛЬНАЯ КАРТОЧКА --- */
        [data-testid="stForm"], .stForm {
            background: rgba(255, 255, 255, 0.05) !important;
            backdrop-filter: blur(15px) !important;
            border: 1px solid rgba(56, 189, 248, 0.3) !important;
            padding: 30px !important;
            border-radius: 20px !important;
        }

        /* Фикс кнопок времени (чтобы не были белыми) */
        div[data-testid="stHorizontalBlock"] button {
            background-color: #1e293b !important;
            color: white !important;
            border: 2px solid #38bdf8 !important;
        }
        
        div[data-testid="stHorizontalBlock"] button[kind="primary"] {
            background: linear-gradient(135deg, #38bdf8 0%, #1e40af 100%) !important;
            border: none !important;
        }
        </style>
        """, unsafe_allow_html=True)
