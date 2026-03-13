import streamlit as st
from openai import OpenAI

# Настройка страницы
st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="wide")

# Красивый дизайн
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #f8fafc; }
    .stButton>button { 
        height: 100px; 
        font-size: 20px !important; 
        border-radius: 20px; 
        border: 2px solid #38bdf8;
        background: #1e293b;
        color: white;
    }
    /* Стиль для активной кнопки (когда нажата) */
    .stButton>button:active, .stButton>button:focus {
        background: #3b82f6 !important;
        border: 2px solid white !important;
    }
    .story-output { background: #fdfbf7; color: #1e293b; padding: 35px; border-radius: 25px; font-size: 1.3em; margin-top: 20px;}
    h1, h2, h3 { text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# Инициализация выбора
if 'theme' not in st.session_state:
    st.session_state.theme = "🛡️ Храбрость"

# Подключаем ключ
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🌟 NomNom Stories")

# Профиль
st.markdown("### 👶 Настройки героя")
col_n, col_a, col_l = st.columns([2, 1, 1])
with col_n: name = st.text_input("Имя", value="Даша")
with col_a: age = st.slider("Возраст", 1, 12, 5)
with col_l: lang = st.selectbox("Язык", ["Русский", "English", "Română"])

st.divider()

# Кнопки выбора темы
st.subheader(f"🎯 Сейчас выбрано: {st.session_state.theme}")
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("🛡️\nХрабрость", use_container_width=True):
        st.session_state.theme = "🛡️ Храбрость"
        st.rerun()
with c2:
    if st.button("🍎\nПривычки", use_container_width=True):
        st.session_state.theme = "🍎 Привычки"
        st.rerun()
with c3:
    if st.button("🤝\nОтношения", use_container_width=True):
        st.session_state.theme = "🤝 Отношения"
        st.rerun()

st.divider()

details = st.text_area("✍️ Добавь подробности (о чем будет сказка сегодня?):")

# Кнопка создания
if st.button("✨ СОЗДАТЬ ВОЛШЕБНУЮ ИСТОРИЮ ✨", type="primary", use_container_width=True):
    with st.spinner('Магия в процессе... Это займет полминуты...'):
        try:
            # Текст
            prompt = f"Напиши сказку для {name} ({age} лет) про {st.session_state.theme}. Детали: {details}. Язык: {lang}. Стиль Pixar."
            res = client.chat.completions.create(model="gpt-4o", messages=[{"role":"user","content":prompt}])
            story = res.choices[0].message.content
            
            # Картинка
            img_res = client.images.generate(model="dall-e-3", prompt=f"Pixar style illustration: {st.session_state.theme}, child {name}, {age} years old.")
            
            # Аудио
            audio_res = client.audio.speech.create(model="tts-1", voice="alloy", input=story[:4000])

            # Вывод
            st.image(img_res.data[0].url, use_container_width=True)
            st.audio(audio_res.content)
            st.markdown(f'<div class="story-output">{story}</div>', unsafe_allow_html=True)
            st.balloons()
        except Exception as e:
            st.error(f"Ошибка: {e}")
