import streamlit as st
import google.generativeai as genai
from PIL import Image

# Modern Page Config
st.set_page_config(page_title="Kalden Study AI", page_icon="🎓", layout="centered")

# Custom CSS for attractive look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #4CAF50; color: white; }
    .css-1r6slb0 { padding: 2rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 Kalden Study Assistant")
st.subheader("Your Personal 9th SSC Tutor")

# API Setup
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel('gemini-3.5-flash')

# Layout - Sidebar
st.sidebar.header("Study Setup")
subject = st.sidebar.selectbox("Select Subject", ["History", "Geography", "Science", "Maths", "English"])
chapter = st.sidebar.text_input("Enter Chapter Name")

st.sidebar.divider()
st.sidebar.subheader("Quick Actions")
if st.sidebar.button("📝 Important Questions"):
    st.session_state.prompt = f"Subject: {subject}, Chapter: {chapter}. Provide 5 important exam-oriented questions."
if st.sidebar.button("🧠 Chapter Summary"):
    st.session_state.prompt = f"Subject: {subject}, Chapter: {chapter}. Provide a concise and clear summary."
if st.sidebar.button("💡 Hard Concepts"):
    st.session_state.prompt = f"Subject: {subject}, Chapter: {chapter}. Explain the difficult concepts with simple examples."

# Scan & Upload Section
with st.expander("📸 Scan & Solve (Upload Image)"):
    uploaded_file = st.file_uploader("Upload your textbook page or question", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Question Snapshot", use_container_width=True)
        if st.button("Analyze & Solve"):
            with st.spinner("Jayesh Sir is analyzing..."):
                response = model.generate_content(["Solve this problem clearly for a 9th SSC student:", image])
                st.markdown(f"**Jayesh Sir:** {response.text}")

# Chat Logic
if "messages" not in st.session_state:
    st.session_state.messages = []

# Process button triggers
if "prompt" in st.session_state:
    user_input = st.session_state.prompt
    del st.session_state.prompt
else:
    user_input = st.chat_input("Ask Jayesh Sir a question about your studies...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        persona = "You are Kalden, a friendly 9th SSC tutor named Jayesh Sir. Be encouraging and clear."
        response = model.generate_content(f"{persona}\nQuery: {user_input}").text
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# Show history
for msg in st.session_state.messages:
    if msg["role"] != "user" or "Is chapter" not in msg["content"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
