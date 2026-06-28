import streamlit as st
from groq import Groq

st.set_page_config(page_title="MoodTune", page_icon="🎵", layout="centered")

st.title("🎵 MoodTune")
st.subheader("Describe how you're feeling. Discover music made for this exact moment.")
st.markdown("---")
st.caption("Spotify keeps recommending songs you already know. MoodTune finds music that matches your mood right now.")

st.markdown("### How are you feeling right now?")
mood = st.text_area("Describe your mood:", placeholder="e.g. I'm anxious but trying to wind down after a long day...", height=120)

st.markdown("### Optional: Help me narrow it down")
col1, col2 = st.columns(2)
with col1:
    genre_pref = st.selectbox("Any genre preference?", ["No preference", "Indie/Alternative", "Pop", "Hip-hop/R&B", "Electronic", "Jazz/Soul", "Classical/Ambient", "Rock", "World Music"])
with col2:
    familiarity = st.selectbox("How adventurous?", ["Surprise me completely", "Somewhat familiar territory", "Similar to what I know but new artists"])

col3, col4 = st.columns(2)
with col3:
    language_pref = st.selectbox("Preferred language?", [
        "No preference",
        "Hindi", "Tamil", "Telugu", "Kannada", "Malayalam",
        "Punjabi", "Bengali", "Marathi", "Gujarati", "Odia",
        "Assamese", "Bhojpuri", "Rajasthani", "Haryanvi", "Urdu",
        "English", "Spanish", "Portuguese", "French",
        "Korean (K-pop)", "Japanese (J-pop)", "Mandarin Chinese",
        "Cantonese", "Arabic", "Turkish", "Indonesian/Malay",
        "Swahili", "Afrikaans", "Italian", "German", "Russian",
        "Greek", "Persian/Farsi", "Thai", "Vietnamese",
        "Filipino/Tagalog", "Dutch", "Polish", "Swedish",
        "Nigerian (Afrobeats)", "Amharic (Ethiopian)",
        "Instrumental (no lyrics)", "Sanskrit/Classical"
    ])
with col4:
    avoid = st.text_input("Any artists or genres to avoid?", placeholder="e.g. No heavy metal, avoid Ed Sheeran...")

if st.button("Discover My Music", use_container_width=True):
    if not mood:
        st.warning("Please describe how you're feeling first!")
    else:
        with st.spinner("Finding music made for this exact moment..."):
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])

                genre_text = "" if genre_pref == "No preference" else "Genre: " + genre_pref + "."
                avoid_text = "" if not avoid else "Avoid: " + avoid + "."
                lang_text = "" if language_pref == "No preference" else "Language: " + language_pref + " only."

                prompt = (
                    "You are a music discovery expert.\n\n"
                    "User mood: " + mood + "\n"
                    + genre_text + "\n"
                    + lang_text + "\n"
                    + avoid_text + "\n\n"
                    "Recommend 5 songs the user has likely never heard. Not mainstream hits.\n\n"
                    "For each song:\n"
                    "**[Number]. Song Title - Artist Name** (Language/Origin)\n"
                    "Why it fits: [2 sentences]\n"
                    "Sonic quality: [1 detail]\n"
                    "Spotify: https://open.spotify.com/search/[song+artist]/tracks\n\n"
                    "After all 5 songs add:\n"
                    "---\n"
                    "Why these are not your usual Spotify picks: [2 sentences]\n\n"
                    "Be specific and surprising. Language must match preference if set."
                )

                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}],
                )
