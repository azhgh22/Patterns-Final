from mypy.semanal_shared import Protocol

from playground.core.models.payments import PaymentRequest


class IPaymentsService(Protocol):
    def calculate_payment(self, receipt_id: int, currency_id: int) -> int:
        pass

    def add_payment(self, payment_request: PaymentRequest) -> bool:
        pass
