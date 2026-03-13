import streamlit as st
from openai import OpenAI
import requests

# 1. Настройка стиля
st.set_page_config(page_title="NomNom Stories", page_icon="🎨", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #0e1117; color: #ffffff; }
    .story-box { background: white; color: #2d3436; padding: 30px; border-radius: 20px; font-size: 1.2em; line-height: 1.6; border: 5px solid #6C5CE7; }
    .stButton>button { background: #6C5CE7; color: white; border-radius: 50px; font-size: 20px; padding: 20px; width: 100%; border: none; }
    h1, h2 { text-align: center; color: #FF7675; }
    </style>
    """, unsafe_allow_html=True)

# 2. Боковая панель
with st.sidebar:
    st.header("🔮 Мастерская")
    api_key = st.text_input("Твой секретный ключ (API Key)", type="password")
    name = st.text_input("Имя ребенка", value="Даша")
    age = st.slider("Возраст", 1, 12, 5)
    lang = st.selectbox("Язык", ["Русский", "English", "Română"])

# 3. Главный экран
st.title("🌟 Твоя Волшебная Книга")

col1, col2, col3 = st.columns(3)
with col1:
    theme = st.radio("Выбери тему:", ["🛡️ Храбрость", "🍏 Здоровье", "🤝 Дружба"])
with col2:
    style = st.radio("Стиль иллюстрации:", ["Pixar 3D", "Акварель", "Комикс"])
with col3:
    length = st.radio("Длина:", ["Короткая", "Длинная (на 5 минут)"])

details = st.text_area("Добавь что-то особенное (например, любимую игрушку):")

if st.button("✨ СОЗДАТЬ СКАЗКУ ✨"):
    if not api_key:
        st.error("Вставь ключ слева!")
    else:
        client = OpenAI(api_key=api_key)
        with st.spinner('Магия в процессе... Рисуем и пишем...'):
            try:
                # ГЕНЕРАЦИЯ ТЕКСТА
                len_instr = "Напиши длинную сказку на 10 абзацев." if length == "Длинная (на 5 минут)" else "Напиши короткую сказку."
                full_prompt = f"{len_instr} Имя ребенка: {name}, возраст {age}. Тема: {theme}. Детали: {details}. Язык: {lang}. Сделай сказку психологической и доброй."
                
                text_res = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": full_prompt}]
                )
                story_text = text_res.choices[0].message.content

                # ГЕНЕРАЦИЯ КАРТИНКИ
                img_prompt = f"Детская книжная иллюстрация в стиле {style}. Девочка {name}, {age} лет. Сюжет: {theme}. Детали: {details}. Яркие цвета, милая атмосфера."
                img_res = client.images.generate(model="dall-e-3", prompt=img_prompt, size="1024x1024", n=1)
                img_url = img_res.data[0].url

                # ОЗВУЧКА
                audio_res = client.audio.speech.create(model="tts-1", voice="alloy", input=story_text[:4000])
                
                # ВЫВОД
                st.image(img_url, use_container_width=True) # Исправил параметр на современный
                st.audio(audio_res.content) 
                st.markdown(f'<div class="story-box">{story_text}</div>', unsafe_allow_html=True)
                st.balloons()

            except Exception as e:
                st.error(f"Упс! Что-то пошло не так: {e}")
