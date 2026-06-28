import streamlit as st
from groq import Groq

st.set_page_config(page_title="MoodTune", page_icon="🎵", layout="centered")

st.title("🎵 MoodTune")
st.subheader("Describe how you're feeling. Discover music made for this exact moment.")
st.markdown("---")
st.caption("Spotify keeps recommending songs you already know. MoodTune finds music that matches your mood right now.")

st.markdown("### How are you feeling right now?")
mood = st.text_area(
    "Describe your mood:",
    placeholder="e.g. I'm anxious but trying to wind down after a long day...",
    height=120
)

st.markdown("### Optional: Help me narrow it down")

col1, col2 = st.columns(2)
with col1:
    genre_pref = st.selectbox("Any genre preference?", [
        "No preference", "Indie/Alternative", "Pop", "Hip-hop/R&B",
        "Electronic", "Jazz/Soul", "Classical/Ambient", "Rock", "World Music"
    ])
with col2:
    familiarity = st.selectbox("How adventurous?", [
        "Surprise me completely",
        "Somewhat familiar territory",
        "Similar to what I know but new artists"
    ])

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
    avoid = st.text_input(
        "Any artists or genres to avoid?",
        placeholder="e.g. No heavy metal, avoid Ed Sheeran..."
    )

if st.button("🎧 Discover My Music", use_container_width=True):
    if not mood:
        st.warning("Please describe how you're feeling first!")
    else:
        with st.spinner("Finding music made for this exact moment..."):
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])

                genre_text = "" if genre_pref == "No preference" else "Genre: " + genre_pref + "."
                avoid_text = "" if not avoid else "Avoid: " + avoid + "."
                lang_text = "" if language_pref == "No preference" else "Language: " + language_pref + " only. All 5 songs must be in " + language_pref + "."

                lines = [
                    "You are a music discovery expert. Respond ONLY in English regardless of the song language.",
                    "",
                    "User mood: " + mood,
                    genre_text,
                    lang_text,
                    avoid_text,
                    "",
                    "Recommend exactly 5 songs the user has likely never heard. No mainstream mega-hits.",
                    "",
                    "IMPORTANT RULES:",
                    "- Write all your descriptions in English only",
                    "- Song titles and artist names should be in their original language/script",
                    "- For the Spotify link, combine the SONG TITLE and ARTIST NAME together with + signs",
                    "- Example Spotify URL format: https://open.spotify.com/search/Song+Title+Artist+Name/tracks",
                    "",
                    "For each song use EXACTLY this format:",
                    "",
                    "**[Number]. [Song Title in original language] - [Artist Name]**",
                    "Language/Origin: [language and country]",
                    "Why it fits your mood: [2 sentences in English explaining emotional connection]",
                    "Sound: [1 sentence describing vocals, instruments, or production style]",
                    "Search on Spotify: https://open.spotify.com/search/[SongTitle+ArtistName]/tracks",
                    "",
                    "---",
                    "",
                    "After all 5 songs write:",
                    "**Why MoodTune finds better music than Spotify:** [2 sentences comparing mood-based AI discovery vs Spotify history-based recommendations]",
                    "",
                    "Be emotionally intelligent, specific, and genuinely surprising with your picks."
                ]

                prompt = "\n".join(lines)

                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1500,
                    temperature=0.7
                )

                result = response.choices[0].message.content

                st.markdown("---")
                st.markdown("### 🎶 Your Discovery Playlist")
                st.markdown(result)
                st.markdown("---")
                st.info("Click any Spotify link above → Songs tab will open → pick the matching song and enjoy!")

            except Exception as e:
                st.error("Something went wrong. Please try again.")
                st.caption(str(e))

st.markdown("---")
st.caption("Built to solve Spotify's discovery problem | PM Project 2026")
