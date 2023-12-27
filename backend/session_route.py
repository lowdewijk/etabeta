from fastapi import APIRouter, HTTPException
from sessions import sessions
from session import Message

router = APIRouter()

@router.get("/api/session/{session_id}/messages")
def read_messages(session_id: str):
    session = sessions.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")
    sessions.save()
    return {"session_id": session_id, "messages": session.get_messages()}

@router.post("/api/session/{session_id}/send_message")
def send_message(session_id: str, message: Message):
    print(f"Received message: {message.message} from {message.username}")

    session = sessions.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    session.add_message(message)
    sessions.save()

    return {"session_id": session_id}

