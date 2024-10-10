import streamlit as st
from together import Together
from openai import OpenAI

# Initialize the clients for the models with API keys from Streamlit secrets
together_client = Together(base_url="https://api.aimlapi.com/v1", api_key=st.secrets["together"]["api_key"])
openai_client = OpenAI(api_key=st.secrets["openai"]["api_key"], base_url="https://api.aimlapi.com")

def generate_code(user_question, language):
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

    # Step 2: Use OpenAI o1 model to generate optimized code
    instruction = (
        f"As a highly skilled software engineer, please analyze the following question thoroughly and provide optimized "
        f"{language} code for the problem: {processed_string}. Make sure to give only code."
    )
    
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

def explain_code(code):
    # Step 1: Use OpenAI o1 model to explain the generated code line by line
    instruction = (
        f"As a highly skilled software engineer, please provide a detailed line-by-line explanation of the following code:\n\n"
        f"{code}\n\nMake sure to explain what each line does and why it is used."
    )
    
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

# Dropdown menu for programming languages
languages = ["Python", "Java", "C++", "JavaScript", "Go", "Ruby", "Swift"]

# Create the Streamlit interface
st.set_page_config(page_title="Optimized Code Generator", layout="wide")

# Create a sidebar layout for inputs
st.sidebar.title("Input Section")

# Sidebar inputs
language = st.sidebar.selectbox("Select Programming Language:", options=languages, index=0)
#explanation_output = st.sidebar.text_area("Code Explanation:", height=200, value="", placeholder="Code explanation will appear here...", disabled=True)

# Main area for generated code and question input
st.subheader("Generated Code:")
code_container = st.empty()  # Placeholder for generated code

# Use a container to allow scrolling



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




with st.container():
    # Create a placeholder for the input field at the bottom
    user_question = st.text_area("Enter your question:", placeholder="Type your question here...", height=150)
    
    # Submit button at the bottom of the main content
    if st.button("Submit"):
        with st.spinner("Thinking..."):
            code = generate_code(user_question, language)
            explanation = explain_code(code)  # Get explanation using O1 model
            
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
