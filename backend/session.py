import asyncio
from pydantic import BaseModel

class Message(BaseModel):    
    message: str
    username: str

class Session():
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.messages = []
        self.etabeta_messages = []

    def add_message(self, message: Message):
        self.messages.append(message)

    def get_messages(self):
        return self.messages

    def get_session_id(self):
        return self.session_id
    
    async def query_etabeta(self):
        self.etabeta_messages.append(Message(message="Hello from Eta Beta", username="Eta Beta"))

    def get_etabeta_messages(self):
        return self.etabeta_messages
