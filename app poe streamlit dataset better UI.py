from openai import OpenAI
import streamlit as st
import base64
import os
import requests
import time

XAI_API_KEY = os.getenv("XAI_API_KEY")
client = OpenAI(
    api_key="xai-fKaj18ViSWUs3LASpFkv15or1dVRG5atODuiO0ktpdL8rOgnC6xCXHDAluZEXv5r1yv31JAlNsQL4Dhc",
    base_url="https://api.x.ai/v1",
)


def encode_image_from_url(image_url):
    response = requests.get(image_url)
    return base64.b64encode(response.content).decode('utf-8')

# Create a sidebar
st.sidebar.header("Settings")

# Add sidebar content
st.sidebar.text("Adjust your settings below:")
dataset_path1 = st.sidebar.text_input("Enter path to first local dataset:", r"d:\backup hd 3\mtrkd\rkddotai\dataset1.txt")
weight1 = st.sidebar.number_input("Weight for first dataset:", min_value=0.0, max_value=1.0, value=0.5, step=0.1)

dataset_path2 = st.sidebar.text_input("Enter path to second local dataset:", r"d:\backup hd 3\mtrkd\rkddotai\dataset2.txt")
weight2 = st.sidebar.number_input("Weight for second dataset:", min_value=0.0, max_value=1.0, value=0.5, step=0.1)

# Big title image 
title_image_url = r".\nfts\logo pvw.png"
st.image(title_image_url, use_container_width=True)

# New header text
st.markdown("<h2 style='text-align: center;'>AI for EVM and Bitcoin</h2>", unsafe_allow_html=True)

# Personality images and descriptions
personalities = {
    1: {"image_path": r".\nfts\25.jpg", "description": "the strategist - master of tactics and cunning"},
    2: {"image_path": r".\nfts\60.jpg", "description": "the adventurer - loves exploration and thrill"},
    3: {"image_path": r".\nfts\83.jpg", "description": "the sage - wise and knowledgeable, often philosophical"},
    4: {"image_path": r".\nfts\184.jpg", "description": "the warrior - bravery and combat expertise"},
    5: {"image_path": r".\nfts\btc 33.png", "description": "the trickster - loves to play pranks and twist words"},
    6: {"image_path": r".\nfts\btc 75.png", "description": "the rebel - always pushing boundaries, never one to conform"},
    7: {"image_path": r".\nfts\btc 293.png", "description": "the seducer - charms everyone with their wit and allure"},
    8: {"image_path": r".\nfts\btc 264.png", "description": "the jester - life of the party, laughter is their weapon"}
}

# Display personalities in two rows
st.subheader("Select Your Agent")
current_personality = st.session_state.get('current_personality', 1)

# First row
cols_row1 = st.columns(4)
for idx in range(1, 5):
    with cols_row1[idx - 1]:
        if st.button(f"Select {idx}", key=f"personality_{idx}"):
            st.session_state['current_personality'] = idx
        with st.container():
            st.image(personalities[idx]['image_path'], width=100, use_container_width=True)
            st.caption(personalities[idx]['description'])

# Second row
cols_row2 = st.columns(4)
for idx in range(5, 9):
    with cols_row2[idx - 5]:
        if st.button(f"Select {idx}", key=f"personality_{idx}"):
            st.session_state['current_personality'] = idx
        with st.container():
            st.image(personalities[idx]['image_path'], width=100, use_container_width=True)
            st.caption(personalities[idx]['description'])

# Profile pictures
user_avatar_url = r".\nfts\iggy btc pfp 3.png"
ai_avatar_url = personalities[current_personality]['image_path']

# Customizable URLs for multiple images
st.subheader("Image Inputs")
cols = st.columns(3)
image_urls = []

for i, col in enumerate(cols):
    url = col.text_input(f"Enter image URL {i + 1}:",
                         "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/2694490/ss_1650127faf0b8a9aafed90f8ecd909d677e12c3d.600x338.jpg?t=1733510079" if i == 0 else
                         "https://preview.redd.it/poe-and-poe-2-new-ui-idea-v0-rowea8vnum8c1.png?width=1918&format=png&auto=webp&s=7fcc1c87f7845c9b68878ae3455cf4e3da72b126" if i == 1 else
                         "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/2694490/ss_2f4e929d04f39cda41c4bed0494d913001f97976.600x338.jpg?t=1733510079")
    image_urls.append(url)

    if url:
        try:
            col.image(url, caption=f"Preview {i + 1}", use_container_width=True)
        except Exception as e:
            col.write(f"Error loading image {i + 1}: {str(e)}")
    else:
        col.write(f"No preview for image {i + 1}")

# Load context from datasets
context1 = ""
context2 = ""
dataset_status = ""
if dataset_path1:
    try:
        with open(dataset_path1, 'r', encoding='utf-8') as file:
            context1 = file.read().strip()
        dataset_status += "First dataset loaded successfully.\n"
    except Exception as e:
        dataset_status += f"Error loading first dataset: {str(e)}\n"

if dataset_path2:
    try:
        with open(dataset_path2, 'r', encoding='utf-8') as file:
            context2 = file.read().strip()
        dataset_status += "Second dataset loaded successfully.\n"
    except Exception as e:
        dataset_status += f"Error loading second dataset: {str(e)}\n"

# Display dataset status in the sidebar at the bottom
st.sidebar.text_area("Dataset Status", dataset_status, height=150)

# Combine contexts with weights
total_weight = weight1 + weight2
if total_weight > 0:
    combined_context = f"{context1 * int(weight1 * 10)}\n{context2 * int(weight2 * 10)}"
else:
    combined_context = ""

# Encode images
base64_images = [encode_image_from_url(url) for url in image_urls if url]

# Initialize chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for chat in st.session_state.chat_history:
    if chat['role'] == 'user':
        st.markdown(f"**You:** {chat['content']}")
    else:
        st.markdown(f"**MTRKD:** {chat['content']}")

# Fixed input area at the bottom of the page
# Custom CSS for fixed bottom bar
st.markdown("""
<style>
.fixed-bottom-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: #f4f4f4;
    padding: 10px;
    border-top: 1px solid #e0e0e0;
    z-index: 1000;
    display: flex;
    align-items: center;
}
.fixed-bottom-bar img {
    width: 50px;
    height: 50px;
    margin-right: 10px;
}
.fixed-bottom-bar input[type="text"] {
    flex-grow: 1;
    margin-right: 10px;
}
.fixed-bottom-bar button {
    margin-left: 10px;
}
</style>
""", unsafe_allow_html=True)

# Fixed input area at the bottom of the page
st.markdown('<div class="fixed-bottom-bar">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 10])
with col1:
    st.image(user_avatar_url, width=50, use_container_width=False)
with col2:
    user_query = st.text_input("", placeholder="Enter your query about the images or your dataset:", key="user_query")
    if st.button("Analyze", key="analyze_button"):
        if user_query:
            # Store user message
            st.session_state.chat_history.append({"role": "user", "content": user_query})

            # Display selected personality
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

            # Add images as separate messages
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

                # Store AI response
                ai_response = response.choices[0].message.content
                st.session_state.chat_history.append({"role": "ai", "content": ai_response})

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
st.markdown('</div>', unsafe_allow_html=True)

# Your existing code for displaying chat history would go here, before the fixed bottom bar
for chat in st.session_state.chat_history:
    if chat['role'] == 'user':
        st.markdown(f"**You:** {chat['content']}")
    else:
        st.markdown(f"**MTRKD:** {chat['content']}")