import streamlit as st
from groq import Groq

# Page config
st.set_page_config(
    page_title="MoodTune — Spotify Discovery Agent",
    page_icon="🎵",
    layout="centered"
)

# Header
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

                genre_text = "" if genre_pref == "No preference" else f"Genre leaning: {genre_pref}."
                avoid_text = "" if not avoid else f"Avoid: {avoid}."
                adventure_text = f"Discovery level: {familiarity}."

                prompt = f"""You are a music discovery expert who understands the emotional and sonic qualities of music deeply.

A user is feeling: "{mood}"
{genre_text}
{adventure_text}
{avoid_text}

The user is frustrated that Spotify keeps recommending songs they already know or songs from their own playlists. They want genuinely new discoveries.

Recommend exactly 5 songs that:
1. Match their emotional state RIGHT NOW
2. Are NOT mega-hits (no Taylor Swift chart toppers, no songs with 1B+ streams)
3. Are genuinely diverse — different artists, ideally different genres/subgenres
4. The user has likely NEVER heard before
5. Feel like a surprise that makes them think "how did it know?"

For each song provide:
**[Number]. Song Title — Artist Name**
🎭 *Why it fits your mood:* [2 sentences connecting their exact mood to this song]
🎵 *Sonic quality:* [One specific detail about vocals, instrumentation, or production that matches]
🔍 *Listen on Spotify:* https://open.spotify.com/search/[song+name+artist]

After the 5 songs, add:
---
💡 **Why these aren't your usual Spotify picks:** [2 sentences explaining how mood-based discovery differs from Spotify's history-based recommendations]

Be specific, emotionally intelligent, and genuinely surprising. Avoid obvious choices."""

                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1500,
                    temperature=0.7
                )

                st.markdown("---")
                st.markdown("### 🎶 Your Discovery Playlist")
                st.markdown(response.choices[0].message.content)
                st.markdown("---")
                st.success("Found something you'll love? Save it to Spotify before you forget!")

            except Exception as e:
                st.error("Something went wrong. Please try again.")
                st.caption(str(e))

st.markdown("---")
st.caption("Built to solve Spotify's discovery problem | PM Project 2026")
