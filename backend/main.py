from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/session/{session_id}")
def read_session(session_id: int):
    return {"session_id": session_id}

class Message(BaseModel):
    message: str
    username: str

@app.post("/session/{session_id}")
def write_session(session_id: int, message: Message):
    print(f"Received message: {message.message} from {message.username}")
    return {"session_id": session_id}    