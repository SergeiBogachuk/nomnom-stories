import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="wide")

# 1. Улучшенный CSS для активных плиток
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #f8fafc; }
    .category-box {
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 10px;
        border: 2px solid #38bdf8;
        transition: 0.3s;
    }
    .active-box {
        background: #38bdf8 !important;
        color: #0f172a !important;
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.5);
    }
    .inactive-box { background: #1e293b; color: #f8fafc; opacity: 0.6; }
    .stButton>button { width: 100%; border-radius: 20px; font-weight: bold; }
    .story-output { background: #fdfbf7; color: #1e293b; padding: 30px; border-radius: 25px; font-size: 1.2em; }
    </style>
    """, unsafe_allow_html=True)

# 2. Инициализация выбора (чтобы приложение "помнило", что мы нажали)
if 'selected_theme' not in st.session_state:
    st.session_state.selected_theme = "Храбрость"

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🌟 NomNom Stories")

# 3. Профиль
col_n, col_a, col_l = st.columns([2, 1, 1])
with col_n: name = st.text_input("Имя ребенка", value="Даша")
with col_a: age = st.slider("Возраст", 1, 12, 5)
with col_l: lang = st.selectbox("Язык", ["Русский", "English", "Română"])

st.divider()

# 4. Плиточное меню с подсветкой выбранной темы
st.subheader("🎯 Выберите направление:")
col1, col2, col3 = st.columns(3)

with col1:
    active_class = "active-box" if st.session_state.selected_theme == "Храбрость" else "inactive-box"
    st.markdown(f'<div class="category-box {active_class}"><h3>🛡️ Храбрость</h3><p>Побеждаем страхи</p></div>', unsafe_allow_html=True)
    if st.button("Выбрать Храбрость", key="btn1"):
        st.session_state.selected_theme = "Храбрость"
        st.rerun()

with col2:
    active_class = "active-box" if st.session_state.selected_theme == "Привычки" else "inactive-box"
    st.markdown(f'<div class="category-box {active_class}"><h3>🍎 Привычки</h3><p>Полезная еда и сон</p></div>', unsafe_allow_html=True)
    if st.button("Выбрать Привычки", key="btn2"):
        st.session_state.selected_theme = "Привычки"
        st.rerun()

with col3:
    active_class = "active-box" if st.session_state.selected_theme == "Отношения" else "inactive-box"
    st.markdown(f'<div class="category-box {active_class}"><h3>🤝 Отношения</h3><p>Дружба и общение</p></div>', unsafe_allow_html=True)
    if st.button("Выбрать Отношения", key="btn3"):
        st.session_state.selected_theme = "Отношения"
        st.rerun()

st.write(f"**Выбрано направление:** {st.session_state.selected_theme}")
details = st.text_area("✍️ Добавь подробности:")

if st.button("✨ СОЗДАТЬ ВОЛШЕБНУЮ ИСТОРИЮ ✨"):
    with st.spinner('Магия в процессе...'):
        try:
            # Текст
            prompt = f"Напиши сказку для {name} ({age} лет). Тема: {st.session_state.selected_theme}. Детали: {details}. Язык: {lang}."
            res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
            story = res.choices[0].message.content
            
            # Картинка
            img_res = client.images.generate(model="dall-e-3", prompt=f"Pixar style illustration: {st.session_state.selected_theme}, girl {name}, {age} years old.")
            
            # Озвучка
            audio_res = client.audio.speech.create(model="tts-1", voice="alloy", input=story[:4000])

            st.image(img_res.data[0].url, use_container_width=True)
            st.audio(audio_res.content)
            st.markdown(f'<div class="story-output">{story}</div>', unsafe_allow_html=True)
            st.balloons()
        except Exception as e:
            st.error(f"Ошибка: {e}")
