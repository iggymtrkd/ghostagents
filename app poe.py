from openai import OpenAI
from langchain_xai import ChatXAI
import streamlit as st
import base64
import os
import requests

# API Key for OpenAI client (using environment variable for security)
XAI_API_KEY = os.getenv("XAI_API_KEY")
client = OpenAI(api_key="xai-fKaj18ViSWUs3LASpFkv15or1dVRG5atODuiO0ktpdL8rOgnC6xCXHDAluZEXv5r1yv31JAlNsQL4Dhc", base_url="https://api.x.ai/v1")


# Function to encode image from URL to base64
def encode_image_from_url(image_url):
    response = requests.get(image_url)
    return base64.b64encode(response.content).decode('utf-8')

# Example URLs for multiple images
IMAGE_URLS = [
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQw6sbPwVJVtfoz04hhk2nLr2hc57YHbW9-1g&s",
    "https://preview.redd.it/poe-and-poe-2-new-ui-idea-v0-rowea8vnum8c1.png?width=1918&format=png&auto=webp&s=7fcc1c87f7845c9b68878ae3455cf4e3da72b126",
    "https://cdn.mobalytics.gg/assets/poe-2/images/guides/ascendancy/Invoker.jpg"
]

# Encode images
base64_images = [encode_image_from_url(url) for url in IMAGE_URLS]

# Combined text and multiple images request
response = client.chat.completions.create(
    model="grok-vision-beta",  # Assuming this model supports vision
    messages=[
        {
            "role": "system",
            "content": "You are a funny but reticent chatbot. Provide a short, witty response based on both the text and all images."
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text", 
                    "text": "Describe the game you see in the pictures and what you can do in it."
                },
            ] + [
                {
                    "type": "image_url", 
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                } for base64_image in base64_images
            ]
        }
    ],
    temperature=0.1,
    stream=True,
)

# Process streaming response
collected_chunks = []
for chunk in response:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end='')
        collected_chunks.append(chunk.choices[0].delta.content)

# Since the response is streamed, you'll need to join all chunks to get the full response
full_response = ''.join(collected_chunks)
print("\nFull response:", full_response)