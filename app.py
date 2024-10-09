import streamlit as st
import time
from together import Together
from openai import OpenAI

# Initialize the clients for the models with API keys from Streamlit secrets
together_client = Together(base_url="https://api.aimlapi.com/v1", api_key=st.secrets["together"]["api_key"])
openai_client = OpenAI(api_key=st.secrets["openai"]["api_key"], base_url="https://api.aimlapi.com")
openai_mini_client = OpenAI(api_key=st.secrets["openai_mini"]["api_key"], base_url="https://api.aimlapi.com")  # Client for o1-mini

def generate_code(user_question, language, model):
    # Step 1: Use Llama model to get the processed question
    response = together_client.chat.completions.create(
        model="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_question,
                    }
                ],
            }
        ],
        max_tokens=10000,
    )
    
    llama_response = response.choices[0].message.content.strip()
    
    # Remove quotes and make it a single string
    processed_string = llama_response.replace('"', '').replace("'", '').replace('\n', ' ')

    # Step 2: Use selected OpenAI model to generate optimized code
    instruction = (
        f"As a highly skilled software engineer, please analyze the following question thoroughly and provide optimized "
        f"{language} code for the problem: {processed_string}. Make sure to give only code."
    )
    
    # Use the selected model
    if model == "o1-mini":
        openai_response = openai_mini_client.chat.completions.create(
            model="o1-mini",
            messages=[
                {
                    "role": "user",
                    "content": instruction
                },
            ],
            max_tokens=10000,
        )
    else:
        openai_response = openai_client.chat.completions.create(
            model="o1-preview",
            messages=[
                {
                    "role": "user",
                    "content": instruction
                },
            ],
            max_tokens=10000,
        )

    code = openai_response.choices[0].message.content.strip()
    return code

def explain_code(code, model):
    # Step 1: Use OpenAI model to explain the generated code line by line
    instruction = (
        f"As a highly skilled software engineer, please provide a detailed line-by-line explanation of the following code:\n\n"
        f"{code}\n\nMake sure to explain what each line does and why it is used."
    )
    
    if model == "o1-mini":
        openai_response = openai_mini_client.chat.completions.create(
            model="o1-mini",
            messages=[
                {
                    "role": "user",
                    "content": instruction
                }
            ],
            max_tokens=10000,
        )
    else:
        openai_response = openai_client.chat.completions.create(
            model="o1-preview",
            messages=[
                {
                    "role": "user",
                    "content": instruction
                }
            ],
            max_tokens=10000,
        )

    explanation = openai_response.choices[0].message.content.strip()
    return explanation

# Function to simulate typing animation for the welcome message
def typing_animation(text, delay=0.1):
    for char in text:
        yield char
        time.sleep(delay)

# List of welcome messages
welcome_messages = [
    "Welcome, how can I assist you?",
    "What can I help with?",
    "Feel free to ask any coding questions!",
    "I'm here to help with your programming needs.",
    "How may I support you today?",
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

# Model selection dropdown
models = ["o1-preview", "o1-mini"]
model = st.sidebar.selectbox("Select Model:", options=models, index=0)

# Main area for the welcome message and generated code
st.subheader("Welcome to the Code Optimizer")
welcome_container = st.empty()  # Placeholder for the welcome message

# Cycle through the welcome messages with typing animation
for message in welcome_messages:
    typed_message = ''.join(typing_animation(message))
    welcome_container.markdown(f"<h4 style='color: #4CAF50;'>{typed_message}</h4>", unsafe_allow_html=True)
    time.sleep(1.5)  # Wait before displaying the next message
    # Create a new container for the model response display
    model_response_container = st.empty()

    # Display which model generated the response
    model_response_container.markdown(f"<h5 style='color: #4CAF50;'>Response generated from: {model}</h5>", unsafe_allow_html=True)



# Create a placeholder for the generated code
code_container = st.empty()

# Use a container to allow scrolling
with st.container():
    # Create a placeholder for the input field at the bottom
    user_question = st.text_area("Enter your question:", placeholder="Type your question here...", height=150)
    
    # Submit button at the bottom of the main content
    if st.button("Submit"):
        with st.spinner("Thinking..."):
            code = generate_code(user_question, language, model)
            explanation = explain_code(code, model)  # Get explanation using selected model
            
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
