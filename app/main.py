import os
from openai import OpenAI
from typing import Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MODEL = 'gpt-4.1-mini'

@app.get('/')
def read_root():
    return {'message': 'Hello, Oshi-ben 👩'}

class SingleChatRequest(BaseModel):
    system_prompt: Optional[str] = Field(default=None)
    message: str

class SingleChatResponse(BaseModel):
    message: str = Field(..., description='可愛い口調で返答する。')


@app.post('/v1/single-chat')
def single_chat_with_openai(payload: SingleChatRequest):
    client = OpenAI(api_key=OPENAI_API_KEY)

    messages = []
    if payload.system_prompt:
        messages.append({'role': 'system', 'content': payload.system_prompt})

    messages.append({'role': 'user', 'content': payload.message})

    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=messages,
        response_format=SingleChatResponse,
    )

    parsed_message = completion.choices[0].message.parsed

    return parsed_message
