st.set_page_config(
    page_title="Jayesh Tutorial", 
    page_icon="🎓", 
    layout="centered"
)
import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="SSC Genius AI", page_icon="🎓", layout="centered")

st.title("🎓 Jayesh Tutorial")
st.sidebar.header("Kalden")
subject = st.sidebar.selectbox("Subject", ["History", "Geography", "Science", "Maths", "English"])

# API Setup
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel('gemini-3.5-flash')

# Persona
persona = "You are Jayesh Sir, a 9th SSC tutor. Be encouraging, clear, and always start your response with 'Jayesh Sir:- '."

# --- Sidebar Test Generator ---
st.sidebar.markdown("---")
st.sidebar.subheader("Create Test Paper")
chapter_test = st.sidebar.text_input("Enter Chapter for Test")
marks_test = st.sidebar.number_input("Total Marks", min_value=5, max_value=100, value=20)
q_type = st.sidebar.radio("Question Type", ["Short Answer", "Long Answer", "Fill in the Blanks", "All Mixed"])

if st.sidebar.button("Generate Test Paper"):
    if chapter_test:
        with st.spinner("Jayesh Sir is preparing your test..."):
            test_prompt = f"{persona}\nGenerate a NEW and UNIQUE test paper for {subject}, Chapter: {chapter_test}. Total Marks: {marks_test}. Question Type: {q_type}. Do not repeat questions."
            response = model.generate_content(test_prompt)
            st.session_state.messages.append({"role": "assistant", "content": f"Jayesh Sir:- Here is your test paper:\n\n{response.text}"})
    else:
        st.sidebar.warning("Please enter a chapter name!")

# --- Chat Section ---
st.subheader("Chat with Jayesh Sir")
# Camera / Upload integrated here
uploaded_file = st.file_uploader("📸 Scan/Upload Question", type=["jpg", "jpeg", "png"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("Ask a doubt or paste an answer for grading..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.spinner("Jayesh Sir is thinking..."):
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.chat_message("user").image(image, caption="Uploaded Image")
            response = model.generate_content([f"{persona}\nSolve this:", image, prompt])
        else:
            response = model.generate_content(f"{persona}\nQuery: {prompt}")
            
        final_response = response.text
    
    st.chat_message("assistant").markdown(final_response)
    st.session_state.messages.append({"role": "assistant", "content": final_response})
