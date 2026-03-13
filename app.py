import streamlit as st
from openai import OpenAI

# Настройка страницы
st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="wide")

# 1. Улучшенный CSS для интерактивных карточек
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #f8fafc; }
    
    /* Стили для карточек тем */
    .category-box {
        padding: 30px;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 10px;
        border: 3px solid #38bdf8;
        transition: 0.3s ease-in-out;
        cursor: pointer; /* Делаем курсор "ручкой" */
    }
    
    /* Эффект при наведении */
    .category-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(56, 189, 248, 0.3);
    }
    
    /* Стили для АКТИВНОЙ (выбранной) карточки */
    .active-box {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%) !important;
        color: #0f172a !important;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.6);
        border: none !important;
    }
    
    /* Стили для НЕАКТИВНЫХ карточек */
    .inactive-box { background: #1e293b; color: #f8fafc; opacity: 0.7; }
    
    /* Убираем стандартные кнопки Streamlit, делаем их невидимыми поверх карточек */
    .stButton>button {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        opacity: 0; /* Делаем кнопку невидимой */
        border: none;
        cursor: pointer;
    }
    .stButton { position: relative; height: 100%; } /* Контейнер для кнопки */

    h3 { color: inherit !important; margin-top: 0; }
    p { color: inherit !important; margin-bottom: 0; }
    
    .story-output { background: #fdfbf7; color: #1e293b; padding: 35px; border-radius: 25px; font-size: 1.3em; }
    </style>
    """, unsafe_allow_html=True)

# 2. Инициализация выбора (память приложения)
if 'selected_theme' not in st.session_state:
    st.session_state.selected_theme = "Храбрость"

# Подключаем ключ из Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🌟 NomNom Stories")

# 3. Профиль героя
st.markdown("### 👶 Профиль")
col_n, col_a, col_l = st.columns([2, 1, 1])
with col_n: name = st.text_input("Имя героя", value="Даша")
with col_a: age = st.slider("Возраст", 1, 12, 5)
with col_l: lang = st.selectbox("Язык", ["Русский", "English", "Română"])

st.divider()

# 4. Плиточное меню без серых кнопок
st.subheader("🎯 Какая сказка нужна сегодня?")
col1, col2, col3 = st.columns(3)

with col1:
    # Определяем класс CSS (активная или нет)
    active_class = "active-box" if st.session_state.selected_theme == "Храбрость" else "inactive-box"
    
    # Рисуем саму карточку
    st.markdown(f'''
        <div class="category-box {active_class}">
            <h3>🛡️ Храбрость</h3>
            <p>Побеждаем страхи</p>
        </div>
    ''', unsafe_allow_html=True)
    
    # Поверх карточки кладем невидимую кнопку, которая фиксирует нажатие
    if st.button("", key="hidden_btn1"):
        st.session_state.selected_theme = "Храбрость"
        st.rerun()

with col2:
    active_class = "active-box" if st.session_state.selected_theme == "Привычки" else "inactive-box"
    st.markdown(f'''
        <div class="category-box {active_class}">
            <h3>🍎 Привычки</h3>
            <p>Полезная еда и сон</p>
        </div>
    ''', unsafe_allow_html=True)
    if st.button("", key="hidden_btn2"):
        st.session_state.selected_theme = "Привычки"
        st.rerun()

with col3:
    active_class = "active-box" if st.session_state.selected_theme == "Отношения" else "inactive-box"
    st.markdown(f'''
        <div class="category-box {active_class}">
            <h3>🤝 Отношения</h3>
            <p>Дружба и общение</p>
        </div>
    ''', unsafe_allow_html=True)
    if st.button("", key="hidden_btn3"):
        st.session_state.selected_theme = "Отношения"
        st.rerun()

# Отображаем выбор и поле для деталей
st.write(f"**Выбранное направление магии:** {st.session_state.selected_theme}")
details = st.text_area("✍️ Добавь подробности:")

st.divider()

# 5. Кнопка запуска
if st.button("✨ СОЗДАТЬ ВОЛШЕБНУЮ ИСТОРИЮ ✨"):
    with st.spinner('Магия в процессе... Рисуем и пишем...'):
        try:
            # Генерация текста
            prompt = f"Напиши сказку для {name} ({age} лет). Тема: {st.session_state.selected_theme}. Детали: {details}. Язык: {lang}. Стиль Pixar."
            res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
            story = res.choices[0].message.content
            
            # Генерация картинки
            img_res = client.images.generate(model="dall-e-3", prompt=f"Pixar style: {st.session_state.selected_theme}, girl {name}, {age} years old.")
            
            # Генерация аудио
            audio_res = client.audio.speech.create(model="tts-1", voice="alloy", input=story[:4000])

            # Вывод результата
            st.image(img_res.data[0].url, use_container_width=True)
            st.audio(audio_res.content)
            st.markdown(f'<div class="story-output">{story}</div>', unsafe_allow_html=True)
            st.balloons()
        except Exception as e:
            st.error(f"Упс! {e}")
