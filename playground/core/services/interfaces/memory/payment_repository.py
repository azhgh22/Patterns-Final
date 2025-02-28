from typing import Protocol

from playground.core.models.payments import Payment


class PaymentRepository(Protocol):
    def register_payment(self, payment: Payment) -> None:
        pass

    def get_payment(self, receipt_id: str) -> Payment | None:
        pass

    def get_all_payments(self) -> list[Payment]:
        pass
