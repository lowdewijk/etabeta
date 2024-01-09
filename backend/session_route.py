import logging
from attr import dataclass
from fastapi import APIRouter, HTTPException
from UserError import UserError
from sessions import sessions
from session import AIUser, Message, SessionState
from pydantic import BaseModel
import time
import asyncio
import shlex

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
    if len(message.message) == 0:
        return

    session = sessions.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    command = command_parse(message)
    if command is not None:
        logging.info(f"Received command: {command} from {message.username}")

        if command.cmd == "topic":
            if len(command.args) != 1:
                raise UserError(
                    command.commander,
                    "Invalid number of arguments for command /topic. Expected 1.",
                )
            session.set_topic(message.username, " ".join(command.args))
            sessions.save()
            return

        if command.cmd == "start":
            session.set_state(message.username, SessionState.DEBATING)
            sessions.save()
            return

        if command.cmd == "pause":
            session.set_state(message.username, SessionState.PAUSED)
            sessions.save()
            return

        if command.cmd == "ai":
            if len(command.args) != 2:
                raise UserError(
                    command.commander,
                    f"Invalid number of arguments for command /ai. Expected 2, but got {len(command.args)}.",
                )
            session.add_ai_user(
                command.commander, AIUser(command.args[0], command.args[1])
            )
            sessions.save()
            return

        raise UserError(command.commander, f"Unknown command: {command.cmd}")
    else:
        logging.info(f"Received message: {message.message} from {message.username}")

        store_message = Message(
            message=message.message,
            username=message.username,
            timestamp=time.time_ns() // 1_000_000,
        )
        session.add_message(store_message)
        sessions.save()

        if (
            session.get_state() == SessionState.DEBATING
            and message.message.startswith("#") == False
        ):
            asyncio.create_task(session.query_ais())


@dataclass
class Command:
    commander: str
    cmd: str
    args: list[str]


def command_parse(message: SendMessage) -> Command | None:
    commander = message.username
    msg = message.message.lstrip(" ")
    if msg[0].startswith("/") == False:
        return None

    space = msg.find(" ")
    if space == -1:
        cmd = msg[1:]
        return Command(commander, cmd, [])
    else:
        cmd = msg[1:space]
        args = shlex.split(msg[space + 1 :])
        return Command(commander, cmd, args)
