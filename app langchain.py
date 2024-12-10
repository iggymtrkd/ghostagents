from openai import OpenAI
from langchain_xai import ChatXAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import base64
import os
import requests
# API Key for xAI client
XAI_API_KEY = "xai-fKaj18ViSWUs3LASpFkv15or1dVRG5atODuiO0ktpdL8rOgnC6xCXHDAluZEXv5r1yv31JAlNsQL4Dhc"
client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")

# Initialize ChatXAI instead of ChatOpenAI
llm = ChatXAI(api_key=XAI_API_KEY, model_name="grok-beta")  # Adjust model_name to what's available from xAI

# Conversation Memory
memory = ConversationBufferMemory(memory_key="chat_history")

# Custom Prompt for Chain of Thought
prompt_template = PromptTemplate(
    input_variables=["chat_history", "input"],
    template="""Analyze the images and the text input. Think step-by-step:
    1. Identify what game is shown in the images.
    2. Based on the images, describe what features or actions are visible or suggested.
    3. Combine this with the user's question to provide an answer.
    Current conversation: {chat_history}
    User: {input}
    Assistant:""",
)

# Create Conversation Chain with Chain of Thought
conversation = ConversationChain(
    llm=llm, 
    memory=memory, 
    prompt=prompt_template,
    verbose=True  # For debugging
)

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

# Prepare the initial message with images and text
initial_message = {
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

# Run the conversation chain with the initial message
response = conversation.run(initial_message["content"])

# Print the response
print("Full response:", response)

# Additional interaction to showcase memory usage
user_input = "What else can I do in this game?"
response = conversation.run(user_input)
print("Further interaction:", response)