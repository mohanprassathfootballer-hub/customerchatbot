from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.database import (
    initialize_database,
    create_conversation,
    save_message,
    get_messages
)

from backend.chatbot import generate_response


app = FastAPI(
    title="Customer Support Chatbot",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConversationRequest(BaseModel):
    customer_name: str = "Guest"


class ChatRequest(BaseModel):
    conversation_id: int
    message: str


@app.on_event("startup")
def startup():
    initialize_database()


@app.get("/api/health")
def health():
    return {
        "status": "online",
        "service": "Customer Support Chatbot"
    }


@app.post("/api/conversations")
def new_conversation(request: ConversationRequest):

    conversation_id = create_conversation(
        request.customer_name
    )

    return {
        "conversation_id": conversation_id
    }


@app.get("/api/conversations/{conversation_id}")
def conversation_history(conversation_id: int):

    messages = get_messages(conversation_id)

    return {
        "conversation_id": conversation_id,
        "messages": messages
    }


@app.post("/api/chat")
async def chat(request: ChatRequest):

    message = request.message.strip()

    if not message:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    history = get_messages(
        request.conversation_id
    )

    save_message(
        request.conversation_id,
        "user",
        message
    )

    history.append(
        {
            "role": "user",
            "message": message
        }
    )

    try:

        response = await generate_response(history)

    except Exception as error:

        print("Ollama error:", error)

        raise HTTPException(
            status_code=500,
            detail="Unable to connect to Ollama."
        )

    save_message(
        request.conversation_id,
        "assistant",
        response
    )

    return {
        "response": response
    }


BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app.mount(
    "/",
    StaticFiles(
        directory=FRONTEND_DIR,
        html=True
    ),
    name="frontend"
)