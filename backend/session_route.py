from fastapi import APIRouter, HTTPException
from sessions import sessions
from session import Message
from pydantic import BaseModel
import time
import asyncio

router = APIRouter()

@router.get("/api/session/{session_id}/messages")
def read_messages(session_id: str):
    session = sessions.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")
    return {"session_id": session_id, "messages": session.get_messages()}

@router.get("/api/session/{session_id}/etabeta_messages")
def read_etabeta_messages(session_id: str):
    session = sessions.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")
    return session.get_etabeta_state()


class SendMessage(BaseModel):    
    message: str
    username: str

@router.post("/api/session/{session_id}/send_message")
async def send_message(session_id: str, message: SendMessage):
    print(f"Received message: {message.message} from {message.username}")

    session = sessions.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    store_message = Message(message=message.message, username=message.username, timestamp=time.time_ns() // 1_000_000)
    session.add_message(store_message)
    sessions.save()

    asyncio.create_task(session.query_etabeta())

    return {"session_id": session_id}


