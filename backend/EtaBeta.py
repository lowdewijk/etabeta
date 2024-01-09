from dataclasses import dataclass
import logging
import time
import yaml
import json
from pydantic import BaseModel

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam
from typing import Optional, List, Callable

from Message import Message
from textwrap import dedent

ETABETA_USERNAME="Eta Beta"

@dataclass
class ObservationDesc:
    description: str
    tostr: Callable[[str, str], str]
    score: float


OBSERVATIONS_TYPES: dict[str, ObservationDesc] = {
    "strong-argument": ObservationDesc(
        description="Strong, well-reasoned and convincing arguments made.",
        tostr=lambda user, arg: f"Nice argument {user}! {arg}",
        score=5,
    ),
    "strong-evidence": ObservationDesc(
        description="High-quality, reliable evidence presented.",
        tostr=lambda user, arg: f"Awesome evidence {user}! {arg}",
        score=8,
    ),
    "logic": ObservationDesc(
        description="Logical consistency and coherence.",
        tostr=lambda user, arg: f"Logical consistency {user}! {arg}",
        score=3,
    ),
    "accurate_summary": ObservationDesc(
        description="Giving an accurate summary of the other side's argument.",
        tostr=lambda user, arg: f"God summary {user}! {arg}",
        score=1,
    ),
    "clarifying_questions": ObservationDesc(
        description="Asking clarifying questions.",
        tostr=lambda user, arg: f"Good job asking clarifying questions {user}! {arg}",
        score=0.25,
    ),
    "low_quality_evidence": ObservationDesc(
        description="Low-quality evidence presented.",
        tostr=lambda user, arg: f"{user} presented low-quality evidence: {arg}",
        score=-0.5,
    ),
    "logical_fallacies": ObservationDesc(
        description="Logical fallacies or errors in reasoning.",
        tostr=lambda user, arg: f"{user} committed a fallacy: {arg}",
        score=-0.5,
    ),
    "personal_attacks": ObservationDesc(
        description="Personal attacks or ad hominem fallacies.",
        tostr=lambda user, arg: f"{user} committed an ad hominem: {arg}",
        score=-2,
    ),
    "insults": ObservationDesc(
        description="Insults or profanity.",
        tostr=lambda user, arg: f"{user} insulted someone: {arg}",
        score=-5,
    ),
    "off_topic": ObservationDesc(
        description="Off-topic or irrelevant comments.",
        tostr=lambda user, arg: f"{user} went off-topic: {arg}",
        score=-0.1,
    ),
    "repetition": ObservationDesc(
        description="Repetition of previous arguments.",
        tostr=lambda user, arg: f"{user} repeated themselves: {arg}",
        score=-0.5,
    ),
    "contradiction": ObservationDesc(
        description="Contradiction of previous arguments.",
        tostr=lambda user, arg: f"{user} contradicted themselves: {arg}",
        score=-0.5,
    ),
    "nonsequitur": ObservationDesc(
        tostr=lambda user, arg: f"{user} made a non-sequitur: {arg}",
        description="Non-sequitur or non-logical arguments.",
        score=-0.5,
    ),
    "misinformation": ObservationDesc(
        description="Misinformation or false claims.",
        tostr=lambda user, arg: f"{user} spread misinformation: {arg}",
        score=-0.5,
    ),
    "misleading": ObservationDesc(
        description="Misleading or deceptive claims.",
        tostr=lambda user, arg: f"{user} made a misleading claim: {arg}",
        score=-0.5,
    ),
    "unsubstantiated": ObservationDesc(
        description="Unsubstantiated claims.",
        tostr=lambda user, arg: f"{user} made an unsubstantiated claim: {arg}",
        score=-0.5,
    ),
}

POSITIVE_OBSERVATIONS = {
    p_key: {
        "type": "object",
        "required": ["name", "comment"],
        "description": "Observation comments by EtaBeta. " + p_value.description,
        "properties": {
            "name": {
                "type": "string",
                "enum": [p_key],
            },
            "comment": {"type": "string"},
        },
    }
    for p_key, p_value in OBSERVATIONS_TYPES.items()
}

ETABETA_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["observations", "ball_in_court", "summary"],
    "properties": {
        "observations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "required": ["name"],
                    "name": {
                        "type": "string",
                        "enum": list(OBSERVATIONS_TYPES.keys()),
                    },
                    "comment": {"type": "string"},
                },
            },
        },
        "summary": {
            "type": "string",
            "description": "Summary of the debate",
        },
        "ball_in_court": {
            "description": "User with the initiative",
            "type": "string",
        },
    },
}

class Observation(BaseModel):
    name: str
    comment: str


class EtaBetaResponse(BaseModel):
    observations: List[Observation] = []
    summary: str
    ball_in_court: str


class EtaBeta(BaseModel):
    messages: List[Message] = []
    in_court: Optional[str] = None
    scores: dict[str, float] = {}
    under_observation: List[int] = []

    def create_assistant_prompt(self):
      obs_descriptions = "\n".join([f"{name} - {obs.description}" for name, obs in OBSERVATIONS_TYPES.items()])

      return dedent(f"""
        You are EtaBeta, an AI designed to impartially analyze debates. 
                      
        You will be given a chat log. You should make observations about the messages that are flagged for observation.
        The observations that you should make are:
        {obs_descriptions}

        You should also 
          - Summarize the debate
          - Determine who has the initiative in the debate ('ball in their court').

        Use this JSON schema for your response:

        {yaml.dump(ETABETA_RESPONSE_SCHEMA)}
      """)
        

    async def query(self, debate_topic: str, debate_messages: List[Message]) -> None:
        if len(debate_messages) == 0:
            return
        observed_message_timestamp = debate_messages[-1].timestamp

        try:
            client = AsyncOpenAI()

            chat_log = [
                {"user": msg.username, "message": msg.message, "observe": False}
                for msg in debate_messages
            ]
            chat_log[-1]["observe"] = True
            observed_user = debate_messages[-1].username
            self.under_observation.append(observed_message_timestamp)

            assistant_prompt = self.create_assistant_prompt()
            messages: List[ChatCompletionMessageParam]=[
                    {
                        "role": "system",
                        "content": assistant_prompt,
                    },
                    {"role": "user", "content": 
                        dedent(f""""
                          The debate topic is: {debate_topic}."
                          This is the chat log:
                          {yaml.dump(chat_log)}
                        """),
                    }
                ]
            logging.info(yaml.dump(messages))
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                response_format={"type": "json_object"},
                messages=messages,
            )
            if response.choices[0].message.content is None:
                raise Exception("Empty response from EtaBeta.")

            logging.info(response.choices[0].message.content)
            resp_content: dict = json.loads(response.choices[0].message.content)
            resp = EtaBetaResponse(**resp_content)

            self.in_court = resp.ball_in_court

            timestamp = time.time_ns() // 1_000_000

            for observation in resp.observations:
                obs_type = OBSERVATIONS_TYPES.get(observation.name)
                if obs_type is None:
                    logging.warning(f"Unknown observation '{observation.name}' with comment: {observation.comment}")
                    continue
                
                msg = ("👍" if obs_type.score > 0 else "👎") +" "+ obs_type.tostr(observed_user, observation.comment)
                self.messages.append(
                    Message(
                        message=msg,
                        username=ETABETA_USERNAME,
                        timestamp=timestamp,
                    )
                )
                prev_score = self.scores.get(observed_user, 0)
                self.scores[observed_user] = max(0,round(prev_score + obs_type.score, 2))
        except Exception as e:
            logging.exception(e)
        finally:
            self.under_observation.remove(observed_message_timestamp)
