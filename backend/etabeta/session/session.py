import asyncio
from dataclasses import dataclass
from enum import Enum
import time

from typing import Optional, List
from etabeta.session.AIUser import AIUser
from etabeta.session.EtaBeta import ETABETA_USERNAME, EtaBeta
from etabeta.common.Message import Message

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
class HumanUser:
    name: str


User = HumanUser | AIUser


class Session:
    session_id: str
    messages: List[Message] = []
    topic: Optional[str] = None
    etabeta: EtaBeta
    state: SessionState
    state_history: List[StateChange]
    active_users: List[User] = []

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.etabeta = EtaBeta()
        self.messages = []
        self.state = SessionState.LOBBY
        self.state_history = []
        self.active_users = []

    def add_message(self, message: Message):
        self.messages.append(message)

    def get_messages(self):
        return self.messages

    def get_session_id(self):
        return self.session_id

    async def query_ais(self):
        debate_messages = self.get_debate_messages()
        topic = self.topic
        if topic == None or len(debate_messages) == 0:
            return

        async def get_ai_message(
            ai_user: AIUser, debate_messages: list[Message]
        ) -> None:
            message = await ai_user.query(topic, debate_messages)
            self.messages.append(
                Message(
                    message=message,
                    username=ai_user.name,
                    timestamp=time.time_ns() // 1_000_000,
                )
            )

        ai_users = self.get_ai_users()
        awaits = [self.etabeta.query(topic, debate_messages)] + [
            get_ai_message(ai_user, debate_messages) for ai_user in ai_users
        ]
        await asyncio.gather(*awaits)

        # run again to check the message of the AI users
        if len(ai_users) > 0:
            await self.etabeta.query(self.get_topic(), self.get_debate_messages())

    def get_etabeta_state(self):
        return self.etabeta

    def set_topic(self, commander: str, topic: str):
        self.topic = topic
        self.messages.append(
            Message(
                message=f"Topic set to '{topic}' by {commander}",
                username="Eta Beta",
                timestamp=time.time_ns() // 1_000_000,
            )
        )

    def get_topic(self):
        return self.topic

    def set_state(self, commander: str, state: SessionState):
        if self.state != SessionState.DEBATING and state == SessionState.DEBATING:
            if self.topic is None:
                raise UserError(commander, "Topic must be set before starting debate.")
            self.messages.append(
                Message(
                    message=f"Debate has started!",
                    username="Eta Beta",
                    timestamp=time.time_ns() // 1_000_000,
                )
            )

        self.state_history.append(
            StateChange(
                timestamp=time.time_ns() // 1_000_000,
                prev_state=self.state,
                next_state=state,
            )
        )
        self.state = state

    def get_state(self):
        return self.state

    def get_debate_times(self):
        """
        Returns a list of tuples (start, end) where start is the timestamp of the start of the debate and
        end is the timestamp of the end of the debate or None whenever the debate is still ongoing.
        """
        debate_times = []
        start_debate = None
        for state in self.state_history:
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
            for message in self.messages
            if message.timestamp >= debate_times[0][0]
            and (debate_times[0][1] is None or message.timestamp <= debate_times[0][1])
            and message.username != ETABETA_USERNAME
            and message.message.startswith("#") == False
        ]
        return debate_messasges

    def get_active_users(self):
        return self.active_users

    def add_ai_user(self, commander: str, ai_user: AIUser):
        self.active_users.append(ai_user)
        self.messages.append(
            Message(
                message=f"AI user '{ai_user.name}' added by {commander}.",
                username="Eta Beta",
                timestamp=time.time_ns() // 1_000_000,
            )
        )

    def get_ai_users(self) -> list[AIUser]:
        return [user for user in self.active_users if isinstance(user, AIUser)]
