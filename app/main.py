import os
from openai import OpenAI
from typing import Optional, List, Literal
from pydantic import BaseModel, Field

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000', 'https://7110.github.io/'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MODEL = 'gpt-4.1-mini'

@app.get('/')
def read_root():
    return {'message': 'Hello, Oshi-ben 👩'}

class RequestMessage(BaseModel):
    message: str
    role: Literal['user', 'system']

class ResponseMessage(BaseModel):
    message: str

class SingleChatRequest(RequestMessage):
    system_prompt: Optional[str] = Field(default=None)

class SingleChatResponse(ResponseMessage):
    pass


@app.post('/v1/single-chat')
def single_chat_with_openai(payload: SingleChatRequest):
    client = OpenAI(api_key=OPENAI_API_KEY)

    messages = []
    if payload.system_prompt:
        messages.append({'role': 'system', 'content': payload.system_prompt})

    messages.append({'role': payload.role, 'content': payload.message})

    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=messages,
        response_format=SingleChatResponse,
    )

    parsed_message = completion.choices[0].message.parsed

    return parsed_message

class ConversationResponseMessage(ResponseMessage):
    tips: Optional[str] = Field(default=None)

class ConversationRequest(BaseModel):
    system_prompt: Optional[str] = Field(default=None)
    messages: List[RequestMessage]

@app.post('/v1/conversation')
def conversation_with_openai(payload: ConversationRequest):
    client = OpenAI(api_key=OPENAI_API_KEY)

    messages = []
    if payload.system_prompt:
        messages.append({'role': 'system', 'content': payload.system_prompt})

    # ここを修正：payload.messages をそのまま messages に使う
    for msg in payload.messages:
        messages.append({'role': msg.role, 'content': msg.message})

    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=messages,
        response_format=ConversationResponseMessage,
    )

    parsed_message = completion.choices[0].message.parsed

    return parsed_message
