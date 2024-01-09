from fastapi import APIRouter, HTTPException
from UserError import UserError
from sessions import sessions
from session import Message, SessionState
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

    if len(message.message) == 0:
        return 

    session = sessions.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    if message.message.startswith("/topic"):
        margs = message.message.split(" ")
        if len(margs) == 2:
            raise UserError(message.username, "Invalid number of arguments for command /topic. Expected >1.")
        session.set_topic(message.username, margs[1])
        sessions.save()
        return

    if message.message.startswith("/start"):
        session.set_state(message.username, SessionState.DEBATING)
        sessions.save()
        return

    if message.message.startswith("/pause"):
        session.set_state(message.username, SessionState.PAUSED)
        sessions.save()
        return

    store_message = Message(
        message=message.message,
        username=message.username,
        timestamp=time.time_ns() // 1_000_000,
    )
    session.add_message(store_message)
    sessions.save()

    if session.get_state() == SessionState.DEBATING:
        asyncio.create_task(session.query_etabeta())
