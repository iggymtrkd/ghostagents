from langchain_xai import ChatXAI
import streamlit as st
import base64
import os
import requests
import time

# API Key for xAI client (using environment variable for security)
XAI_API_KEY = os.getenv("XAI_API_KEY")
client = ChatXAI(api_key="xai-fKaj18ViSWUs3LASpFkv15or1dVRG5atODuiO0ktpdL8rOgnC6xCXHDAluZEXv5r1yv31JAlNsQL4Dhc", base_url="https://api.x.ai/v1")

# Function to encode image from URL to base64
def encode_image_from_url(image_url):
    response = requests.get(image_url)
    return base64.b64encode(response.content).decode('utf-8')

# Streamlit UI
st.markdown("<h1 style='text-align: center;'>AI Image and Text Analysis</h1>", unsafe_allow_html=True)

# Big title image 
title_image_url = "https://www.creativefabrica.com/wp-content/uploads/2019/02/10-Arcade-Game-Title-style-for-AI-by-anomali.bisu_-580x387.jpg"
st.image(title_image_url, use_container_width=True)

# Profile pictures
user_avatar_url = "https://clipart-library.com/8300/1931/crowd-clipart-xl.png"  
ai_avatar_url = "https://clipart-library.com/8300/1931/person-standing-emoji-clipart-sm.png"  

# Customizable URLs for multiple images
st.subheader("Image Inputs")
cols = st.columns(3)
IMAGE_URLS = []
for i, col in enumerate(cols):
    url = col.text_input(f"Enter Image URL {i+1}:", f"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQw6sbPwVJVtfoz04hhk2nLr2hc57YHbW9-1g&s" if i == 0 else f"https://preview.redd.it/poe-and-poe-2-new-ui-idea-v0-rowea8vnum8c1.png?width=1918&format=png&auto=webp&s=7fcc1c87f7845c9b68878ae3455cf4e3da72b126" if i == 1 else "https://cdn.mobalytics.gg/assets/poe-2/images/guides/ascendancy/Invoker.jpg")
    IMAGE_URLS.append(url)
    if url:
        try:
            col.image(url, caption=f"Preview {i+1}", use_container_width=True)
        except Exception as e:
            col.write(f"Error loading image {i+1}: {str(e)}")
    else:
        col.write(f"No preview for Image {i+1}")

# Add a field for local dataset path
dataset_path = st.text_input("Enter path to your local dataset:", r"D:\Backup HD 3\MTRKD\RKDdotAI\dataset.txt")

# Load context from file
context = ""
if dataset_path:
    try:
        with open(dataset_path, 'r', encoding='utf-8') as file:
            context = file.read().strip()
        st.success("Context loaded successfully.")
    except Exception as e:
        st.error(f"Error loading context: {str(e)}")

# Encode images
base64_images = [encode_image_from_url(url) for url in IMAGE_URLS if url]

# User input with avatar and analyze button moved to the right under the prompt
col1, col2 = st.columns([1, 10])
with col1:
    st.image(user_avatar_url, width=25, use_container_width=True)
with col2:
    user_query = st.text_input("", placeholder="Enter your query:", key="user_query")
    if st.button("Analyze", key="analyze_button"):
        st.session_state['analyze'] = True
    if user_query and st.session_state.get('user_query_prev', '') != user_query:
        st.session_state['analyze'] = True
        st.session_state['user_query_prev'] = user_query

if 'analyze' in st.session_state and st.session_state['analyze']:
    st.session_state['analyze'] = False  # Reset the trigger
    
    messages = [
        {
            "role": "system",
            "content": "You are a chatbot. Answer based on the context provided and the user's query."
        },
        {
            "role": "user",
            "content": f"{user_query}. Context: {context}"
        }
    ]

    try:
        # Assuming 'create' is the correct method name
        response = client.create(
            model="grok-beta",  # Use the correct model name
            messages=messages,
            temperature=0.1,
            stream=True,
        )
        
        # Containers for displaying messages
        ai_message = st.container()

        # AI response with streaming, avatar, and loading animation
        with ai_message:
            col1, col2 = st.columns([10, 1])
            with col1:
                loading_placeholder = st.empty()
                message_placeholder = st.empty()
                full_response = ""
                
                # Display loading text with animation
                loading_text = "Loading"
                for i in range(5):
                    loading_placeholder.markdown(f"**MTRKD:** {loading_text + '.' * (i % 4)}")
                    time.sleep(0.5)
                
                for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(f"**MTRKD:** {full_response}")
                        if i == 0:  # Only clear once
                            loading_placeholder.empty()
                            i += 1
                message_placeholder.markdown(f"**MTRKD:** {full_response}")
            with col2:
                st.image(ai_avatar_url, width=25, use_container_width=True)
    except AttributeError:
        st.error("The method to create completions is not available. Please check your ChatXAI setup.")
    except Exception as e:
        st.error(f"An error occurred while generating AI response: {str(e)}")