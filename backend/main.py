from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:4000", # for development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/session/{session_id}")
def read_session(session_id: int):
    return {"session_id": session_id}

class Message(BaseModel):
    message: str
    username: str

@app.post("/api/session/{session_id}")
def write_session(session_id: int, message: Message):
    print(f"Received message: {message.message} from {message.username}")
    return {"session_id": session_id}    