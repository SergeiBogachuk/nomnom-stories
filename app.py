import streamlit as st
from openai import OpenAI

# 1. Базовые настройки страницы
st.set_page_config(page_title="NomNom Stories", page_icon="🌟")

# 2. Дизайн (CSS) — здесь была ошибка, теперь всё четко
st.markdown("""
    <style>
    .stApp { background-color: #fdfbf7; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #6C5CE7; color: white; border: none; }
    h1 { color: #2d3436; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌟 NomNom Stories")
st.write("<p style='text-align: center;'>Волшебные сказки для детей</p>", unsafe_allow_html=True)

# 3. Боковая панель
with st.sidebar:
    st.header("⚙️ Настройки")
    api_key = st.text_input("Введите ваш API Key", type="password")
    lang = st.selectbox("Выберите язык", ["Русский", "English", "Română"])
    
    st.divider()
    name = st.text_input("Имя ребенка", value="Даша")
    age = st.slider("Возраст", 1, 12, 5)

# 4. Выбор темы
st.subheader("О чем будет сказка сегодня?")
issue = st.selectbox("", [
    "Храбрость и новые места", 
    "Умение делиться игрушками", 
    "Победа над страхом темноты",
    "Любовь к полезной еде",
    "Уверенность в себе"
])

# 5. Логика работы
if api_key:
    client = OpenAI(api_key=api_key)
    if st.button("Создать магию ✨"):
        with st.spinner('Пишем сказку...'):
            try:
                # Промпт для ИИ
                prompt = f"Напиши добрую сказку на языке {lang} для ребенка по имени {name}, возраст {age}. Тема: {issue}. В конце добавь 2 вопроса для обсуждения."
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                story = response.choices[0].message.content
                st.markdown("---")
                st.markdown(f"### 📖 Сказка для {name}")
                st.write(story)
                st.success("Готово! Приятного чтения.")
                
            except Exception as e:
                st.error(f"Ошибка API: {e}")
else:
    st.info("Пожалуйста, введите ваш API Key в меню слева.")
