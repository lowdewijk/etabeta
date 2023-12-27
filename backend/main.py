from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
import pickle


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

class Sessions():
    def __init__(self):
        self.sessions = {}

    def create_session(self, session: Session):
        self.sessions[session.get_session_id()] = session

    def get_session(self, session_id: str):
        return self.sessions.get(session_id)

    def delete_session(self, session_id: str):
        del self.sessions[session_id]

    def get_session_ids(self):
        return self.sessions.keys()

    def save(self):
        with open('chat_data/sessions.pickle', 'wb') as handle:
            pickle.dump(self.sessions, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    def load(self):
        try:
            with open('chat_data/sessions.pickle', 'rb') as handle:
                self.sessions = pickle.load(handle)
        except FileNotFoundError:
            return

sessions = Sessions()
sessions.load()

class CreateSession(BaseModel):    
    sessionID: str

@app.post("/api/session/")
def create_session(session: CreateSession):
    session_id = session.sessionID
    if sessions.get_session(session_id) is None:
        sessions.create_session(Session(session_id))
    else:
        raise HTTPException(status_code=400, detail=f"Session '{session_id}' already exists.")

    print(f"Session '{session_id}' created")
    sessions.save()

    return {"session_id": session_id}    

@app.delete("/api/session/{session_id}")
def delete_session(session_id: str):
    print(f"Session '{session_id}' deleted")

    if sessions.get_session(session_id) is None:
        sessions.delete_sessions()
    else:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    return {"session_id": session_id}

@app.get("/api/session/")
def list_sessions():
    return [{"id": id} for id in sessions.get_session_ids()]

@app.get("/api/session/{session_id}/messages")
def read_messages(session_id: str):
    session = sessions.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")
    sessions.save()
    return {"session_id": session_id, "messages": session.get_messages()}

@app.post("/api/session/{session_id}/send_message")
def send_message(session_id: str, message: Message):
    print(f"Received message: {message.message} from {message.username}")

    session = sessions.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    session.add_message(message)
    sessions.save()

    return {"session_id": session_id}

