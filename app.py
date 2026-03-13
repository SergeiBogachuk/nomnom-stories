import streamlit as st
from openai import OpenAI

# Настройка страницы
st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="wide")

# 1. CSS для правильной подсветки
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #f8fafc; }
    
    .category-box {
        padding: 30px;
        border-radius: 25px;
        text-align: center;
        transition: 0.3s ease-in-out;
        cursor: pointer;
        min-height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    /* Цвет ВЫБРАННОЙ карточки */
    .active-box {
        background: #3b82f6 !important; /* Яркий синий */
        color: white !important;
        box-shadow: 0 0 30px rgba(59, 130, 246, 0.6);
        border: 2px solid #60a5fa;
    }
    
    /* Цвет НЕАКТИВНЫХ карточек */
    .inactive-box {
        background: #1e293b;
        color: #94a3b8;
        border: 2px solid #334155;
    }

    /* Делаем невидимую кнопку поверх всей карточки */
    .stButton>button {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        opacity: 0;
        z-index: 10;
    }
    .stButton { position: relative; height: 150px; }

    .story-output { background: #fdfbf7; color: #1e293b; padding: 35px; border-radius: 25px; font-size: 1.3em; margin-top: 20px;}
    </style>
    """, unsafe_allow_html=True)

# 2. Инициализация выбора в памяти
if 'theme' not in st.session_state:
    st.session_state.theme = "Храбрость"

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🌟 NomNom Stories")

# 3. Профиль
st.markdown("### 👶 Настройки")
col_n, col_a, col_l = st.columns([2, 1, 1])
with col_n: name = st.text_input("Имя героя", value="Даша")
with col_a: age = st.slider("Возраст", 1, 12, 5)
with col_l: lang = st.selectbox("Язык", ["Русский", "English", "Română"])

st.divider()

# 4. Ряд карточек
st.subheader("🎯 Какую тему выберем?")
c1, c2, c3 = st.columns(3)

# Функция для отрисовки карточки
def draw_card(title, desc, icon, key_name, current_theme):
    is_active = (current_theme == key_name)
    css_class = "active-box" if is_active else "inactive-box"
    
    st.markdown(f'''
        <div class="category-box {css_class}">
            <h2 style="margin:0; color: inherit;">{icon}</h2>
            <h3 style="margin:0; color: inherit;">{title}</h3>
            <p style="margin:0; color: inherit; opacity: 0.8;">{desc}</p>
        </div>
    ''', unsafe_allow_html=True)
    
    if st.button("", key=f"btn_{key_name}"):
        st.session_state.theme = key_name
        st.rerun()

with c1:
    draw_card("Храбрость", "Побеждаем страхи", "🛡️", "Храбрость", st.session_state.theme)
with c2:
    draw_card("Привычки", "Полезная еда и сон", "🍎", "Привычки", st.session_state.theme)
with c3:
    draw_card("Отношения", "Дружба и общение", "🤝", "Отношения", st.session_state.theme)

st.write(f"✅ **Сейчас выбрано:** {st.session_state.theme}")

# Детали
details = st.text_area("✍️ Добавь подробности:")

st.divider()

# 5. Кнопка создания
if st.button("✨ СОЗДАТЬ ВОЛШЕБНУЮ ИСТОРИЮ ✨", key="main_gen"):
    with st.spinner('Магия в процессе...'):
        try:
            # Текст
            prompt = f"Напиши сказку для {name} ({age} лет) про {st.session_state.theme}. Детали: {details}. Язык: {lang}."
            res = client.chat.completions.create(model="gpt-4o", messages=[{"role":"user","content":prompt}])
            story = res.choices[0].message.content
            
            # Картинка
            img_res = client.images.generate(model="dall-e-3", prompt=f"Pixar style: {st.session_state.theme}, girl {name}, {age} years old.")
            
            # Аудио
            audio_res = client.audio.speech.create(model="tts-1", voice="alloy", input=story[:4000])

            st.image(img_res.data[0].url, use_container_width=True)
            st.audio(audio_res.content)
            st.markdown(f'<div class="story-output">{story}</div>', unsafe_allow_html=True)
            st.balloons()
        except Exception as e:
            st.error(f"Ошибка: {e}")
