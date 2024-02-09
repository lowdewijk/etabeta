from etabeta.common.Username import Username
from pydantic import BaseModel


class Message(BaseModel):
    message: str
    username: str
    # timestamp in ms since epoch
    timestamp: int
    private_message: list[Username] | None = None
