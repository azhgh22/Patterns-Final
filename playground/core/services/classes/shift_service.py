from collections import defaultdict
from dataclasses import dataclass
from uuid import uuid4

from playground.core.enums.shift_state import ShiftState
from playground.core.models.product import ProductReport
from playground.core.models.revenue import Revenue
from playground.core.models.shift import Shift
from playground.core.models.x_report import XReport
from playground.core.services.interfaces.memory.shift_repository import ShiftRepository
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

    def close(self, shift_id: str, receiptService: ReceiptService) -> bool:
        if shift_id != self.get_open_shift_id():
            raise IndexError
        receipt_ids = self.repo.get_shift_receipt_ids(shift_id)
        for receipt_id in receipt_ids:
            receipt = receiptService.get(receipt_id)
            # TODO: change it to use enum
            if receipt.status == "open":
                return False

        return self.repo.close(shift_id)

    def get_open_shift_id(self) -> str | None:
        return self.repo.get_open_shift_id()

    def get_x_report(
        self,
        shift_id: str,
        receiptService: ReceiptService,
        paymentService: PaymentService,
    ) -> XReport:
        items = defaultdict(int)
        sales = defaultdict(int)

        shift_receipt_ids = self.repo.get_shift_receipt_ids(shift_id)

        for receipt_id in shift_receipt_ids:
            receipt = receiptService.get(receipt_id)
            for product in receipt.products:
                items[product.product_id] += product.amount

            payment = paymentService.get(receipt_id)
            sales[payment.currency_id] += payment.amount

        products = [
            ProductReport(product_id, amount) for product_id, amount in items.items()
        ]
        revenue = [
            Revenue(currency_id, amount) for currency_id, amount in sales.items()
        ]

        return XReport(shift_id, len(shift_receipt_ids), products, revenue)

    # IMPORTANT: only closed receipts are added to the shift
    def add_receipt(
        self, shift_id: str, receipt_id: str, receiptService: ReceiptService
    ) -> bool:
        open_shift_id = self.get_open_shift_id()
        if open_shift_id is None or open_shift_id != shift_id:
            raise IndexError
        if receiptService.get(receipt_id).status == "open":
            raise ValueError

        self.repo.add_receipt(shift_id, receipt_id)
        return True
