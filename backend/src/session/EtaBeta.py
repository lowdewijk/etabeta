from dataclasses import dataclass
import logging
import time
import yaml
import json
from pydantic import BaseModel

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam
from typing import Optional, Callable

from src.common.Message import Message
from textwrap import dedent

ETABETA_USERNAME = "Eta Beta"


@dataclass
class ObservationDesc:
    description: str
    tostr: Callable[[str, str], str] | None = None
    score: float = 0


OBSERVATIONS_TYPES: dict[str, ObservationDesc] = {
    "questioning": ObservationDesc(
        description="Asking questions to the other side.",
        score=0,
    ),
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
    "accurate_summary": ObservationDesc(
        description="Giving an accurate summary of the other side's argument.",
        tostr=lambda user, arg: f"Good summary {user}! {arg}",
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
        description="Off-topic, irrelevant comments or not answering the question.",
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
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["observations_about_the_last_message", "ball_in_court", "summary"],
    "properties": {
        "observations_about_the_last_message": {
            "description": "Observation comments by EtaBeta about the last message only.",
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
            "type": "array",
            "description": "Summary of the entire debate in terms of its arguments",
            "items": {
                "type": "object",
                "items": {"$ref": "#/definitions/argument"},
            },
        },
        "ball_in_court": {
            "description": "User with the initiative",
            "type": "string",
        },
    },
    "definitions": {
        "argument": {
            "type": "object",
            "properties": {
                "argument": {"type": "string"},
                "counter_arguments": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/argument"},
                },
            },
            "required": ["argument"],
        }
    },
}


class Observation(BaseModel):
    name: str
    comment: str


class Argument(BaseModel):
    argument: str
    counter_arguments: "list[Argument]" = []


class EtaBetaResponse(BaseModel):
    observations_about_the_last_message: list[Observation] = []
    summary: list[Argument] = []
    ball_in_court: str = ""


class EtaBeta(BaseModel):
    messages: list[Message] = []
    in_court: Optional[str] = None
    scores: dict[str, float] = {}
    under_observation: list[int] = []
    summary: str = ""

    def create_assistant_prompt(self, observed_user: str):
        obs_descriptions = "\n".join(
            [
                f" - {name} - {obs.description}\n"
                for name, obs in OBSERVATIONS_TYPES.items()
            ]
        )

        return dedent(
            f"""
        You are EtaBeta, an AI designed to impartially analyze debates. You will be given a chat log to analyze by the user. 
        
        Please observe the LAST message by {observed_user} in the chat log and provide feedback on potential:
        {obs_descriptions}

        Try to keep the list of observations as small as possible. Do not respond with observations of any other messges in the chat log, but the last message.

        You should also: 
          - Summarize the entire debate using nested bullet-points with arguments for and against.
          - Determine who has the initiative in the debate ('ball in their court').

        Use this JSON schema for your response:
        {yaml.dump(ETABETA_RESPONSE_SCHEMA)}
      """
        )

    async def query(self, debate_topic: str, debate_messages: list[Message]) -> None:
        if len(debate_messages) == 0:
            return
        observed_message_timestamp = debate_messages[-1].timestamp

        try:
            client = AsyncOpenAI()

            chat_log: str = yaml.dump(
                [
                    {"user": msg.username, "message": msg.message}
                    for msg in debate_messages[:-1]
                ]
            )
            chat_log += "\n----\nThe last message is\n----\n" + yaml.dump(
                {
                    "user": debate_messages[-1].username,
                    "message": debate_messages[-1].message,
                }
            )

            observed_user = debate_messages[-1].username
            self.under_observation.append(observed_message_timestamp)

            assistant_prompt = self.create_assistant_prompt(observed_user)
            completion_messages: list[ChatCompletionMessageParam] = [
                {
                    "role": "system",
                    "content": assistant_prompt,
                },
                {
                    "role": "user",
                    "content": dedent(
                        f""""
                          The debate topic is: {debate_topic}."
                          This is the chat log:
                          {chat_log}
                        """
                    ),
                },
            ]
            # logging.info(json.dumps(completion_messages))
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo-1106",  # "gpt-4-1106-preview",
                response_format={"type": "json_object"},
                messages=completion_messages,
            )

            json_response = response.choices[0].message.content

            # this is so the type checker understand json_reponse is not optional
            if json_response is None:
                raise Exception("Empty AI repsonse.")

            logging.info(json_response)
            parsed_json_response: dict = json.loads(json_response)
            resp = EtaBetaResponse(**parsed_json_response)

            self.in_court = resp.ball_in_court
            self.summary = resp.summary
            if self.summary is None:
                self.summary = []

            timestamp = time.time_ns() // 1_000_000

            messages: list[str] = []
            for observation in resp.observations_about_the_last_message:
                obs_type = OBSERVATIONS_TYPES.get(observation.name)
                if obs_type is None or obs_type.score == 0:
                    logging.warning(
                        f"Unknown observation '{observation.name}' with comment: {observation.comment}"
                    )
                    continue

                up_or_down = "👍" if obs_type.score > 0 else "❌"
                msg = (
                    up_or_down
                    + " "
                    + obs_type.tostr(observed_user, observation.comment)
                    if obs_type.tostr is not None
                    else ""
                )
                messages.append(msg)
                prev_score = self.scores.get(observed_user, 0)
                self.scores[observed_user] = max(
                    0, round(prev_score + obs_type.score, 2)
                )

            if len(messages) > 0:
                self.messages.append(
                    Message(
                        username=ETABETA_USERNAME,
                        message="\n\n".join(messages),
                        timestamp=timestamp,
                    )
                )
        except Exception as e:
            logging.exception(e)
        finally:
            self.under_observation.remove(observed_message_timestamp)
