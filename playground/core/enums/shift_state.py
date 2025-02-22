from enum import Enum


class ShiftState(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
