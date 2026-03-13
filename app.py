import streamlit as st
from openai import OpenAI

# 1. Настройка "ночного" сказочного стиля
st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #f8fafc; }
    .category-box {
        background: #1e293b;
        border: 2px solid #38bdf8;
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 15px;
        min-height: 180px;
    }
    .story-output {
        background: #fdfbf7;
        color: #1e293b;
        padding: 30px;
        border-radius: 25px;
        font-family: 'Georgia', serif;
        font-size: 1.2em;
        line-height: 1.7;
    }
    .stButton>button {
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 100%);
        color: white; border-radius: 30px; height: 4em; font-weight: bold; border: none; font-size: 1.2em;
    }
    h1, h2, h3 { color: #f8fafc !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Подключаем спрятанный ключ из Secrets
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error("Ключ не найден в Secrets! Пожалуйста, добавь его в настройки Streamlit.")
    st.stop()

# 3. Заголовок
st.title("🌟 NomNom Stories")
st.write("<p style='text-align: center; font-size: 1.3em;'>Инструмент для родителей: превращаем капризы в сказочные уроки</p>", unsafe_allow_html=True)

# 4. Профиль героя
st.markdown("### 👶 Кто сегодня герой?")
col_n, col_a, col_l = st.columns([2, 1, 1])
with col_n: name = st.text_input("Имя ребенка", value="Даша")
with col_a: age = st.slider("Возраст", 1, 12, 5)
with col_l: lang = st.selectbox("Язык", ["Русский", "English", "Română"])

st.divider()

# 5. Плиточное меню (Темы-психологи)
st.subheader("🎯 Выберите направление воспитания:")
col1, col2, col3 = st.columns(3)

theme = "Общая добрая сказка"

with col1:
    st.markdown('<div class="category-box"><h3>🛡️ Храбрость</h3><p>Для тех, кто боится темноты, врачей или новых мест</p></div>', unsafe_allow_html=True)
    if st.button("Выбрать: Храбрость"): theme = "Победа над страхами и уверенность в себе"

with col2:
    st.markdown('<div class="category-box"><h3>🍎 Привычки</h3><p>Если ребенок не хочет есть овощи или чистить зубы</p></div>', unsafe_allow_html=True)
    if st.button("Выбрать: Привычки"): theme = "Полезная еда и гигиена"

with col3:
    st.markdown('<div class="category-box"><h3>🤝 Отношения</h3><p>Учимся делиться, не драться и заводить друзей</p></div>', unsafe_allow_html=True)
    if st.button("Выбрать: Отношения"): theme = "Дружба и умение договариваться"

# Детали
st.write("")
details = st.text_area("✍️ Добавь подробности (необязательно):", placeholder="Например: Даша не хочет идти в садик или боится пауков...")

# 6. Кнопка запуска
if st.button("✨ СОЗДАТЬ ВОЛШЕБНУЮ ИСТОРИЮ ✨"):
    with st.spinner('Сказка пишется, магия рисуется...'):
        try:
            # Генерация текста (терапевтическая инструкция)
            system_instr = "Ты — детский психолог и сказочник Pixar. Твоя задача — через метафору помочь ребенку справиться с проблемой."
            user_instr = f"Напиши длинную сказку для {name} ({age} лет) на тему: {theme}. Учти детали: {details}. Язык: {lang}. В конце добавь 2 вопроса для ребенка."
            
            text_res = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": system_instr}, {"role": "user", "content": user_instr}]
            )
            story = text_res.choices[0].message.content

            # Генерация картинки
            img_res = client.images.generate(
                model="dall-e-3",
                prompt=f"Детская иллюстрация в стиле Pixar. Девочка {name}, {age} лет, в волшебном мире. Тема: {theme}. Яркая, теплая, магическая.",
                size="1024x1024"
            )
            
            # Озвучка
            audio_res = client.audio.speech.create(model="tts-1", voice="alloy", input=story[:4000])

            # Вывод всего на экран
            st.image(img_res.data[0].url, use_container_width=True)
            st.audio(audio_res.content)
            st.markdown(f'<div class="story-output">{story}</div>', unsafe_allow_html=True)
            st.balloons()
            
        except Exception as e:
            st.error(f"Произошла ошибка: {e}")
