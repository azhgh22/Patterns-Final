from typing import Protocol

from playground.core.models.receipt import Receipt
from playground.core.models.shift import Shift


class ShiftRepository(Protocol):
    def get_open_shift_id(self) -> str | None:
        pass

    def close(self, shift_id: str) -> bool:
        pass

    def store(self, shift: Shift) -> None:
        pass

    def add_receipt(self, shift_id: str, receipt: Receipt) -> bool:
        pass

    def get_shift_receipts(self, shift_id: str) -> list[Receipt]:
        pass

    def remove_receipt(self, shift_id: str, receipt_id: str) -> bool:
        pass
