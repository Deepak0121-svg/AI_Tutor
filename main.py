import os
import streamlit as st
from gtts import gTTS
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import uuid
import translators as ts

# ✅ Load API key from .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# ✅ Initialize Gemini AI Model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.6, google_api_key=API_KEY)

# ✅ Streamlit UI
st.title("🎓 AI Tutor & Homework Helper")
st.subheader("Ask any question, and the AI will explain it!")

# ✅ User Question
query = st.text_area("✍️ Enter your question:")

# ✅ Language Selection for Text Answer
text_language = st.selectbox("📜 Select Language for Text Answer:", ["English", "Tamil", "Hindi", "Malayalam"])

# ✅ Enable Voice Output
use_voice = st.checkbox("🔊 Enable Voice Answer")

# ✅ Language Selection for Voice Answer (if enabled)
if use_voice:
    voice_language = st.selectbox("🎤 Select Language for Voice Answer:", ["English", "Tamil", "Hindi", "Malayalam"])
else:
    voice_language = None  # No voice if not selected

# ✅ Language Mapping
lang_map = {"English": "en", "Tamil": "ta", "Hindi": "hi", "Malayalam": "ml"}

# ✅ Process Question
if st.button("🎯 Get Answer"):
    if query:
        # ✅ Step 1: Generate AI Explanation
        prompt = f"Provide a step-by-step explanation in {text_language} for: {query}"
        response = llm.invoke(prompt).content  

        st.write(f"🤖 Answer in {text_language}:")
        st.write(response)

        # ✅ Step 2: Convert to Voice (if enabled)
        if use_voice:
            # ✅ If text language is different from voice language, translate first
            if text_language != voice_language:
                translated_response = ts.translate_text(response, to_language=lang_map[voice_language])
            else:
                translated_response = response

            # ✅ Generate Voice File
            filename = f"answer_{uuid.uuid4().hex}.mp3"
            tts = gTTS(text=translated_response, lang=lang_map[voice_language])
            tts.save(filename)

            # ✅ Play the Audio
            st.audio(filename)

    else:
        st.warning("⚠️ Please enter a question.")
