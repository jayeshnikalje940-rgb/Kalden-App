import streamlit as st
import datetime
import google.generativeai as genai

# Page Config for Mobile friendly UI
st.set_page_config(page_title="Kalden AI", page_icon="📚")

# Sidebar for Subject selection (Yeh mobile mein menu jaisa dikhega)
st.sidebar.title("📚 Kalden Subjects")
subject = st.sidebar.selectbox("Choose Subject", ["History", "Geography", "Science", "Maths", "English"])
chapter = st.sidebar.text_input("Enter Chapter/Lesson Name")

# API Key Setup
api_key = st.sidebar.text_input("Enter API Key", type="password")

# Logic
def get_greeting():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12: return "Good Morning!"
    elif 12 <= hour < 17: return "Good Afternoon!"
    else: return "Hello!"

st.title(f"Kalden AI 🎓")
st.write(f"**{get_greeting()}** - I am Jayesh Sir, your personal 9th SSC tutor.")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask Jayesh Sir..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Jayesh Sir Persona Logic
        persona = f"""
        You are 'Kalden', acting as Jayesh Sir. 
        Student: 9th SSC Maharashtra Board. 
        Subject: {subject}, Chapter: {chapter}.
        Always prefix answer with 'Jayesh Sir:- '.
        Give explanations, notes, and solve test papers in a simple way.
        """
        
        with st.chat_message("assistant"):
            full_prompt = f"{persona}\nQuery: {prompt}"
            response = model.generate_content(full_prompt).text
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.warning("Sidebar mein API key enter karo shuru karne ke liye!")