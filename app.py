import streamlit as st
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO

# --- 1. Настройка страницы и кастомный дизайн (CSS) ---
st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="centered")

# Делаем приложение красивым
st.markdown("""
    <style>
    .stApp { background-color: #fdfbf7; font-family: 'Georgia', serif; }
    .stButton>button { 
        width: 100%; border-radius: 25px; height: 3.5em; 
        background-color: #6C5CE7; color: white; font-weight: bold;
        border: none; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #a29bfe; color: white; }
    h1 { color: #2d3436; text-align: center; font-size: 2.5em; }
    .story-card {
        background-color: white; padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px;
    }
    .stSelectbox label, .stSlider label, .stTextInput label, .stTextArea label {
        color: #444; font-weight: bold; font-size: 1.1em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Инициализация и настройки (Боковая панель) ---
with st.sidebar:
    st.header("⚙️ Настройки магии")
    api_key = st.text_input("Введите ваш OpenAI API Key", type="password")
    
    st.divider()
    st.header("👶 Профиль ребенка")
    child_name = st.text_input("Имя", value="Даша")
    child_age = st.slider("Возраст", 1, 12, 5)
    
    st.divider()
    lang = st.selectbox("Язык сказки", ["Русский", "English", "Română"])
    voice = st.selectbox("Голос озвучки", ["Female (Alloy)", "Male (Echo)"])

# --- 3. Главный экран: Параметры сказки ---
st.title("🌟 NomNom Stories")
st.write("<p style='text-align: center; font-size: 1.2em;'>Ваш личный сказочник на каждый вечер</p>", unsafe_allow_html=True)

st.header("О чем будет сказка сегодня?")

# Основная тема (оставляем для удобства)
issue = st.selectbox("Выберите психологический фокус:", [
    "Храбрость и новые места", 
    "Умение делиться игрушками", 
    "Победа над страхом темноты",
    "Любовь к полезной еде",
    "Уверенность в себе"
])

# Поле для ДЕТАЛИЗАЦИИ (Твой запрос)
details = st.text_area("Добавьте детали (необязательно):", 
                       placeholder=f"Например: {child_name} встречает волшебного единорога, или пусть действие происходит на шоколадной фабрике. Или добавьте любимую игрушку.")

# --- 4. Логика генерации (Текст + Картинка + Аудио) ---
if api_key:
    client = OpenAI(api_key=api_key)
    
    if st.button("Создать магию ✨"):
        # Создаем контейнер для красивого вывода
        story_container = st.container()
        
        with st.spinner('Пишем сказку, рисуем картинку и озвучиваем... Это займет около 30-40 секунд'):
            
            # --- ЧАСТЬ 1: Генерация ТЕКСТА (делаем длиннее) ---
            system_msg = f"Ты профессиональный детский писатель и сказкотерапевт. Твой стиль как у Pixar. Пиши на языке: {lang}."
            user_msg = f"Напиши длинную, подробную, волшебную сказку для ребенка по имени {child_name} (возраст: {child_age} лет). Тема сказки: {issue}. Дополнительные детали: {details}. Сказка должна быть метафоричной, с красивым описанием мира, диалогами героев и приключениями. В конце добавь 2 вопроса для обсуждения с ребенком."
            
            try:
                # Генерируем текст
                text_response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": user_msg}
                    ]
                )
                story_text = text_response.choices[0].message.content
                
                # --- ЧАСТЬ 2: Генерация КАРТИНКИ (DALL-E 3) ---
                # Формируем запрос для картинки
                image_prompt = f"Детская книжная иллюстрация в стиле Pixar. Маленькая девочка по имени {child_name}, {child_age} лет, в центре волшебного приключения. Тема сказки: {issue}. Детали: {details}. Яркие цвета, магическая атмосфера, милая и добрая."
                
                img_response = client.images.generate(
                    model="dall-e-3",
                    prompt=image_prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1
                )
                image_url = img_response.data[0].url
                
                # --- ЧАСТЬ 3: Вывод результата (Интерьер) ---
                with story_container:
                    st.markdown(f"## 📖 Сказка для {child_name}")
                    
                    # Показываем картинку
                    st.image(image_url, caption=f"Волшебный мир для {child_name}", use_column_width=True)
                    
                    # Показываем текст в красивой карточке
                    st.markdown(f"""
                        <div class="story-card">
                            {story_text.replace(chr(10), '<br>')}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.success("Волшебство готово! Можете читать.")
                    st.info("💡 Озвучка (Аудио) будет добавлена в следующем шаге!")
                    
            except Exception as e:
                st.error(f"Произошла ошибка: {e}. Проверьте ваш API ключ или баланс в OpenAI.")
else:
    st.warning("⚠️ Пожалуйста, введите ваш OpenAI API Key в панели слева.")
