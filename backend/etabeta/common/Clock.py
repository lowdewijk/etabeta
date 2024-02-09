import time
from typing import Callable
from typing import NewType

Timestamp = NewType("Timestamp", int)

class Clock:
    def __init__(self, get_timestamp: Callable[[],int]):
        self._get_timestamp = get_timestamp

    def get_timestamp(self) -> Timestamp:
        return Timestamp(self._get_timestamp())
    
    def set_fixed_timestamp(self, timestamp: int | Timestamp):
        self._get_timestamp = lambda: timestamp

clock = Clock(lambda: time.time_ns() // 1_000_000)
