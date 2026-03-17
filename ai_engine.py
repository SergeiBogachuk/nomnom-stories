import base64
import os

import requests
import streamlit as st
from openai import OpenAI


def _secret_or_env(name):
    if name in st.secrets and st.secrets[name]:
        return st.secrets[name]

    value = os.getenv(name)
    if value:
        return value

    raise RuntimeError(f"Missing required secret: {name}")


@st.cache_resource(show_spinner=False)
def get_openai_client():
    return OpenAI(api_key=_secret_or_env("OPENAI_API_KEY"))


def _estimate_word_target(time_val):
    targets = {
        3: "350-500 words",
        5: "550-800 words",
        10: "900-1300 words",
    }
    return targets.get(time_val, "600-900 words")


def generate_story_text(child_name, lang, skills, details, time_val):
    skills_text = ", ".join(skills) if skills else "gentle confidence, calm, and kindness"
    story_context = details or "Create an original cozy bedtime situation that fits a young child."
    word_target = _estimate_word_target(time_val)
    model = os.getenv("OPENAI_MODEL") or (
        st.secrets["OPENAI_MODEL"] if "OPENAI_MODEL" in st.secrets else "gpt-5.3-chat-latest"
    )

    system_prompt = (
        "You are a warm children's bedtime storyteller with a strong understanding of gentle child "
        "development. You write emotionally safe fairy tales that model skills through story, not through "
        "lecturing. Keep everything soothing, imaginative, and appropriate for young children."
    )

    user_prompt = f"""
Write a complete bedtime fairy tale in {lang}.

Story requirements:
- The child's name is: {child_name}
- Gently support these themes or skills: {skills_text}
- Story context to include when helpful: {story_context}
- Target reading time: about {time_val} minutes ({word_target})
- The first line must be a short, beautiful title only
- After the title, write the story in short, readable paragraphs

Tone and safety requirements:
- Warm, magical, tender, and calming
- Show the skill through the character's journey instead of preaching
- No scary villains, humiliation, shame, or harsh punishment
- No sarcasm, cynicism, or overstimulation
- End with felt safety, emotional relief, and a gentle sense of growth

Writing quality:
- Make the child feel seen, capable, and comforted
- Use sensory details, but keep the pacing soft enough for bedtime
- Keep the plot coherent and complete
- Do not use markdown, bullet points, or section labels

Return only:
1. Title on the first line
2. The full story after that
""".strip()

    response = get_openai_client().chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    full_text = response.choices[0].message.content or ""
    return full_text.replace(":::writing", "").replace("###", "").strip()


def generate_image(title, child_name=None, lang=None, skills=None, details=None):
    try:
        skills_text = ", ".join(skills or [])
        details_text = details or "a calm and magical bedtime moment"
        prompt = f"""
Create a warm storybook cover illustration for a children's bedtime fairy tale.

Visual direction:
- soft painterly lighting
- gentle magical atmosphere
- expressive but calm character emotions
- cozy, imaginative composition for young children
- no text, no letters, no watermark

Story context:
- title: {title}
- child's name: {child_name or "child"}
- language context: {lang or "neutral"}
- themes: {skills_text or "kindness and emotional safety"}
- plot hints: {details_text}
""".strip()

        response = get_openai_client().images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
        )
        return response.data[0].url
    except Exception:
        return None


def get_speech_b64(text, voice_id):
    api_key = _secret_or_env("ELEVENLABS_API_KEY")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    response = requests.post(
        url,
        json={
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.45,
                "similarity_boost": 0.75,
            },
        },
        headers={
            "xi-api-key": api_key,
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
        },
        timeout=60,
    )

    if response.status_code == 200:
        return base64.b64encode(response.content).decode()

    return None
