from pydantic import BaseModel

class Message(BaseModel):
    message: str
    username: str
    # timestamp in ms since epoch
    timestamp: int
