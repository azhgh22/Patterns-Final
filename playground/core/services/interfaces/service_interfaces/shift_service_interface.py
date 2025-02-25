from typing import Protocol

from playground.core.models.receipt import Receipt
from playground.core.models.shift import Shift
from playground.core.models.x_report import XReport
from playground.core.services.interfaces.service_interfaces.payments_service_interface import (
    IPaymentsService,
)


class IShiftService(Protocol):
    def open(self) -> Shift:
        pass

    def close(self, shift_id: str) -> bool:
        pass

    def get_open_shift_id(self) -> str | None:
        pass

    def get_x_report(
        self,
        shift_id: str,
        payment_service: IPaymentsService,
    ) -> XReport:
        pass

    def add_receipt(self, receipt: Receipt) -> Receipt:
        pass

    def remove_receipt(self, shift_id: str, receipt_id: str) -> bool:
        pass
