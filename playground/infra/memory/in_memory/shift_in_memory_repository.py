from copy import deepcopy
from typing import List

from playground.core.models.receipt import Receipt
from playground.core.models.shift import Shift


class ShiftInMemoryRepository:
    def __init__(self, shift_list: List[Shift] | None = None) -> None:
        if shift_list is None:
            shift_list = []
        self.shift_list = shift_list

    def get_shift_with_id(self, shift_id: str) -> Shift | None:
        for shift in self.shift_list:
            if shift.id == shift_id:
                return shift
        return None

    def get_all_shifts(self) -> list[Shift]:
        return deepcopy(self.shift_list)

    def store_shift(self, shift: Shift) -> None:
        self.shift_list.append(deepcopy(shift))

    def get_open_shift_id(self) -> str | None:
        pass

    def close(self, shift_id: str) -> bool:
        pass

    def store(self, shift: Shift) -> None:
        pass

    def add_receipt(self, shift_id: str, receipt: Receipt) -> bool:
        pass
