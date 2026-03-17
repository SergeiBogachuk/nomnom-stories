import os

import streamlit as st
from supabase import create_client


class EmptyResult:
    data = []


def _secret_or_env(name):
    if name in st.secrets and st.secrets[name]:
        return st.secrets[name]

    value = os.getenv(name)
    if value:
        return value

    raise RuntimeError(f"Missing required secret: {name}")


@st.cache_resource(show_spinner=False)
def get_supabase():
    return create_client(
        _secret_or_env("SUPABASE_URL"),
        _secret_or_env("SUPABASE_KEY"),
    )


def check_user(email, password):
    try:
        result = (
            get_supabase()
            .table("users")
            .select("id")
            .eq("email", email.strip())
            .eq("password", password)
            .limit(1)
            .execute()
        )
        return len(result.data) > 0
    except Exception:
        return False


def get_user_stories(email):
    try:
        return (
            get_supabase()
            .table("stories")
            .select("*")
            .eq("user_email", email.strip())
            .order("id", desc=True)
            .execute()
        )
    except Exception:
        return EmptyResult()


def save_story(story_data):
    payload = {
        "user_email": story_data.get("user_email"),
        "child_name": story_data.get("child_name"),
        "title": story_data.get("title"),
        "story_text": story_data.get("story_text"),
        "image_url": story_data.get("image_url"),
    }

    try:
        return get_supabase().table("stories").insert(payload).execute()
    except Exception:
        return None


def update_audio(story_id, audio_b64):
    try:
        return (
            get_supabase()
            .table("stories")
            .update({"audio_base64": audio_b64})
            .eq("id", story_id)
            .execute()
        )
    except Exception:
        return None


def delete_story(story_id):
    try:
        get_supabase().table("stories").delete().eq("id", story_id).execute()
        return True
    except Exception:
        return False
