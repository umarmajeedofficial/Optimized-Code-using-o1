try:
    from models.o1_preview import O1PreviewModel
    from models.o1_mini import O1MiniModel
    from models.llama import LlamaModel
    from models.deepseek_coder_instruct import DeepseekCoderInstructModel
    from models.gpt4o_model import GPT4oModel  # Updated import
except ImportError as e:
    st.error(f"Error importing models: {e}")
    st.stop()

# Initialize the GPT-4o model
gpt4o_model = GPT4oModel(
    api_key=st.secrets["gpt4o"]["api_key"], 
    base_url="https://api.aimlapi.com"
)

# Initialize the Llama client
llama_model = LlamaModel(
    api_key=st.secrets["together"]["api_key"],
    base_url="https://api.aimlapi.com/v1"
)

# Initialize the OpenAI clients for base models
o1_preview_model = O1PreviewModel(
    api_key=st.secrets["openai"]["api_key"],
    base_url="https://api.aimlapi.com"
)

o1_mini_model = O1MiniModel(
    api_key=st.secrets["openai_mini"]["api_key"],
    base_url="https://api.aimlapi.com"
)

# Initialize the comparison models
deepseek_model = DeepseekCoderInstructModel(
    api_key=st.secrets["deepseek"]["api_key"],
    base_url="https://api.aimlapi.com"
)



# Initialize Streamlit session state for user input and model selection
if "user_question" not in st.session_state:
    st.session_state.user_question = ""
if "selected_base_model" not in st.session_state:
    st.session_state.selected_base_model = "o1-preview"  # Default to o1-preview
if "compare_mode" not in st.session_state:
    st.session_state.compare_mode = False
if "selected_compare_models" not in st.session_state:
    st.session_state.selected_compare_models = []

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

# Base Model Selection
base_models = ["o1-preview", "o1-mini"]
selected_base_model = st.sidebar.selectbox(
    "Select Base Model:", 
    options=base_models, 
    index=base_models.index(st.session_state.selected_base_model)
)
st.session_state.selected_base_model = selected_base_model

# Comparison mode checkbox
compare_mode = st.sidebar.checkbox("Compare with Other Models", key="compare_mode")

# If compare_mode is enabled, show additional model selection
if compare_mode:
    comparison_models = ["deepseek-coder-instruct", "gpt4o"]
    selected_compare_model = st.sidebar.selectbox(
        "Select Model to Compare:", 
        options=comparison_models,
        index=0  # Default to the first model in the list
    )
    st.session_state.selected_compare_models = [selected_compare_model]  # Store the selected model as a list
else:
    st.session_state.selected_compare_models = []


# Function to get model instances based on selection
def get_model_instance(model_name):
    if model_name == "o1-preview":
        return o1_preview_model
    elif model_name == "o1-mini":
        return o1_mini_model
    elif model_name == "deepseek-coder-instruct":
        return deepseek_model
    elif model_name == "gpt4o":
        return gpt4o_model
    else:
        return o1_preview_model  # Default fallback

# Main area for the welcome message and generated code
st.subheader("Welcome to the Code Optimizer")
welcome_container = st.empty()  # Placeholder for the welcome message

# Display the welcome messages
for message in welcome_messages:
    welcome_container.markdown(f"<h4 style='color: #4CAF50;'>{message}</h4>", unsafe_allow_html=True)
    time.sleep(1.5)  # Wait before displaying the next message

# Display selected models information
if compare_mode:
    st.markdown(f"<h5 style='color: #4CAF50;'>Base Model: {st.session_state.selected_base_model}</h5>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='color: #4CAF50;'>Comparison Models: {', '.join(st.session_state.selected_compare_models) if st.session_state.selected_compare_models else 'None'}</h5>", unsafe_allow_html=True)
else:
    st.markdown(f"<h5 style='color: #4CAF50;'>Selected Model: {st.session_state.selected_base_model}</h5>", unsafe_allow_html=True)

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
            results = {}
            # Process Base Model
            base_model_instance = get_model_instance(st.session_state.selected_base_model)
            try:
                base_code = generate_code(st.session_state.user_question, language, base_model_instance)
                base_explanation = explain_code(base_code, base_model_instance)
                results["Base Model"] = {
                    "model_name": st.session_state.selected_base_model,
                    "code": base_code,
                    "explanation": base_explanation
                }
            except Exception as e:
                results["Base Model"] = {
                    "model_name": st.session_state.selected_base_model,
                    "code": "Error generating code.",
                    "explanation": f"Error: {e}"
                }
            
            # Process Comparison Models if enabled
            if compare_mode and st.session_state.selected_compare_models:
                for model_name in st.session_state.selected_compare_models:
                    model_instance = get_model_instance(model_name)
                    try:
                        code = generate_code(st.session_state.user_question, language, model_instance)
                        explanation = explain_code(code, model_instance)
                        results[model_name] = {
                            "model_name": model_name,
                            "code": code,
                            "explanation": explanation
                        }
                    except Exception as e:
                        results[model_name] = {
                            "model_name": model_name,
                            "code": "Error generating code.",
                            "explanation": f"Error: {e}"
                        }
            
            # Display Results
            if compare_mode and st.session_state.selected_compare_models:
                # Include Base Model in the results for display
                display_models = ["Base Model"] + st.session_state.selected_compare_models
            else:
                display_models = ["Base Model"]
            
            # Determine the number of columns based on the number of models to display
            num_models = len(display_models)
            cols = st.columns(num_models)
            
            for idx, model_key in enumerate(display_models):
                with cols[idx]:
                    model_info = results.get(model_key, {})
                    model_display_name = model_info.get("model_name", model_key)
                    st.subheader(f"**{model_display_name}**")
                    st.markdown("**Code:**")
                    st.code(model_info.get("code", "No code generated."), language=language.lower())
                    st.markdown("**Explanation:**")
                    st.text_area("", value=model_info.get("explanation", "No explanation provided."), height=200, disabled=True)

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
