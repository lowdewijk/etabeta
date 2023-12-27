import asyncio
import time
from pydantic import BaseModel

from openai import AsyncOpenAI
from typing import Optional

class Message(BaseModel):    
    message: str
    username: str
    # timestamp in ms since epoch
    timestamp: int

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
      client = AsyncOpenAI()

      chat_list = [f"User: {msg.username} Message: {msg.message}" for msg in self.messages]
      chat_log = "\n---\n".join(chat_list)

      response = await client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={ "type": "json_object" },
        messages=[
          {"role": "system", "content": """
You are etabeta, an impartial debate observer. You will be given a chat log and should return the following information:

 * Observations about the LAST message:
  * Positive:
   * High quality evidence presented by the last user to speak
   * High quality arguments presented by the last user to speak
  * Negative:
    * Any logical fallacies or logical mistakes committed by the last user to speak
    * Any low quality evidence presented by the last user to speak
    * Any insults or ad hominem attacks committed by the last user to speak
 * The name of the user who has the ball in their court
 * The name of the user who is winning the debate

Use this JSON schema:

{
  "type": "object",
  "properties": {
    "observations_last_message": {
      "type": "object",
      "description": "Observations about the last message",
      "properties": {
        "positive": {
          "type": "object",
          "properties": {
            "high_quality_evidence_presented": {
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "high_quality_arguments_presented": {
              "type": "array",
              "items": {
                "type": "string"
              }
            }
          }
        },
        "negative": {
          "type": "object",
          "properties": {
            "logical_fallacies_or_mistakes": {
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "low_quality_evidence_presented": {
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "insults_or_ad_hominem_attacks": {
              "type": "array",
              "items": {
                "type": "string"
              }
            }
          }
        }
      }
    },
    "last_user_with_ball": {
      "type": "string"
    },
    "debate_winner": {
      "type": "string"
    }
  },
  "required": ["observations", "last_user_with_ball", "debate_winner"]
}
"""},
          {"role": "user", "content": chat_log}
        ]
      )
      self.etabeta_messages.append(Message(message=response.choices[0].message.content, username="Eta Beta", timestamp=time.time_ns() // 1_000_000))

    def get_etabeta_messages(self):
        return self.etabeta_messages
