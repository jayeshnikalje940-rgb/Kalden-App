import streamlit as st
import google.generativeai as genai
from PIL import Image

# Page Config
st.set_page_config(page_title="Kalden AI", page_icon="🎓")
st.title("🎓 Kalden Study Assistant")
st.write(f"**Jayesh Sir** - Your personal 9th SSC tutor.")

# Sidebar - Settings
st.sidebar.title("📚 Selection")
subject = st.sidebar.selectbox("Choose Subject", ["History", "Geography", "Science", "Maths", "English"])
chapter = st.sidebar.text_input("Enter Chapter Name")

# API Configuration
try:
    genai.configure(api_key=st.secrets["API_KEY"])
    # 1.5-flash is best for both text and image scanning
    model = genai.GenerativeModel('gemini-3.5-flash')
except Exception as e:
    st.error("Configuration error!")

# Sidebar - Quick Tools
st.sidebar.subheader("Quick Study Tools")
if st.sidebar.button("📝 Important Questions"):
    st.session_state.prompt = f"Subject: {subject}, Chapter: {chapter}. Is chapter ke 5 important questions do."
if st.sidebar.button("🧠 Chapter Summary"):
    st.session_state.prompt = f"Subject: {subject}, Chapter: {chapter}. Is chapter ki aasaan summary samjhao."
if st.sidebar.button("💡 Hard Concepts"):
    st.session_state.prompt = f"Subject: {subject}, Chapter: {chapter}. Is chapter ke hard concepts examples ke saath samjhao."

# Photo Upload / Scan Feature
st.subheader("📸 Scan & Solve")
uploaded_file = st.file_uploader("Textbook page ya question ka photo upload karo", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Question", use_container_width=True)
    if st.button("Solve this Question"):
        with st.spinner("Jayesh Sir solving..."):
            response = model.generate_content(["Solve this problem for 9th SSC student:", image])
            st.markdown(f"**Jayesh Sir:-** {response.text}")

# Chat Logic
if "messages" not in st.session_state:
    st.session_state.messages = []

# Buttons trigger prompt
if "prompt" in st.session_state:
    user_input = st.session_state.prompt
    del st.session_state.prompt
else:
    user_input = st.chat_input("Ask Jayesh Sir...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        persona = "You are Kalden, acting as Jayesh Sir, 9th SSC tutor. Always prefix answer with 'Jayesh Sir:- '."
        response = model.generate_content(f"{persona}\nQuery: {user_input}").text
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# Show chat history
for msg in st.session_state.messages:
    if msg["role"] != "user" or "Is chapter" not in msg["content"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
