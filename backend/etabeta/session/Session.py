import asyncio
from dataclasses import dataclass
from enum import Enum
import time

from typing import Optional, List
from etabeta.common.Clock import Timestamp, clock
from etabeta.common.User import User
from etabeta.common.AIUser import AIUser
from etabeta.session.EtaBeta import ETABETA_USERNAME, EtaBeta
from etabeta.common.Message import Message
from etabeta.common.Username import Username

from etabeta.common.UserError import UserError


class SessionState(Enum):
    LOBBY = 1
    DEBATING = 2
    PAUSED = 3


@dataclass
class StateChange:
    timestamp: int
    prev_state: SessionState
    next_state: SessionState

@dataclass
class SessionUser:
    user: User
    last_active: Timestamp

class Session:
    _session_id: str
    _messages: List[Message]
    _topic: Optional[str]
    _etabeta: EtaBeta
    _state: SessionState
    _state_history: List[StateChange]
    _ais: List[AIUser]
    _active_users: dict[Username, SessionUser]

    def __init__(self, session_id: str):
        self._session_id = session_id
        self._etabeta = EtaBeta()
        self._messages = []
        self._state = SessionState.LOBBY
        self._state_history = []
        self._ais = []
        self._active_users = {}

    def add_message(self, message: Message):
        self._messages.append(message)

    def get_messages(self, username: Username) -> list[Message]:
        return [
            msg
            for msg in self._messages
            if msg.private_message is None or username in msg.private_message
        ]

    def get_session_id(self):
        return self._session_id

    async def query_ais(self):
        debate_messages = self.get_debate_messages()
        topic = self._topic
        if topic == None or len(debate_messages) == 0:
            return

        async def get_ai_message(
            ai_user: AIUser, debate_messages: list[Message]
        ) -> None:
            message = await ai_user.query(topic, debate_messages)
            self._messages.append(
                Message(
                    message=message,
                    username=ai_user.name,
                    timestamp=time.time_ns() // 1_000_000,
                )
            )

        awaits = [self._etabeta.query(topic, debate_messages)] + [
            get_ai_message(ai_user, debate_messages) for ai_user in self._ais
        ]
        await asyncio.gather(*awaits)

        # run again to check the message of the AI users
        if len(self._ais) > 0:
            await self._etabeta.query(self.get_topic(), self.get_debate_messages())

    def get_etabeta_state(self):
        return self._etabeta

    def set_topic(self, commander: str, topic: str):
        self._topic = topic
        self._messages.append(
            Message(
                message=f"Topic set to '{topic}' by {commander}",
                username="Eta Beta",
                timestamp=time.time_ns() // 1_000_000,
            )
        )

    def get_topic(self):
        return self._topic

    def set_state(self, commander: str, state: SessionState):
        if self._state != SessionState.DEBATING and state == SessionState.DEBATING:
            if self._topic is None:
                raise UserError(commander, "Topic must be set before starting debate.")
            self._messages.append(
                Message(
                    message=f"Debate has started!",
                    username="Eta Beta",
                    timestamp=time.time_ns() // 1_000_000,
                )
            )

        self._state_history.append(
            StateChange(
                timestamp=time.time_ns() // 1_000_000,
                prev_state=self._state,
                next_state=state,
            )
        )
        self._state = state

    def get_state(self):
        return self._state

    def get_debate_times(self):
        """
        Returns a list of tuples (start, end) where start is the timestamp of the start of the debate and
        end is the timestamp of the end of the debate or None whenever the debate is still ongoing.
        """
        debate_times = []
        start_debate = None
        for state in self._state_history:
            if state.next_state == SessionState.DEBATING:
                start_debate = state.timestamp
            if state.prev_state == SessionState.DEBATING:
                debate_times.append((start_debate, state.timestamp))
                start_debate = None
        if start_debate is not None:
            debate_times.append((start_debate, None))
        return debate_times

    def get_debate_messages(self):
        debate_times = self.get_debate_times()
        debate_messasges = [
            message
            for message in self._messages
            if message.timestamp >= debate_times[0][0]
            and (debate_times[0][1] is None or message.timestamp <= debate_times[0][1])
            and message.username != ETABETA_USERNAME
            and message.message.startswith("#") == False
        ]
        return debate_messasges

    def get_ais(self):
        return self._ais

    def add_ai(self, commander: str, ai_user: AIUser):
        self._ais.append(ai_user)
        self._messages.append(
            Message(
                message=f"AI user '{ai_user.name}' added by {commander}.",
                username="Eta Beta",
                timestamp=time.time_ns() // 1_000_000,
            )
        )

    def add_user(self, user: User):
        self._active_users[user.name] = SessionUser(user, clock.get_timestamp())
    
    def update_user_last_active(self, user: User, timestamp = clock.get_timestamp()):
        if user.name in self._active_users:
            self._active_users[user.name].last_active = timestamp

    def remove_user(self, username: Username) -> bool:
        user_exists = username in self._active_users
        if user_exists:
            del self._active_users[username]
        return user_exists

    def get_active_users(self) -> list[SessionUser]:
        return list(self._active_users.values())