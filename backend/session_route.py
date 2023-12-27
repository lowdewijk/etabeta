from fastapi import APIRouter, HTTPException
from sessions import sessions
from session import Message
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
    return {"session_id": session_id, "messages": session.get_etabeta_messages()}

@router.post("/api/session/{session_id}/send_message")
async def send_message(session_id: str, message: Message):
    print(f"Received message: {message.message} from {message.username}")

    session = sessions.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    session.add_message(message)
    sessions.save()

    asyncio.create_task(session.query_etabeta())

    return {"session_id": session_id}


