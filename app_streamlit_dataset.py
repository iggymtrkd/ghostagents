from openai import OpenAI
import streamlit as st
import base64
import os
import requests
import time

st.set_page_config(
    page_title="Ghost Agents",
    page_icon=":ghost:"  # 'path/to/your_icon.png'
)

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.x.ai/v1",
)

def encode_image_from_url(image_url):
    response = requests.get(image_url)
    return base64.b64encode(response.content).decode('utf-8')

# Big title image 
title_image_url = "NFTs/logo pvw.png"
st.image(title_image_url, use_container_width=True)

# New header text
st.markdown("<h2 style='text-align: center;'>Ghost Agents</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Blockchain Gaming AI Companion Agents</h3>", unsafe_allow_html=True)
#st.markdown("<h3 style='text-align: center;'>True Ownership. For EVM and Bitcoin</h3>", unsafe_allow_html=True)

# Personality Images and Descriptions
personalities = {
    1: {"image_path": "NFTs/25.jpg", "description": "The Strategist - Master of tactics and cunning"},
    2: {"image_path": "NFTs/60.jpg", "description": "The Adventurer - Loves exploration and thrill"},
    3: {"image_path": "NFTs/83.jpg", "description": "The Sage - Wise and knowledgeable, often philosophical"},
    4: {"image_path": "NFTs/184.jpg", "description": "The Warrior - Bravery and combat expertise"}
    #5: {"image_path": "NFTs/btc 33.png", "description": "The Trickster - Loves to play pranks and twist words"},
    #6: {"image_path": "NFTs/btc 75.png", "description": "The Rebel - Always pushing boundaries, never one to conform"},
    #7: {"image_path": "NFTs/btc 293.png", "description": "The Seducer - Charms everyone with their wit and allure"},
    #8: {"image_path": "NFTs/btc 264.png", "description": "The Jester - Life of the party, laughter is their weapon"}
}

# Display personalities in two rows
st.subheader("Select Your Agent")
current_personality = st.session_state.get('current_personality', 1)
# First Row
cols_row1 = st.columns(4)
for idx in range(1, 5):
    with cols_row1[idx - 1]:
        if st.button(f"Select {idx}", key=f"personality_{idx}"):
            st.session_state['current_personality'] = idx
        with st.container():
            st.image(personalities[idx]['image_path'], width=100, use_container_width=True)
            st.caption(personalities[idx]['description'])

# Second Row
#cols_row2 = st.columns(4)
#for idx in range(5, 9):
#    with cols_row2[idx - 5]:
#        if st.button(f"Select {idx}", key=f"personality_{idx}"):
#           st.session_state['current_personality'] = idx
#        with st.container():
#            st.image(personalities[idx]['image_path'], width=100, use_container_width=True)
#            st.caption(personalities[idx]['description'])

# Profile pictures
user_avatar_url = r"NFTs/iggy BTC PFP 3.png"
ai_avatar_url = personalities[current_personality]['image_path']

# Customizable URLs for multiple images
with st.expander("Add extra context with pictures", expanded=False):  # Set expanded=True to open by default
    st.subheader("Image links")
    cols = st.columns(3)
    IMAGE_URLS = []

    for i, col in enumerate(cols):
        url = col.text_input(
            f"Enter Image URL {i+1}:",
            "https://i.imgur.com/3AgdEXo.png" if i == 0 else
            "https://i.imgur.com/aPZoxnI.png" if i == 1 else
            "https://i.imgur.com/EyBfbcb.png"
        )
        IMAGE_URLS.append(url)

        if url:
            try:
                col.image(url, caption=f"Preview {i+1}", use_container_width=True)
            except Exception as e:
                col.write(f"Error loading image {i+1}: {str(e)}")
        else:
            col.write(f"No preview for Image {i+1}")


# Add fields for two local dataset paths with weights
dataset_path1 = "dataset1gf.txt"  # Fixed path for the first dataset
dataset_path2 = "dataset2gf.txt"  # Fixed path for the second dataset
weight1 = 0.75  # Fixed weight for the first dataset
weight2 = 0.25  # Fixed weight for the second dataset

context1 = ""
context2 = ""
if dataset_path1:
    try:
        with open(dataset_path1, 'r', encoding='utf-8') as file:
            context1 = file.read().strip()
    except Exception as e:
        st.error(f"Error loading game dataset: {str(e)}")

if dataset_path2:
    try:
        with open(dataset_path2, 'r', encoding='utf-8') as file:
            context2 = file.read().strip()
    except Exception as e:
        st.error(f"Error loading second dataset: {str(e)}")

# Combine contexts with weights
total_weight = weight1 + weight2
if total_weight > 0:
    combined_context = f"{context1 * int(weight1 * 10)}\n{context2 * int(weight2 * 10)}"
else:
    combined_context = ""


# Encode images
base64_images = [encode_image_from_url(url) for url in IMAGE_URLS if url]

# User input with avatar and analyze button
col1, col2 = st.columns([1, 10])
with col1:
    st.image(user_avatar_url, width=50, use_container_width=True)
with col2:
    user_query = st.text_input("", placeholder="Enter your query about the images or your dataset:", key="user_query")
    if st.button("Analyze", key="analyze_button"):
        st.session_state['analyze'] = True
    if user_query and st.session_state.get('user_query_prev', '') != user_query:
        st.session_state['analyze'] = True
        st.session_state['user_query_prev'] = user_query

if 'analyze' in st.session_state and st.session_state['analyze']:
    st.session_state['analyze'] = False

    # Display which personality is selected
    selected_personality = personalities[current_personality]['description']
    st.write(f"**Selected Personality:** {selected_personality}")

    personality = personalities[current_personality]['description']
    system_message = {
        "role": "system",
        "content": f"You are {personality}. Provide a short, witty response based on both the text, images, and the provided context from the datasets."
    }
    
    text_message = {
        "role": "user",
        "content": f"{user_query}. Context: {combined_context}. Here are {len(base64_images)} images for additional context:"
    }
    messages = [system_message, text_message]

    # Add images as separate messages but reference them in the text message
    for base64_image in base64_images:
        messages.append({
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        })

    try:
        with st.spinner('Got it, just a moment...'):
            response = client.chat.completions.create(
                model="grok-vision-beta",
                messages=messages
            )

        ai_message = st.container()
        with ai_message:
            col1, col2 = st.columns([9, 2])
            with col1:
                message_placeholder = st.empty()
                message_placeholder.markdown(f"**MTRKD:** {response.choices[0].message.content}")
            with col2:
                st.image(ai_avatar_url, width=50, use_container_width=True)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 