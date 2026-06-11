import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Page Config - Wide Layout taaki columns achhe dikhein
st.set_page_config(page_title="SSC Genius AI", page_icon="🎓", layout="wide")

# 2. Branding-Free CSS (Sidebar ko permanent hide kar diya)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            /* Hide the actual sidebar entirely */
            [data-testid="stSidebar"] {display: none;}
            /* Adjust padding for mobile */
            .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. API Setup
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel('gemini-3.5-flash')

# Persona
persona = "You are Jayesh Sir, a 9th SSC tutor. Be encouraging, clear, and always start your response with 'Jayesh Sir:- '."

# --- MAIN INTERFACE (Sidebar content moved to main area) ---
st.title("🎓 Jayesh Tutorial - SSC Genius AI")

# Creating two columns: Left for Menu, Right for Chat
col_menu, col_chat = st.columns([1, 2.2])

with col_menu:
    st.markdown("### 📋 Menu & Controls")
    subject = st.selectbox("Select Subject", ["History", "Geography", "Science", "Maths", "English"])
    
    st.markdown("---")
    st.subheader("📝 Test Generator")
    chapter_test = st.text_input("Enter Chapter Name")
    marks_test = st.number_input("Total Marks", min_value=5, max_value=100, value=20)
    q_type = st.radio("Question Type", ["Short Answer", "Long Answer", "Fill in the Blanks", "All Mixed"])

    if st.button("🚀 Generate Test Paper"):
        if chapter_test:
            with st.spinner("Jayesh Sir is preparing your test..."):
                test_prompt = f"{persona}\nGenerate a NEW and UNIQUE test paper for {subject}, Chapter: {chapter_test}. Total Marks: {marks_test}. Question Type: {q_type}."
                response = model.generate_content(test_prompt)
                if "messages" not in st.session_state:
                    st.session_state.messages = []
                st.session_state.messages.append({"role": "assistant", "content": f"Jayesh Sir:- Here is your test paper for {chapter_test}:\n\n{response.text}"})
                st.success("Test Generated! Check the chat.")
        else:
            st.warning("Please enter chapter name!")

with col_chat:
    st.markdown("### 💬 Chat with Jayesh Sir")
    
    # Image Upload within Chat Area
    uploaded_file = st.file_uploader("📸 Scan/Upload Question", type=["jpg", "jpeg", "png"])

    # Message Container
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display History
    chat_placeholder = st.container()
    with chat_placeholder:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Chat Input
    if prompt := st.chat_input("Ask a doubt..."):
        # User message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Jayesh Sir Response
        with st.spinner("Jayesh Sir is thinking..."):
            if uploaded_file:
                image = Image.open(uploaded_file)
                response = model.generate_content([f"{persona}\nSolve this:", image, prompt])
            else:
                response = model.generate_content(f"{persona}\nQuery: {prompt}")
            
            final_response = response.text
            
        with st.chat_message("assistant"):
            st.markdown(final_response)
        st.session_state.messages.append({"role": "assistant", "content": final_response})
