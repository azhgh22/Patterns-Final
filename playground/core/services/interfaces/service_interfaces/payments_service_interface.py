from typing import Protocol

from playground.core.models.payments import Payment
from playground.core.models.sales import SalesItem


class IPaymentsService(Protocol):
    def calculate_payment(self, currency_id: str, amount: int) -> int:
        pass

    def register_payment(self, payment_request: Payment) -> Payment:
        pass

    def get(self, receipt_id: str) -> Payment:
        pass

    def get_sales(self) -> list[SalesItem]:
        pass
