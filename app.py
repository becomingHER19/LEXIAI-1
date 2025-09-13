import streamlit as st
import whisper
from gtts import gTTS
import os
import difflib
st.set_page_config(page_title="LexiAI", layout="wide")
st.title("📖 LexiAI – Interactive Reading Coach")
# Load Whisper model (small for speed)
@st.cache_resourcedef load_model():
return whisper.load_model("small")
model = load_model()
# Paragraphs
passages = {    "Easy": "The cat sat on the mat.",    "Medium": "Learning to read can be fun when we practice every day.",    "Hard": "Children with dyslexia face unique challenges, but technology can help them succeed."}
choice = st.selectbox("📚 Choose a passage difficulty:", list(passages.keys()))target_text = passages[choice]
st.markdown(f"### Passage to read:")st.write(target_text)
# Option to listen to passage
if st.button("🔊 Hear this passage"):
  tts = gTTS(text=target_text, lang="en")    tts.save("passage.mp3")    st.audio("passage.mp3")
# Upload child's reading audio
uploaded_audio = st.file_uploader("🎤 Upload your reading (MP3/WAV)", type=["mp3", "wav", "m4a"])
if uploaded_audio:
  with open("child_reading.wav", "wb") as f:
    f.write(uploaded_audio.getbuffer())
    st.info("⏳ Transcribing...")    
    result = model.transcribe("child_reading.wav")
    child_text = result["text"]
    st.markdown("### 🗣️ Child's Reading")
    st.write(child_text)
    # Compare with target
    seq = difflib.SequenceMatcher(None, target_text.lower(), child_text.lower())
    accuracy = round(seq.ratio() * 100, 2)
    st.markdown(f"### ✅ Accuracy: {accuracy}%")
    # Show corrections
st.markdown("### 🔎 Feedback")
target_words = target_text.split()
child_words = child_text.split()
feedback = []
for t, c in zip(target_words, child_words):
  if t.lower() != c.lower():
    
    feedback.append(f"Expected **{t}**, but heard **{c}**")
    if feedback:
      for fdb in feedback:
        st.warning(fdb)
    else:
      st.success("Great job! No major mistakes 🎉")
