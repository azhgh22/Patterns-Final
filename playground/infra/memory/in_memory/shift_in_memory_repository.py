from copy import deepcopy
from typing import List

from playground.core.enums.shift_state import ShiftState
from playground.core.models.receipt import Receipt
from playground.core.models.shift import Shift


class ShiftInMemoryRepository:
    def __init__(self, shift_list: List[Shift] | None = None) -> None:
        if shift_list is None:
            shift_list = []
        self.shift_list = deepcopy(shift_list)

    def get_open_shift_id(self) -> str | None:
        for shift in self.shift_list:
            if shift.state == ShiftState.OPEN:
                return shift.id
        return None

    def close(self, shift_id: str) -> bool:
        for shift in self.shift_list:
            if shift.id == shift_id:
                shift.state = ShiftState.CLOSED
                return True
        return False

    def store(self, shift: Shift) -> None:
        self.shift_list.append(deepcopy(shift))

    def add_receipt(self, shift_id: str, receipt: Receipt) -> bool:
        for shift in self.shift_list:
            if shift.id == shift_id:
                shift.receipts.append(deepcopy(receipt))
                return True
        return False
