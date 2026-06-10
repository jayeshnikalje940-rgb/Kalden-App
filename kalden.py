import streamlit as st
import datetime
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="Kalden AI", page_icon="🎓")

# App Title
st.title("🎓 Kalden Study Assistant")
st.write(f"**Jayesh Sir** - Your personal 9th SSC tutor.")

# Sidebar - Settings
st.sidebar.title("📚 Selection")
subject = st.sidebar.selectbox("Choose Subject", ["History", "Geography", "Science", "Maths", "English"])
chapter = st.sidebar.text_input("Enter Chapter Name")

# Sidebar - Quick Tools
st.sidebar.subheader("Quick Study Tools")
if st.sidebar.button("📝 Important Questions"):
    st.session_state.prompt = f"Subject: {subject}, Chapter: {chapter}. Is chapter ke 5 important questions do jo exams mein aate hain."

if st.sidebar.button("🧠 Chapter Summary"):
    st.session_state.prompt = f"Subject: {subject}, Chapter: {chapter}. Is chapter ki aasaan summary samjhao."

if st.sidebar.button("💡 Hard Concepts"):
    st.session_state.prompt = f"Subject: {subject}, Chapter: {chapter}. Is chapter ke hard concepts ko examples ke saath samjhao."

# API Configuration
try:
    genai.configure(api_key=st.secrets["API_KEY"])
    model = genai.GenerativeModel('gemini-3.5-flash')
except Exception as e:
    st.error("Configuration error!")

# Chat Logic
if "messages" not in st.session_state:
    st.session_state.messages = []

# Agar button click hua, toh prompt set karo
if "prompt" in st.session_state:
    user_input = st.session_state.prompt
    st.session_state.messages.append({"role": "user", "content": user_input})
    del st.session_state.prompt # Reset
else:
    user_input = st.chat_input("Ask Jayesh Sir...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        persona = "You are Kalden, acting as Jayesh Sir, 9th SSC tutor. Prefix answer with 'Jayesh Sir:- '."
        response = model.generate_content(f"{persona}\nQuery: {user_input}").text
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# Show old messages
for msg in st.session_state.messages:
    if msg["role"] != "user" or "Is chapter" not in msg["content"]: # Filter button prompts
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
