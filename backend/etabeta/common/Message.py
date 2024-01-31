from pydantic import BaseModel
from typing import NewType

Username = NewType("Username", str)


class Message(BaseModel):
    message: str
    username: str
    # timestamp in ms since epoch
    timestamp: int
    private_message: list[Username] | None = None
