import streamlit as st
from gtts import gTTS
import os
import tempfile
import difflib
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# DATA
# -----------------------------
PASSAGES = {    "Easy": "The sun is big and bright.",    "Medium": "The little rabbit hopped quickly through the forest.",    "Hard": "Elephants are fascinating animals because of their size and memory."}

# Track session data
if "history" not in st.session_state:
  st.session_state["history"] = []
  
# -----------------------------
# UI SETTINGS
# -----------------------------
st.set_page_config(page_title="LexiAI", layout="centered")

# Dyslexia mode toggle
dyslexia_mode = st.sidebar.checkbox("Activate Dyslexia-Friendly Mode")

if dyslexia_mode:
  st.markdown(        """        <style>        body {            background-color: #FFF9E6;        }        * {            font-family: 'OpenDyslexic', sans-serif !important;            line-height: 1.6;        }        </style>        """,        unsafe_allow_html=True    )
st.title("📖 LexiAI – Reading Coach for Kids")

# -----------------------------
# SELECT PASSAGE
# -----------------------------
level = st.radio("Choose a passage difficulty:", list(PASSAGES.keys()))
text = PASSAGES[level]st.write(f"**Passage:** {text}")

# -----------------------------
# LISTEN FEATURE
# -----------------------------
if st.button("🔊 Listen to Passage"):
  tts = gTTS(text)
  with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
    tts.save(fp.name)
    st.audio(fp.name, format="audio/mp3")
    
# -----------------------------
# READ ALOUD FEATURE
# -----------------------------
uploaded_audio = st.file_uploader("🎤 Read the passage aloud (upload a WAV/MP3)", type=["wav", "mp3"])
if uploaded_audio is not None:
  # Save temp file
  with tempfile.NamedTemporaryFile(delete=False) as fp:
    fp.write(uploaded_audio.read())
    audio_path = fp.name
    
    # For now, just mock transcription (no Google Speech to Text due to API key)
    # In real app: send audio_path to Google STT
    transcript = "the little rabbit hop quickly through forest"  # Demo fake output
    st.subheader("Your Reading (transcribed):")
    st.write(transcript)
    # Compare with passage
    diff = difflib.ndiff(text.lower().split(), transcript.lower().split())
    mistakes = [word for word in diff if word.startswith('- ')]
    if mistakes:
      st.error(f"Good try! You missed or misread {len(mistakes)} words:
      {', '.join([m[2:] for m in mistakes])}")
    else:
      st.success("Excellent! You read everything correctly 🎉")
    # Save to dashboard
    accuracy = round((1 - len(mistakes)/len(text.split())) * 100, 1)
    st.session_state["history"].append({"Passage": level, "Accuracy": accuracy})
    
# -----------------------------
# DASHBOARD
# -----------------------------
st.subheader("📊 Parent/Teacher Dashboard")
if st.session_state["history"]:
  df = pd.DataFrame(st.session_state["history"])
  st.dataframe(df)
    fig, ax = plt.subplots()
df.groupby("Passage")["Accuracy"].mean().plot(kind="bar", ax=ax)
ax.set_ylabel("Accuracy %")
st.pyplot(fig)
else:
st.info("No reading attempts yet. Try reading a passage!")

