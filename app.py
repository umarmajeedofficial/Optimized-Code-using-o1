# app.py

import streamlit as st
import time
from models import (
    O1PreviewModel,
    O1MiniModel,
    LlamaModel,
    CodeLlama70BModel,
    DeepseekCoder33BModel,
    WizardCoderPython34BModel,
    PhindCodeLlamaV2Model,
    SQLCoder15BModel
)

# Initialize the Llama client
llama_model = LlamaModel(
    api_key=st.secrets["together"]["api_key"],
    base_url="https://api.aimlapi.com/v1"
)

# Initialize the OpenAI clients for both main models
o1_preview_model = O1PreviewModel(
    api_key=st.secrets["openai"]["api_key"],
    base_url="https://api.aimlapi.com"
)

o1_mini_model = O1MiniModel(
    api_key=st.secrets["openai_mini"]["api_key"],
    base_url="https://api.aimlapi.com"
)

# Initialize the comparison models
codellama_70b_model = CodeLlama70BModel(
    api_key=st.secrets["codellama_70b"]["api_key"],
    base_url="https://api.aimlapi.com"
)

deepseek_coder_33b_model = DeepseekCoder33BModel(
    api_key=st.secrets["deepseek_coder_33b"]["api_key"],
    base_url="https://api.aimlapi.com"
)

wizardcoder_python_34b_model = WizardCoderPython34BModel(
    api_key=st.secrets["wizardcoder_python_34b"]["api_key"],
    base_url="https://api.aimlapi.com"
)

phind_codellama_v2_model = PhindCodeLlamaV2Model(
    api_key=st.secrets["phind_codellama_v2"]["api_key"],
    base_url="https://api.aimlapi.com"
)

sqlcoder_15b_model = SQLCoder15BModel(
    api_key=st.secrets["sqlcoder_15b"]["api_key"],
    base_url="https://api.aimlapi.com"
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

# Function to display error messages
def display_error(message):
    st.error(message)

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
selected_model = st.sidebar.selectbox(
    "Select Model:", 
    options=models, 
    index=models.index(st.session_state.selected_model)
)

# Update session state based on selection
st.session_state.selected_model = selected_model

# Comparison checkbox
compare = st.sidebar.checkbox("Compare with another model")

# Comparison model selection
if compare:
    compare_models = [
        "Code Llama (70B)",
        "Deepseek Coder Instruct (33B)",
        "WizardCoder Python v1.0 (34B)",
        "Phind Code LLaMA v2 (34B)",
        "SQLCoder (15B)"
    ]
    compare_model = st.sidebar.selectbox("Compare with", options=["-- Select a model --"] + compare_models, index=0)
else:
    compare_model = None

# Select the appropriate model instance based on user selection
if st.session_state.selected_model == "o1-mini":
    selected_model_instance = o1_mini_model
else:
    selected_model_instance = o1_preview_model

# Select the appropriate comparison model instance
if compare and compare_model and compare_model != "-- Select a model --":
    if compare_model == "Code Llama (70B)":
        compare_model_instance = codellama_70b_model
    elif compare_model == "Deepseek Coder Instruct (33B)":
        compare_model_instance = deepseek_coder_33b_model
    elif compare_model == "WizardCoder Python v1.0 (34B)":
        compare_model_instance = wizardcoder_python_34b_model
    elif compare_model == "Phind Code LLaMA v2 (34B)":
        compare_model_instance = phind_codellama_v2_model
    elif compare_model == "SQLCoder (15B)":
        compare_model_instance = sqlcoder_15b_model
    else:
        compare_model_instance = None
else:
    compare_model_instance = None

# Main area for the welcome message and generated code
st.subheader("Welcome to the Code Optimizer")
welcome_container = st.empty()  # Placeholder for the welcome message

# Display the welcome messages
for message in welcome_messages:
    welcome_container.markdown(f"<h4 style='color: #4CAF50;'>{message}</h4>", unsafe_allow_html=True)
    time.sleep(1.5)  # Wait before displaying the next message

# Display selected model separately
model_response_container = st.empty()
model_response_container.markdown(f"<h5 style='color: #4CAF50;'>Selected Model: {st.session_state.selected_model}</h5>", unsafe_allow_html=True)

# Create placeholders for the generated code and comparison
code_container = st.empty()
compare_code_container = st.empty()

# Use a container to allow scrolling
with st.container():
    # Create a placeholder for the input field at the bottom
    user_question = st.text_area("Enter your question:", placeholder="Type your question here...", height=150)
    
    # Submit button at the bottom of the main content
    if st.button("Submit"):
        st.session_state.user_question = user_question  # Store the question in session state
        with st.spinner("Thinking..."):
            # Generate code and explanation for the main model
            code = generate_code(st.session_state.user_question, language, selected_model_instance)
            explanation = explain_code(code, selected_model_instance)  # Get explanation using selected model
            
            # Check if an error occurred during code generation
            if code.startswith("Error"):
                display_error(code)
            else:
                # If comparison is enabled and a model is selected
                if compare and compare_model_instance:
                    # Generate code and explanation for the comparison model
                    compare_code = generate_code(st.session_state.user_question, language, compare_model_instance)
                    compare_explanation = explain_code(compare_code, compare_model_instance)
                    
                    # Check if an error occurred during comparison model generation
                    if compare_code.startswith("Error"):
                        display_error(compare_code)
                    else:
                        # Create two columns for side-by-side display
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader(f"Output from {st.session_state.selected_model}")
                            st.code(code, language=language.lower())
                            st.text_area("Explanation:", value=explanation, height=200, disabled=True)
                        
                        with col2:
                            st.subheader(f"Output from {compare_model}")
                            st.code(compare_code, language=language.lower())
                            st.text_area("Explanation:", value=compare_explanation, height=200, disabled=True)
                else:
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
