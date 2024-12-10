from openai import OpenAI
from langchain_xai import ChatXAI
import base64
import os

XAI_API_KEY = os.getenv("XAI_API_KEY")
client = OpenAI(api_key="xai-fKaj18ViSWUs3LASpFkv15or1dVRG5atODuiO0ktpdL8rOgnC6xCXHDAluZEXv5r1yv31JAlNsQL4Dhc", base_url="https://api.x.ai/v1")

# Basic Chat

response = client.chat.completions.create(
    model="grok-beta",
    messages=[{"role": "system", "content": "You are Grok, a helpful chatbot."},
              {"role": "user", "content": "Why not tell me about 2024?"}],
    stream=True,
)

for chunk in response:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")




IMAGE_PATH = "25.jpg"

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

base64_image = encode_image(IMAGE_PATH)

response = client.chat.completions.create(
    model="grok-vision-beta",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that responds in Markdown. Help me with my math homework!"},
        {"role": "user", "content": [
            {"type": "text", "text": "What's the area of the triangle?"},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}
            }
        ]}
    ],
    temperature=0.0,
)

print(response.choices[0].message.content)