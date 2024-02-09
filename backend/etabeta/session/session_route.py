import logging
from dataclasses import asdict, dataclass
from fastapi import APIRouter, HTTPException
from etabeta.common.AIUser import AIUser
from etabeta.common.Message import Message, Username
from etabeta.common.User import User
from etabeta.session.Session import SessionState
from etabeta.common.UserError import UserError
from etabeta.common.chat_data import sessions

from pydantic import BaseModel
import time
import asyncio
import shlex

router = APIRouter()
log = logging.getLogger(__name__)

def get_session_or_raise(session_id):
    session = sessions.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")
    return session

@router.get("/session/{session_id}/join/{username}")
def join_session(session_id: str, username: Username) -> None:
    session = get_session_or_raise(session_id)
    session.add_user(User(username))
    sessions.save()

@router.get("/session/{session_id}/leave/{username}")
def leave_session(session_id: str, username: Username) -> None:
    session = get_session_or_raise(session_id)
    session.remove_user(username)
    sessions.save()

class SessionUser(BaseModel):
    username: str
    last_active: int

class ActiveUsers(BaseModel):
    users: list[SessionUser]
    ais: list[str]

@router.get("/session/{session_id}/active_users")
def get_active_users(session_id: str) -> ActiveUsers:
    session = get_session_or_raise(session_id)
    return ActiveUsers(
        users=[SessionUser(username=user.user.name, last_active=user.last_active) for user in session.get_active_users()],
        ais=[ai.name for ai in session.get_ais()]
    )

class ReadMessage(BaseModel):
    message: str
    username: str
    # timestamp in ms since epoch
    timestamp: int
    is_private_message: bool


@router.get("/session/{session_id}/messages/{username}")
def read_messages(session_id: str, username: Username):
    session = get_session_or_raise(session_id)
    session.update_user_last_active(username)
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
    session = get_session_or_raise(session_id)
    return session.get_etabeta_state()


class SendMessage(BaseModel):
    message: str
    username: Username


@router.post("/session/{session_id}/send_message")
async def send_message(session_id: str, message: SendMessage):
    if len(message.message) == 0:
        return

    session = get_session_or_raise(session_id)

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
            session.add_ai(
                command.commander, AIUser(command.args[0], command.args[1])
            )
            sessions.save()
            return

        if command.cmd == "help":
            session.add_message(
                Message(
                    message="""
| Command     | Arguments     | Description                                                                                                                            |
| ----------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| /topic      | $topic        | Set the topic of the debate to $topic.                                                                                                 |
| /start      |               | Start the debate. The topic must first be set, see /topic.                                                                             |
| /pause      |               | Pause the debate.                                                                                                                      |
| /ai         | $name $prompt | Add an AI user to the room with the given name and prompt. You can use the prompt to tell the AI what to think about the debate topic. | 
| /help       |               | Show this help message.                                                                                                                |

*Note*: Command arguments must be separated by a space. For multi-word arguments, use quotes. For example: /topic "This is a topic".
""",
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
