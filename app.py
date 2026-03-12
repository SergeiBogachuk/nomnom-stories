import streamlit as st
from openai import OpenAI

# Настройка заголовков и иконки (как мы обсуждали)
st.set_page_config(page_title="NomNom Stories", page_icon="🌟")

st.title("🌟 NomNom Stories")
st.subheader("AI Bedtime Stories for Growth & Confidence")

# Ввод API Ключа (потом спрячем его в настройки)
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

if api_key:
    client = OpenAI(api_key=api_key)

    # --- Меню создания Аватара ---
    st.sidebar.header("Child's Profile")
    child_name = st.sidebar.text_input("Child's Name", value="Dasha")
    child_age = st.sidebar.number_input("Age", min_value=1, max_value=12, value=7)

    # --- Выбор Психологического фокуса ---
    st.header(f"What shall {child_name} learn tonight?")
    issue = st.selectbox("Choose today's challenge:", [
        "Being brave in a new place",
        "Sharing toys with friends",
        "Not being afraid of the dark",
        "Public speaking / Confidence",
        "Trying new healthy food"
    ])

    if st.button("Generate Magic Story ✨"):
        with st.spinner('Magic is happening...'):
            prompt = f"Write a bedtime story for a {child_age} year old named {child_name}. Focus: {issue}. Make it magical, like a Pixar movie. Use metaphors. End with 2 reflection questions."
            
            response = client.chat.completions.create(
                model="gpt-4o", # Самая мощная модель 2026 года
                messages=[{"role": "user", "content": prompt}]
            )
            
            story = response.choices[0].message.content
            st.write("---")
            st.markdown(story)
            st.success("The story is ready! Sweet dreams!")

else:
    st.info("Please enter your OpenAI API Key in the sidebar to start.")
