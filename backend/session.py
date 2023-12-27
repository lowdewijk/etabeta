from pydantic import BaseModel

class Message(BaseModel):    
    message: str
    username: str

class Session():
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.messages = []

    def add_message(self, message: Message):
        self.messages.append(message)

    def get_messages(self):
        return self.messages

    def get_session_id(self):
        return self.session_id
