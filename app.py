import streamlit as st
from openai import OpenAI

# Настройка страницы
st.set_page_config(page_title="NomNom Stories", page_icon="🌟")

# Дизайн
st.markdown("""
    <style>
    .stApp { background-color: #fdfbf7; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #6C5CE7; color: white; }
    </style>
    """, unsafe_content_safe=True)

st.title("🌟 NomNom Stories")
st.write("### Волшебные сказки для Даши и всех детей")

# Боковая панель
with st.sidebar:
    st.header("⚙️ Настройки")
    api_key = st.text_input("Введите ваш API Key", type="password")
    lang = st.selectbox("Язык", ["Русский", "English", "Română"])
    
    st.divider()
    name = st.text_input("Имя ребенка", value="Даша")
    age = st.slider("Возраст", 1, 12, 5)

# Основной выбор
issue = st.selectbox("Выберите тему сказки:", [
    "Храбрость", 
    "Умение делиться", 
    "Победа над страхом темноты",
    "Полезная еда",
    "Уверенность в себе"
])

if api_key:
    client = OpenAI(api_key=api_key)
    if st.button("Создать магию ✨"):
        with st.spinner('Пишем сказку...'):
            try:
                prompt = f"Напиши добрую сказку на языке {lang} для ребенка по имени {name}, возраст {age}. Тема: {issue}. В конце 2 вопроса."
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.markdown("---")
                st.write(response.choices[0].message.content)
                st.success("Готово!")
            except Exception as e:
                st.error(f"Ошибка: {e}")
else:
    st.info("Пожалуйста, введите API Key в меню слева.")
