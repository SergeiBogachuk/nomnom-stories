import streamlit as st
from openai import OpenAI

# 1. Настройка страницы
st.set_page_config(page_title="NomNom Stories", page_icon="🌙", layout="centered")

# Словарь для перевода
translations = {
    "Русский": {
        "title": "🌟 NomNom Stories",
        "subtitle": "Превращаем капризы в сказочные уроки",
        "settings": "👶 Настройки героя",
        "name": "Имя героя",
        "age": "Возраст",
        "lang_label": "Язык",
        "theme_header": "🎯 Какую тему выберем?",
        "selected": "Сейчас выбрано",
        "themes": ["🛡️ Храбрость", "🍎 Привычки", "🤝 Отношения"],
        "details_label": "✍️ Добавь подробности:",
        "details_ph": "Например: Даша не хочет идти в садик...",
        "button": "✨ СОЗДАТЬ ВОЛШЕБНУЮ ИСТОРИЮ ✨",
        "processing": "Магия в процессе...",
    },
    "English": {
        "title": "🌟 NomNom Stories",
        "subtitle": "Turning tantrums into fairy tale lessons",
        "settings": "👶 Hero Settings",
        "name": "Hero Name",
        "age": "Age",
        "lang_label": "Language",
        "theme_header": "🎯 Which theme?",
        "selected": "Selected",
        "themes": ["🛡️ Bravery", "🍎 Habits", "🤝 Relationships"],
        "details_label": "✍️ Add details:",
        "details_ph": "Example: Dasha doesn't want to go to daycare...",
        "button": "✨ CREATE MAGICAL STORY ✨",
        "processing": "Magic in progress...",
    },
    "Română": {
        "title": "🌟 NomNom Stories",
        "subtitle": "Transformăm capriciile în lecții de basm",
        "settings": "👶 Setări Erou",
        "name": "Numele eroului",
        "age": "Vârsta",
        "lang_label": "Limba",
        "theme_header": "🎯 Ce temă alegem?",
        "selected": "Selectat",
        "themes": ["🛡️ Curaj", "🍎 Obiceiuri", "🤝 Relații"],
        "details_label": "✍️ Adaugă detalii:",
        "details_ph": "Exemplu: Dasha nu vrea să meargă la grădiniță...",
        "button": "✨ CREEAZĂ O POVESTE MAGICĂ ✨",
        "processing": "Magia este în curs...",
    }
}

# Дизайн
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #f8fafc; }
    .stButton>button { 
        height: 100px; font-size: 20px !important; border-radius: 20px; 
        border: 2px solid #38bdf8; background: #1e293b; color: white;
    }
    .story-output { background: #fdfbf7; color: #1e293b; padding: 35px; border-radius: 25px; font-size: 1.2em; margin-top: 20px;}
    /* Убираем лишние отступы у колонок */
    [data-testid="stVerticalBlock"] > div:contains("🌍") { width: 50% !important; }
    </style>
    """, unsafe_allow_html=True)

if 'theme_idx' not in st.session_state:
    st.session_state.theme_idx = 0

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- ВЕРХНЯЯ ПАНЕЛЬ (ЯЗЫК) ---
# Делаем выбор языка коротким, помещая его в колонку
col_l_top, _ = st.columns([1, 2])
with col_l_top:
    lang = st.selectbox("🌍 Language", ["Русский", "English", "Română"])

t = translations[lang]

st.title(t["title"])
st.write(f"<p style='text-align: center;'>{t['subtitle']}</p>", unsafe_allow_html=True)

st.divider()

# --- НАСТРОЙКИ ГЕРОЯ (ИМЯ И ВОЗРАСТ) ---
st.markdown(f"### {t['settings']}")
# Делаем имя коротким, используя колонки. 
# Соотношение [1, 1, 1] создаст три равные части, имя займет только одну.
col_name, col_age, _ = st.columns([1.5, 1.5, 1]) 
with col_name:
    name = st.text_input(t["name"], value="Даша")
with col_age:
    age = st.slider(t["age"], 1, 12, 5)

st.divider()

# --- ВЫБОР ТЕМЫ ---
st.subheader(f"{t['theme_header']}")
st.write(f"**{t['selected']}:** {t['themes'][st.session_state.theme_idx]}")

c1, c2, c3 = st.columns(3)
with c1:
    if st.button(t["themes"][0], use_container_width=True):
        st.session_state.theme_idx = 0
        st.rerun()
with c2:
    if st.button(t["themes"][1], use_container_width=True):
        st.session_state.theme_idx = 1
        st.rerun()
with c3:
    if st.button(t["themes"][2], use_container_width=True):
        st.session_state.theme_idx = 2
        st.rerun()

st.divider()

details = st.text_area(t["details_label"], placeholder=t["details_ph"])

if st.button(t["button"], type="primary", use_container_width=True):
    with st.spinner(t["processing"]):
        try:
            current_theme = t["themes"][st.session_state.theme_idx]
            prompt = f"Write a long fairy tale in {lang} for {name} ({age} years old). Theme: {current_theme}. Details: {details}. Pixar style."
            
            res = client.chat.completions.create(model="gpt-4o", messages=[{"role":"user","content":prompt}])
            story = res.choices[0].message.content
            
            img_res = client.images.generate(model="dall-e-3", prompt=f"Pixar style illustration: {current_theme}, child {name}, {age} years old.")
            audio_res = client.audio.speech.create(model="tts-1", voice="alloy", input=story[:4000])

            st.image(img_res.data[0].url, use_container_width=True)
            st.audio(audio_res.content)
            st.markdown(f'<div class="story-output">{story}</div>', unsafe_allow_html=True)
            st.balloons()
        except Exception as e:
            st.error(f"Error: {e}")
