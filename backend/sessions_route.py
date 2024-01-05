from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from session import Session
from sessions import sessions

router = APIRouter()


class CreateSession(BaseModel):
    sessionID: str


@router.post("/api/session/")
def create_session(session: CreateSession):
    session_id = session.sessionID
    if sessions.get_session(session_id) is None:
        sessions.create_session(Session(session_id))
    else:
        raise HTTPException(
            status_code=400, detail=f"Session '{session_id}' already exists."
        )

    print(f"Session '{session_id}' created.")
    sessions.save()

    return {"session_id": session_id}


@router.delete("/api/session/{session_id}")
def delete_session(session_id: str):
    if sessions.get_session(session_id) is not None:
        sessions.delete_session(session_id)
        print(f"Session '{session_id}' deleted.")
    else:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    return {"session_id": session_id}


@router.get("/api/session/")
def list_sessions():
    return [{"id": id} for id in sessions.get_session_ids()]
