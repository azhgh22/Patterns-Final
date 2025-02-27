from copy import deepcopy
from typing import List

from playground.core.models.payments import Payment


class PaymentInMemoryRepository:
    def __init__(self, payment_list: List[Payment] | None = None) -> None:
        if payment_list is None:
            payment_list = []
        self.payment_list = payment_list

    def register_payment(self, payment: Payment) -> None:
        self.payment_list.append(deepcopy(payment))

    def get_payment(self, receipt_id: str) -> Payment | None:
        for payment in self.payment_list:
            if payment.receipt_id == receipt_id:
                return deepcopy(payment)
        return None

    def get_all_payments(self) -> list[Payment]:
        return self.payment_list
