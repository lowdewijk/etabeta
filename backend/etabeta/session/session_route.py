import logging
from dataclasses import dataclass
from fastapi import APIRouter, HTTPException
from etabeta.session.AIUser import AIUser
from etabeta.common.Message import Message, Username
from etabeta.session.session import SessionState
from etabeta.common.UserError import UserError
from etabeta.common.chat_data import sessions

from pydantic import BaseModel
import time
import asyncio
import shlex

router = APIRouter()
log = logging.getLogger(__name__)


class ReadMessage(BaseModel):
    message: str
    username: str
    # timestamp in ms since epoch
    timestamp: int
    is_private_message: bool


@router.get("/session/{session_id}/messages/{username}")
def read_messages(session_id: str, username: Username):
    session = sessions.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")
    messages = [
        ReadMessage(
            message=msg.message,
            username=msg.username,
            timestamp=msg.timestamp,
            is_private_message=msg.private_message is not None,
        )
        for msg in session.get_messages(username)
    ]
    return {"session_id": session_id, "messages": messages}


@router.get("/session/{session_id}/etabeta_messages")
def read_etabeta_messages(session_id: str):
    session = sessions.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")
    return session.get_etabeta_state()


class SendMessage(BaseModel):
    message: str
    username: Username


@router.post("/session/{session_id}/send_message")
async def send_message(session_id: str, message: SendMessage):
    if len(message.message) == 0:
        return

    session = sessions.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    command = command_parse(message)
    if command is not None:
        log.info(f"Received command: {command} from {message.username}")

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

        if command.cmd == "help":
            session.add_message(
                Message(
                    message="""Commands:                    

| Command     | Arguments     | Description                                                                                                                            |
| ----------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| /topic      | $topic        | Set the topic of the debate to $topic.                                                                                                 |
| /start      |               | Start the debate. The topic must first be set, see /topic.                                                                             |
| /pause      |               | Pause the debate.                                                                                                                      |
| /ai         | $name $prompt | Add an AI user to the room with the given name and prompt. You can use the prompt to tell the AI what to think about the debate topic. | 
| /help       |               | Show this help message.                                                                                                                |

*Note*: Command arguments must be separated by a space. For multi-word arguments, use quotes. For example: /topic "This is a topic".""",
                    username="etabeta",
                    timestamp=time.time_ns() // 1_000_000,
                    private_message=[command.commander],
                )
            )
            sessions.save()
            return

        raise UserError(command.commander, f"Unknown command: {command.cmd}")
    else:
        log.info(f"Received message: {message.message} from {message.username}")

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
    commander: Username
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
