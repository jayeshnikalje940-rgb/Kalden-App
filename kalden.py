import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="Kalden AI", page_icon="🎓", layout="centered")

# Styling
st.markdown("<style>.stApp { background-color: #f4f7f6; }</style>", unsafe_allow_html=True)

st.title("🎓 Kalden Study Assistant")
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel('gemini-3.5-flash')

# Persona
persona = "You are Jayesh Sir, a 9th SSC tutor. Be encouraging, clear, and always start your response with 'Jayesh Sir:- '."

# --- Sidebar Test Generator ---
st.sidebar.header("Student Dashboard")
subject = st.sidebar.selectbox("Subject", ["History", "Geography", "Science", "Maths", "English"])

st.sidebar.markdown("---")
st.sidebar.subheader("Create Test Paper")
chapter_test = st.sidebar.text_input("Enter Chapter for Test")
marks_test = st.sidebar.number_input("Total Marks", min_value=5, max_value=100, value=20)
q_type = st.sidebar.radio("Question Type", ["Short Answer", "Long Answer", "Fill in the Blanks", "All Mixed"])

if st.sidebar.button("Generate Test Paper"):
    if chapter_test:
        test_prompt = f"{persona}\nGenerate a NEW and UNIQUE test paper for {subject}, Chapter: {chapter_test}. Total Marks: {marks_test}. Question Type: {q_type}. Do not repeat questions."
        with st.spinner("Jayesh Sir is preparing your test..."):
            response = model.generate_content(test_prompt)
            st.session_state.messages.append({"role": "assistant", "content": f"Jayesh Sir:- Here is your test paper:\n\n{response.text}"})
    else:
        st.sidebar.warning("Please enter a chapter name!")

# --- Chat Section ---
st.subheader("Chat with Jayesh Sir")
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("Ask a doubt or paste an answer for grading..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.spinner("Jayesh Sir is thinking..."):
        # Check if user wants grading or general help
        full_prompt = f"{persona}\nQuery: {prompt}"
        response = model.generate_content(full_prompt)
        final_response = response.text
        
    st.chat_message("assistant").markdown(final_response)
    st.session_state.messages.append({"role": "assistant", "content": final_response})
