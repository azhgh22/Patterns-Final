from collections import defaultdict
from dataclasses import dataclass
from uuid import uuid4

from playground.core.enums.shift_state import ShiftState
from playground.core.models.product import ProductReport
from playground.core.models.receipt import Receipt
from playground.core.models.revenue import Revenue
from playground.core.models.shift import Shift
from playground.core.models.x_report import XReport
from playground.core.services.interfaces.memory.shift_repository import ShiftRepository
from playground.core.services.interfaces.service_interfaces.payments_service_interface import (
    IPaymentsService,
)
from playground.infra.memory.in_memory.shift_in_memory_repository import (
    ShiftInMemoryRepository,
)


@dataclass
class ShiftService:
    repo: ShiftRepository = ShiftInMemoryRepository()

    def open(self) -> Shift:
        if self.get_open_shift_id() is not None:
            raise ValueError
        shift = Shift(str(uuid4()), ShiftState.OPEN, [])
        self.repo.store(shift)
        return shift

    def close(self, shift_id: str) -> bool:
        if shift_id != self.get_open_shift_id():
            raise IndexError
        receipts = self.repo.get_shift_receipts(shift_id)
        for receipt in receipts:
            # TODO: change it to use enum
            if receipt.status == "open":
                return False

        return self.repo.close(shift_id)

    def get_open_shift_id(self) -> str | None:
        return self.repo.get_open_shift_id()

    def get_x_report(
        self,
        shift_id: str,
        payment_service: IPaymentsService,
    ) -> XReport:
        items: dict[str, int] = defaultdict(int)
        sales: dict[str, int] = defaultdict(int)

        shift_receipts = self.repo.get_shift_receipts(shift_id)

        for receipt in shift_receipts:
            for item in receipt.products:
                items[item.product_id] += item.quantity

            payment = payment_service.get(receipt.id)
            sales[payment.currency_id] += payment.amount

        products = [
            ProductReport(product_id, quantity) for product_id, quantity in items.items()
        ]
        revenue = [Revenue(currency_id, amount) for currency_id, amount in sales.items()]

        return XReport(shift_id, len(shift_receipts), products, revenue)

    def add_receipt(self, receipt: Receipt) -> Receipt | None:
        open_shift_id = self.get_open_shift_id()
        if open_shift_id is None:
            raise ValueError("Open shift to start working")
        if receipt.status == "close":
            return None

        updated_receipt = self.repo.add_receipt(open_shift_id, receipt)
        return updated_receipt

    def remove_receipt(self, shift_id: str, receipt_id: str) -> bool:
        open_shift_id = self.get_open_shift_id()
        if open_shift_id is None or open_shift_id != shift_id:
            raise ValueError("open shift doesn't exist")

        self.repo.remove_receipt(shift_id, receipt_id)
        return True
