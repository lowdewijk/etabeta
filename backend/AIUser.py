from dataclasses import dataclass
import logging
from textwrap import dedent

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam
import yaml

from Message import Message

@dataclass
class AIUser:
    name: str
    description_prompt: str

    def create_assistant_prompt(self, debate_topic: str):
      return dedent(f"""
        You are participating in a debate on the topic: {debate_topic}. 
        Try to match the length of your response to the length of the messages you are responding to.
        You should respond to the last message. 
        {self.description_prompt}
      """)
        
    async def query(self, debate_topic: str, debate_messages: list[Message]) -> str:
      client = AsyncOpenAI()

      chat_log = [
          {"user": msg.username, "message": msg.message}
          for msg in debate_messages
      ]

      assistant_prompt = self.create_assistant_prompt(debate_topic)
      messages: list[ChatCompletionMessageParam]=[
              {
                  "role": "system",
                  "content": assistant_prompt,
              },
              {"role": "user", "content": 
                  dedent(f""""
                    This is the chat log:
                    {yaml.dump(chat_log)}
                  """),
              }
          ]
      logging.error(yaml.dump(messages))
      response = await client.chat.completions.create(
          model="gpt-3.5-turbo-1106",
          messages=messages,
      )
      
      response_message = response.choices[0].message.content
      if response_message is None:
        raise Exception("Empty AI response.")
      return response_message
