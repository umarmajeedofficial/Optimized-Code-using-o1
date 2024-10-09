# main.py

import streamlit as st
import time
from models.o1_preview import O1PreviewModel
from models.o1_mini import O1MiniModel
from models.llama import LlamaModel

# Initialize the OpenAI clients for both models
o1_preview_model = O1PreviewModel(
    api_key=st.secrets["openai"]["api_key"],
    base_url="https://api.aimlapi.com"
)

o1_mini_model = O1MiniModel(
    api_key=st.secrets["openai_mini"]["api_key"],
    base_url="https://api.aimlapi.com"
)

# Initialize the Llama client
llama_model = LlamaModel(
    api_key=st.secrets["together"]["api_key"],
    base_url="https://api.aimlapi.com/v1"
)

# Initialize Streamlit session state for user input and model selection
if "user_question" not in st.session_state:
    st.session_state.user_question = ""
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "o1-preview"  # Default to o1-preview

def generate_code(user_question, language, model_instance):
    # Step 1: Use the Llama model to process the user's question
    processed_string = llama_model.process_question(user_question)

    # Step 2: Use the selected OpenAI model to generate optimized code
    instruction = (
        f"As a highly skilled software engineer, please analyze the following question thoroughly and provide optimized "
        f"{language} code for the problem: {processed_string}. Make sure to give only code."
    )
    
    # Generate code using the selected model instance
    code = model_instance.generate_code(instruction)
    return code

def explain_code(code, model_instance):
    # Step 1: Use OpenAI model to explain the generated code line by line
    instruction = (
        f"As a highly skilled software engineer, please provide a detailed line-by-line explanation of the following code:\n\n"
        f"{code}\n\nMake sure to explain what each line does and why it is used."
    )
    
    # Explain code using the selected model instance
    explanation = model_instance.explain_code(instruction)
    return explanation

# Function to simulate typing animation for the welcome message
def typing_animation(text, delay=0.05):
    typed_text = ""
    for char in text:
        typed_text += char
        st.markdown(f"<h4 style='color: #4CAF50;'>{typed_text}</h4>", unsafe_allow_html=True)
        time.sleep(delay)
        st.experimental_rerun()
    return typed_text

# List of welcome messages
welcome_messages = [
    "Welcome, how can I assist you?",
    "What can I help with?",
    "Feel free to ask any coding questions!",
    "I'm here to help with your programming needs.",
    "How may I support you today?",
]

# Streamlit app setup
st.set_page_config(page_title="Optimized Code Generator", layout="wide")

# Create a sidebar layout for inputs
st.sidebar.title("Input Section")

# Sidebar inputs
languages = ["Python", "Java", "C++", "JavaScript", "Go", "Ruby", "Swift"]
language = st.sidebar.selectbox("Select Programming Language:", options=languages, index=0)

# Model selection dropdown with session state handling
models = ["o1-preview", "o1-mini"]
st.session_state.selected_model = st.sidebar.selectbox(
    "Select Model:", 
    options=models, 
    index=models.index(st.session_state.selected_model)
)

# Select the appropriate model instance based on user selection
if st.session_state.selected_model == "o1-mini":
    selected_model_instance = o1_mini_model
else:
    selected_model_instance = o1_preview_model

# Main area for the welcome message and generated code
st.subheader("Welcome to the Code Optimizer")

# Display the welcome messages
welcome_container = st.empty()
for message in welcome_messages:
    welcome_container.markdown(f"<h4 style='color: #4CAF50;'>{message}</h4>", unsafe_allow_html=True)
    time.sleep(1.5)  # Wait before displaying the next message

# Display selected model separately
model_response_container = st.empty()
model_response_container.markdown(f"<h5 style='color: #4CAF50;'>Selected Model: {st.session_state.selected_model}</h5>", unsafe_allow_html=True)

# Create a placeholder for the generated code
code_container = st.empty()

# Use a container to allow scrolling
with st.container():
    # Create a placeholder for the input field at the bottom
    user_question = st.text_area("Enter your question:", placeholder="Type your question here...", height=150)
    
    # Submit button at the bottom of the main content
    if st.button("Submit"):
        st.session_state.user_question = user_question  # Store the question in session state
        with st.spinner("Thinking..."):
            code = generate_code(st.session_state.user_question, language, selected_model_instance)
            explanation = explain_code(code, selected_model_instance)  # Get explanation using selected model
            
            # Display the generated code
            code_container.code(code, language=language.lower())
            
            # Set the explanation output in the sidebar
            st.sidebar.text_area("Code Explanation:", value=explanation, height=200, disabled=True)

# Custom CSS to enhance the UI
st.markdown("""
<style>
    .streamlit-expanderHeader {
        font-size: 18px;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #4CAF50; /* Green */
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
    }
    .stTextInput, .stSelectbox, .stTextArea {
        width: 100%;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)
