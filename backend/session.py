from dataclasses import dataclass
from enum import Enum
import time

from typing import Optional, List
from EtaBeta import ETABETA_USERNAME, EtaBeta
from Message import Message

from UserError import UserError

class SessionState(Enum):
    LOBBY = 1
    DEBATING = 2
    PAUSED = 3

@dataclass
class StateChange:
    timestamp: int
    prev_state: SessionState
    next_state: SessionState

class Session:
    session_id: str
    messages: List[Message] = []
    topic: Optional[str] = None
    etabeta: EtaBeta
    state: SessionState = SessionState.LOBBY
    state_history: List[StateChange]

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.etabeta = EtaBeta()
        self.messages = []
        self.state = SessionState.LOBBY
        self.state_history = []

    def add_message(self, message: Message):
        self.messages.append(message)

    def get_messages(self):
        return self.messages

    def get_session_id(self):
        return self.session_id

    async def query_etabeta(self):
        return await self.etabeta.query(self.get_topic(), self.get_debate_messages())

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

        self.state_history.append(StateChange(
            timestamp=time.time_ns() // 1_000_000,
            prev_state=self.state,
            next_state=state,
        ))
        self.state = state
    
    def get_state(self):
        return self.state
    
    def get_debate_times(self):
        '''
        Returns a list of tuples (start, end) where start is the timestamp of the start of the debate and 
        end is the timestamp of the end of the debate or None whenever the debate is still ongoing.
        '''
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
        debate_messasges = [message for message in self.messages 
                            if message.timestamp >= debate_times[0][0] and 
                            (debate_times[0][1] is None or message.timestamp <= debate_times[0][1]) and
                            message.username != ETABETA_USERNAME]
        return debate_messasges
