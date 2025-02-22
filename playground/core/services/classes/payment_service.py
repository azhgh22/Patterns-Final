from dataclasses import dataclass

from playground.core.models.payments import PaymentRequest
from playground.core.services.interfaces.memory.payment_repository import PaymentRepository
from playground.infra.memory.payment_in_memory_repository import PaymentInMemoryRepository


@dataclass
class PaymentService:
    repo: PaymentRepository = PaymentInMemoryRepository()

    def calculate_payment(self, receipt_id: int, currency_id: int) -> int:
        pass

    def add_payment(self, payment_request: PaymentRequest) -> bool:
        pass
