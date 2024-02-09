from pydantic.dataclasses import dataclass

@dataclass
class Config:
    prune_session_user_timeout: int

config = Config(
    prune_session_user_timeout=5*1000
)