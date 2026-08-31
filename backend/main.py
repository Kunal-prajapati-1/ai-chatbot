from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


api_key = os.getenv("NVIDIA_API_KEY")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)


@app.get("/")
def root():
    return {
        "message": "Chatbot API is running"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    response = client.chat.completions.create(
        model="nvidia/nemotron-3.5-lightning-30b-a3b",
        messages=[
            {
            "role": "system",
            "content": "Answer the user's question clearly and concisely. Keep the final answer within 60 words. Do not include reasoning, analysis, or thinking steps."
            },
            {
                "role": "user",
                "content": request.message
            }
        ],
        temperature=0.7,
        max_tokens=100,
        extra_body={
        "chat_template_kwargs": {
            "thinking": False
        }
    },
        stream=False
    )

    answer = response.choices[0].message.content

    return {
        "response": answer
    }