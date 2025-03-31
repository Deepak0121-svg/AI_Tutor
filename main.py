import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import urllib.parse

def get_youtube_video(topic, language):
    """Fetch a YouTube video related to the topic and language."""
    search_query = f"{topic} {language} educational video"
    return f"https://www.youtube.com/results?search_query={urllib.parse.quote(search_query)}"

def get_book_reference(topic):
    """Fetch book recommendations related to the topic."""
    search_query = f"Best books for learning {topic}"
    return f"https://www.google.com/search?q={urllib.parse.quote(search_query)}"

# Load API Key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

def get_gemini_response(user_query, level, language):
    """Generates response using Gemini Pro 1.5 based on class level and language."""
    model = genai.GenerativeModel("gemini-1.5-pro")
    full_query = f"Answer for a {level} student in {language}: {user_query}"
    response = model.generate_content(full_query)
    return response.text

# Streamlit UI
st.title("📖 AI Homework & Assignment Helper")
st.write("Ask me about Math, Science, Coding, and Essays!")

# Class selection
level = st.selectbox("Select Your Level:", ["Class 1-5", "Class 6-10", "class 11-12", "Undergraduate (UG)", "Postgraduate (PG)", "Research Scholar"])
language = st.selectbox("Select Language:", ["English", "Tamil", "Hindi", "Spanish", "French", "German"])

user_input = st.text_input("Enter your question:")
if st.button("Get Answer"):
    if user_input:
        answer = get_gemini_response(user_input, level, language)
        st.success(f"**AI Explanation ({level}) in {language}:** {answer}")
        
        youtube_link = get_youtube_video(user_input, language)
        books_link = get_book_reference(user_input)
        
        st.info(f"🔹 **YouTube Video in {language}:** [Click Here]({youtube_link})")
        st.info(f"📚 **Book Reference:** [Click Here]({books_link})")
