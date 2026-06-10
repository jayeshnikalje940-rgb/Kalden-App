import streamlit as st
import datetime
import google.generativeai as genai

st.set_page_config(page_title="Kalden AI", page_icon="📚")

# Professional Sidebar
st.sidebar.title("📚 Kalden Subjects")
subject = st.sidebar.selectbox("Choose Subject", ["History", "Geography", "Science", "Maths", "English"])
chapter = st.sidebar.text_input("Enter Chapter/Lesson Name")

st.title("Kalden AI 🎓")
st.write(f"**{ 'Good Morning!' if 5 <= datetime.datetime.now().hour < 12 else 'Good Afternoon!' if 12 <= datetime.datetime.now().hour < 17 else 'Hello!' }** - I am Jayesh Sir, your personal 9th SSC tutor.")

# API Configuration via Secrets (No input box needed!)
try:
    genai.configure(api_key=st.secrets["API_KEY"])
    # Hum 2.0-flash use kar rahe hain kyunki ye stable hai
    model = genai.GenerativeModel('gemini-3.5-flash') 
except Exception as e:
    st.error("System configuration error. Please contact the administrator.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask Jayesh Sir..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    persona = f"You are 'Kalden', acting as Jayesh Sir. Student: 9th SSC Maharashtra Board. Subject: {subject}, Chapter: {chapter}. Always prefix answer with 'Jayesh Sir:- '."
    
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(f"{persona}\nQuery: {prompt}").text
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error("Error generating response. Please check API quota.")
