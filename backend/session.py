import asyncio
from pydantic import BaseModel

from openai import OpenAI

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
      client = OpenAI()

      response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={ "type": "json_object" },
        messages=[
          {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
          {"role": "user", "content": "Who won the world series in 2020?"}
        ]
      )
      self.etabeta_messages.append(Message(message=response.choices[0].message.content, username="Eta Beta"))

    def get_etabeta_messages(self):
        return self.etabeta_messages
