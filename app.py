import streamlit as st
from openai import OpenAI

# 1. Настройка "сказочного" стиля
st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="wide")

st.markdown("""
    <style>
    /* Фон и шрифты */
    .stApp {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        color: #e94560;
    }
    /* Карточки разделов */
    .category-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid #e94560;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        transition: 0.3s;
    }
    /* Главная кнопка */
    .stButton>button {
        background: linear-gradient(90deg, #e94560 0%, #950740 100%);
        color: white;
        font-size: 24px !important;
        height: 80px;
        border-radius: 40px;
        border: none;
        box-shadow: 0 10px 20px rgba(233, 69, 96, 0.3);
    }
    h1, h2, h3 { color: #fdfbf7 !important; text-align: center; }
    p { color: #fdfbf7; }
    </style>
    """, unsafe_allow_html=True)

# 2. Боковая панель (профиль)
with st.sidebar:
    st.title("👨‍👩‍👧 Профиль")
    api_key = st.text_input("Введи свой волшебный ключ (API Key)", type="password")
    name = st.text_input("Имя героя", value="Даша")
    age = st.slider("Сколько лет герою?", 1, 12, 5)
    lang = st.selectbox("Язык", ["Русский", "English", "Română"])

# 3. Основной экран
st.title("🌟 Добро пожаловать в NomNom Stories")
st.write("### Выбери направление для сегодняшнего урока:")

# Создаем красивые колонки для разделов
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="category-card"><h3>🛡️ Храбрость</h3><p>Учимся побеждать страхи</p></div>', unsafe_allow_html=True)
    b1 = st.checkbox("Выбрать 'Храбрость'", key="c1")

with col2:
    st.markdown('<div class="category-card"><h3>🍏 Здоровье</h3><p>Почему овощи — это сила</p></div>', unsafe_allow_html=True)
    b2 = st.checkbox("Выбрать 'Здоровье'", key="c2")

with col3:
    st.markdown('<div class="category-card"><h3>🤝 Дружба</h3><p>Как делиться и помогать</p></div>', unsafe_allow_html=True)
    b3 = st.checkbox("Выбрать 'Дружба'", key="c3")

st.divider()

# Детали сказки
st.subheader("📝 Добавь свои детали (по желанию):")
details = st.text_area("", placeholder="Например: В сказке есть синий слон и мы летим на Луну...")

# ГЛАВНАЯ КНОПКА
if st.button("✨ НАЧАТЬ ВОЛШЕБСТВО ✨"):
    if not api_key:
        st.error("Упс! Ты забыл ввести API ключ в колонке слева!")
    else:
        client = OpenAI(api_key=api_key)
        with st.spinner('Сказка пишется, картинки рисуются...'):
            try:
                # Генерируем текст
                prompt = f"Напиши длинную психологическую сказку для {name} ({age} лет). Тема: {details}. Язык: {lang}. Стиль Pixar."
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.markdown(f'<div style="background: white; color: black; padding: 30px; border-radius: 20px;">{response.choices[0].message.content}</div>', unsafe_allow_html=True)
                st.balloons()
            except Exception as e:
                st.error(f"Ошибка: {e}")
