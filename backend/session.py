from enum import Enum
import time

from typing import Optional, List
from EtaBeta import EtaBeta
from Message import Message

from UserError import UserError

class SessionState(Enum):
    LOBBY = 1
    DEBATING = 2
    PAUSED = 3

class Session:
    session_id: str
    messages: List[Message] = []
    topic: Optional[str] = None
    etabeta: EtaBeta
    state: SessionState = SessionState.LOBBY

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.etabeta = EtaBeta()
        self.messages = []
        self.state = SessionState.LOBBY

    def add_message(self, message: Message):
        self.messages.append(message)

    def get_messages(self):
        return self.messages

    def get_session_id(self):
        return self.session_id

    async def query_etabeta(self):
        print("Querying EtaBeta")
        return await self.etabeta.query(self.messages)

    def get_etabeta_state(self):
        return self.etabeta
    
    def set_topic(self, commander: str, topic: str):
        self.topic = topic
        self.messages.append(Message(
            message=f"Topic set to '{topic}' by {commander}",
            username="Eta Beta",
            timestamp=time.time_ns() // 1_000_000,
        ))

    def get_topic(self):
        return self.topic

    def set_state(self, commander: str, state: SessionState):
        if self.state != SessionState.DEBATING and state == SessionState.DEBATING:
            if self.topic is None:
                raise UserError(commander, "Topic must be set before starting debate.")
            self.messages.append(Message(
                message=f"Debate has started!",
                username="Eta Beta",
                timestamp=time.time_ns() // 1_000_000,
            ))

        self.state = state
    
    def get_state(self):
        return self.state