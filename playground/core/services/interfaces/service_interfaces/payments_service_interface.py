from typing import Protocol

from playground.core.models.payments import PaymentRequest, Payment
from playground.core.services.interfaces.service_interfaces.receipt_service_interface import (
    IReceiptService,
)


class IPaymentsService(Protocol):
    def calculate_payment(
        self, receipt_id: str, currency_id: str, receipt_service: IReceiptService
    ) -> int:
        pass

    def register_payment(
        self, payment_request: PaymentRequest, receipt_service: IReceiptService
    ) -> Payment:
        pass

    def get(self, receipt_id: str) -> Payment:
        pass
