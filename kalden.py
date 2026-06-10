import streamlit as st
import google.generativeai as genai
from PIL import Image

# Page Configuration
st.set_page_config(page_title="Kalden AI", page_icon="🎓", layout="centered")

# Styling
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 Kalden Study Assistant")
st.sidebar.header("Student Dashboard")
subject = st.sidebar.selectbox("Subject", ["History", "Geography", "Science", "Maths", "English"])

# API Setup
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel('gemini-3.5-flash')

# 1. Test Scoring Section
with st.expander("📝 Test Scoring & Feedback"):
    user_ans = st.text_area("Paste your answer here for grading:")
    if st.button("Get Marks & Feedback"):
        if user_ans:
            with st.spinner("Jayesh Sir is grading..."):
                prompt = f"Grade this answer for 9th SSC {subject}. Give marks out of 10 and suggest improvements: {user_ans}"
                response = model.generate_content(prompt)
                st.info(response.text)
        else:
            st.warning("Please paste an answer first.")

# 2. Chat Section
st.subheader("Chat with Jayesh Sir")
uploaded_file = st.file_uploader("📸 Scan/Upload Question", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

# Initialize Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input Logic
if prompt := st.chat_input("Type your question or ask for help..."):
    # Display user input
    st.chat_message("user").markdown(prompt)
    
    # Process Logic
    with st.spinner("Jayesh Sir is thinking..."):
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.chat_message("user").image(image, caption="Uploaded Image")
            response = model.generate_content(["Solve this for a 9th SSC student:", image, prompt])
        else:
            response = model.generate_content(prompt)
            
        final_response = response.text
    
    # Show Assistant Response
    st.chat_message("assistant").markdown(final_response)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": final_response})
