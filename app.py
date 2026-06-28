import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="MoodTune — Spotify Discovery Agent",
    page_icon="🎵",
    layout="centered"
)

st.title("🎵 MoodTune")
st.subheader("Describe how you're feeling. Discover music made for this exact moment.")
st.markdown("---")
st.caption("Spotify keeps recommending songs you already know. MoodTune finds music that matches your mood right now — songs you've never heard but will love.")

st.markdown("### How are you feeling right now?")

mood = st.text_area(
    label="Describe your mood, moment, or what you need music for:",
    placeholder="e.g. I'm anxious but trying to wind down after a long day at work...\nor: I want something upbeat but not mainstream for my morning run\nor: I'm feeling nostalgic about old times but don't want to feel sad",
    height=120
)

st.markdown("### Optional: Help me narrow it down")

col1, col2 = st.columns(2)
with col1:
    genre_pref = st.selectbox(
        "Any genre preference?",
        ["No preference", "Indie/Alternative", "Pop", "Hip-hop/R&B", "Electronic", "Jazz/Soul", "Classical/Ambient", "Rock", "World Music"]
    )
with col2:
    familiarity = st.selectbox(
        "How adventurous?",
        ["Surprise me completely", "Somewhat familiar territory", "Similar to what I know but new artists"]
    )

col3, col4 = st.columns(2)
with col3:
    language_pref = st.selectbox(
        "Preferred language?",
