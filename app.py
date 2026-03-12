import streamlit as st
from openai import OpenAI

# 1. Настройка страницы (иконка и заголовок в браузере)
st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="centered")

# 2. Кастомный дизайн (делаем приложение красивым)
st.markdown("""
    <style>
    .stApp { background-color: #fdfbf7; }
    .stButton>button { 
        width: 100%; 
        border-radius: 25px; 
        height: 3.5em; 
        background-color: #6C5CE7; 
        color: white; 
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #a29bfe; color: white; }
    h1 { color: #2d3436; text-align: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .stSelectbox label, .stSlider label, .stTextInput label { color: #444; font-weight: bold; }
    </style>
    """, unsafe_content_safe=True)

# 3. Главный заголовок
st.title("🌟 NomNom Stories")
st.write("<p style='text-align: center; font-size: 1.2em;'>Создавайте волшебные сказки вместе с ребенком</p>", unsafe_content_safe=True)

# 4. Настройки в боковой панели
with st.sidebar:
    st.header("⚙️ Настройки")
    api_key = st.text_input("Введите ваш API Key", type="password")
    language = st.selectbox("Язык сказки / Language", ["Русский", "English", "Română"])
    
    st.divider()
    st.header("👶 Профиль ребенка")
    child_name = st.text_input("Имя ребенка", value="Даша")
    child_age = st.slider("Возраст", 1, 12, 5)

# 5. Выбор темы на главном экране
st.subheader("О чем будет сказка сегодня?")
issue = st.selectbox("Выберите важную тему:", [
    "Храбрость и новые места", 
    "Умение делиться игрушками", 
    "Победа над страхом темноты",
    "Любовь к полезной еде",
    "Уверенность в себе и своих силах"
])

# 6. Логика генерации сказки
if api_key:
    client = OpenAI(api_key=api_key)
    
    if st.button("Создать магию ✨"):
        with st.spinner('Пишем сказку... Это займет 10 секунд'):
            # Промпт (инструкция) для ИИ
            system_msg = f"Ты профессиональный детский писатель и сказкотерапевт. Твой стиль как у Pixar. Пиши на языке: {language}."
            user_msg = f"Напиши добрую сказку для ребенка по имени {child_name} (возраст: {child_age} лет). Тема сказки: {issue}. Сказка должна быть метафоричной, не слишком долгой. В конце добавь 2 вопроса для обсуждения с ребенком."
            
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": user_msg}
                    ]
                )
                
                story_text = response.choices[0].message.content
                
                # Вывод результата
                st.markdown("---")
                st.markdown(f"## 📖 Сказка для {child_name}")
                st.write(story_text)
                
                # Анонс будущих фишек
                st.success("Сказка готова! Приятного чтения.")
                st.info("🎨 Скоро здесь появится кнопка 'Озвучить сказку' и волшебная картинка!")
                
            except Exception as e:
                st.error(f"Произошла ошибка: {e}. Проверьте ваш API ключ или баланс в OpenAI.")
else:
    st.warning("⚠️ Пожалуйста, введите ваш API Key в панели слева (Sidebar), чтобы начать.")

st.markdown("---")
st.caption("© 2026 NomNom Stories - Сделано с любовью для детей.")
