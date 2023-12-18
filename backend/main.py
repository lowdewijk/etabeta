from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException


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

class Message(BaseModel):    
    message: str
    username: str

class Session():
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.messages = []

    def add_message(self, message: Message):
        self.messages.append(message)

    def get_messages(self):
        return self.messages

    def get_session_id(self):
        return self.session_id

sessions = {}

class CreateSession(BaseModel):    
    sessionID: str

@app.post("/api/session/")
def create_session(session: CreateSession):
    session_id = session.sessionID
    if session_id not in sessions:
        sessions[session_id] = Session(session.sessionID)
    else:
        raise HTTPException(status_code=400, detail=f"Session '{session_id}' already exists.")

    print(f"Session '{session_id}' created")
    return {"session_id": session_id}    

@app.delete("/api/session/{session_id}")
def delete_session(session_id: str):
    print(f"Session '{session_id}' deleted")

    if session_id in sessions:
        del sessions[session_id]
    else:
        raise HTTPException(status_code=404, detail="Session not found")

    return {"session_id": session_id}

@app.get("/api/session/")
def list_sessions():
    sessions_list = [{"id": id} for id in sessions.keys()]
    return sessions_list

@app.get("/api/session/{session_id}/messages")
def read_messages(session_id: str):
    session = sessions.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"session_id": session_id, "messages": session.get_messages()}

@app.post("/api/session/{session_id}/send")
def send_message(session_id: str, message: Message):
    print(f"Received message: {message.message} from {message.username}")

    if session_id not in sessions:
        sessions[session_id] = Session(session_id)
    sessions[session_id].add_message(message)

    return {"session_id": session_id}

