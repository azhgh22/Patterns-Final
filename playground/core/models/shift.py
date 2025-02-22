from dataclasses import dataclass
from typing import List

from playground.core.enums.shift_state import ShiftState
from playground.core.models.receipt import Receipt


@dataclass
class Shift:
    id: str
    state: ShiftState
    receipts: List[Receipt]

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, type(self)):
            return False
        return (
            self.id == other.id
            and self.state == other.state
            and self.receipts == other.receipts
        )
