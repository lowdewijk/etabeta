import asyncio
import time
import json
from pydantic import BaseModel

from openai import AsyncOpenAI
from typing import Optional

class Message(BaseModel):    
    message: str
    username: str
    # timestamp in ms since epoch
    timestamp: int

class EtaBeta(BaseModel):
  messages: list[Message] = []
  in_court: Optional[str] = None
  scores: dict[str, int] = {}

class Session():
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.etabeta = EtaBeta()
        self.messages = []

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
        model="gpt-4-1106-preview",
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
  "required": ["observations", "ball_in_court"],
  "properties": {
    "observations": {
      "type": "object",
      "description": "Observations about the last message",
      "required": ["positive", "negative", "username"],
      "properties": {
        "username": {
          "type": "string",
          "description": "The name of the user who spoke last"
        },
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
              "description": "Evidence that is not very convincing. Not contributing anything to the debate does not count as low quality evidence.",
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
    "ball_in_court": {
      "description": "The name of the user who has the ball in their court",
      "type": "string"
    }
  },
}
"""},
          {"role": "user", "content": chat_log}
        ]
      )
      resp = json.loads(response.choices[0].message.content)

      self.etabeta.in_court  = resp.get("ball_in_court", None)
      positives = resp.get("observations", {}).get("positive", {})
      negatives = resp.get("observations", {}).get("negative", {})
      username = resp.get("observations", {}).get("username", None)

      timestamp = time.time_ns() // 1_000_000
      
      for hq in positives.get("high_quality_evidence_presented", []):
        self.etabeta.messages.append(Message(message=f"Nice evidence {username}! {hq}", username="Eta Beta", timestamp=timestamp))
        self.etabeta.scores[username] = self.etabeta.scores.get(username, 0) + 1
      for hq in positives.get("high_quality_arguments_presented", []):
        self.etabeta.messages.append(Message(message=f"Nice argument {username}! {hq}", username="Eta Beta", timestamp=timestamp))
        self.etabeta.scores[username] = self.etabeta.scores.get(username, 0) + 1

      for hq in negatives.get("logical_fallacies_or_mistakes", []):
        self.etabeta.messages.append(Message(message=f"{username} committed a fallacy :( {hq}", username="Eta Beta", timestamp=timestamp))
        self.etabeta.scores[username] = self.etabeta.scores.get(username, 0) - 1
      for hq in negatives.get("low_quality_evidence_presented", []):
        self.etabeta.messages.append(Message(message=f"{username} presented low evidence :( {hq}", username="Eta Beta", timestamp=timestamp))
        self.etabeta.scores[username] = self.etabeta.scores.get(username, 0) - 1
      for hq in negatives.get("insults_or_ad_hominem_attacks", []):
        self.etabeta.messages.append(Message(message=f"{username} committed an ad hominem :( {hq}", username="Eta Beta", timestamp=timestamp))
        self.etabeta.scores[username] = self.etabeta.scores.get(username, 0) - 1

    def get_etabeta_state(self):
        return self.etabeta
