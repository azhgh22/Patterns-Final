from enum import Enum


class ReceiptStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
