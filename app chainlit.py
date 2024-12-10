import os
import chainlit as cl
from openai import AsyncOpenAI

XAI_API_KEY = os.getenv("XAI_API_KEY")
client = AsyncOpenAI(
    api_key="xai-fKaj18ViSWUs3LASpFkv15or1dVRG5atODuiO0ktpdL8rOgnC6xCXHDAluZEXv5r1yv31JAlNsQL4Dhc",
    base_url="https://api.x.ai/v1",
)

settings = {
    "model": "grok-beta",
    "temperature": 0.7,
    "max_tokens": 500,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}

@cl.on_chat_start
def start_chat():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are Grok, a helpful chatbot."}],
    )

@cl.on_message
async def main(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")

    try:
        stream = await client.chat.completions.create(
            messages=message_history, 
            stream=True, 
            **settings
        )

        async for part in stream:
            if token := part.choices[0].delta.content or "":
                await msg.stream_token(token)

        message_history.append({"role": "assistant", "content": msg.content})
        await msg.update()
        
    except Exception as e:
        await msg.update(content=f"Error: {str(e)}")
