# Copyright Volkan Kücükbudak
# Github: https://github.com/volkansah
import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

st.set_page_config(page_title="Gemini AI Chat", layout="wide")

st.title("🤖 Gemini AI Chat Interface by Volkan Sah")
st.markdown("Chat with Google's Gemini AI models. Supports both text and image inputs. Follow me on Github@volkansah for more cool stuff!")

# Sidebar for settings
with st.sidebar:
    api_key = st.text_input("Enter Google AI API Key", type="password")
    model = st.selectbox(
        "Select Model",
        [
            "gemini-1.5-pro",
            "gemini-1.5-pro-vision-latest",
            "gemini-1.0-pro",
            "gemini-1.0-pro-vision-latest"
        ]
    )
    
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    max_tokens = st.slider("Max Tokens", 1, 2048, 1000)
    system_prompt = st.text_area("System Prompt (Optional)")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# File uploader for images
uploaded_file = st.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png"])
uploaded_image = None
if uploaded_file is not None:
    uploaded_image = Image.open(uploaded_file).convert('RGB')
    st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)  # Fixed here

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input and api_key:
    try:
        # Configure the API
        genai.configure(api_key=api_key)
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Prepare the model and content
        model_instance = genai.GenerativeModel(model_name=model)
        
        content = [{"text": user_input}]
        if uploaded_image:
            content.append({"inline_data": {"mime_type": "image/jpeg", "data": uploaded_image}})

        # Generate response
        response = model_instance.generate_content(
            content,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens
            )
        )

        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response.text)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"Error: {str(e)}")

elif not api_key and user_input:
    st.warning("Please enter your API key in the sidebar first.")

# Instructions in the sidebar
with st.sidebar:
    st.markdown("""
    ## 📝 Instructions:
    1. Enter your Google AI API key
    2. Select a model
    3. Adjust temperature and max tokens if needed
    4. Optional: Set a system prompt
    5. Upload an image (optional)
    6. Type your message and press Enter
    """)
