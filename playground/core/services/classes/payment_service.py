from dataclasses import dataclass

from playground.core.models.payments import Payment
from playground.core.services.interfaces.currency_converter_interface import ICurrencyConverter
from playground.core.services.interfaces.memory.payment_repository import PaymentRepository
from playground.infra.currency_converter.er_api_converter import ErApiConverter
from playground.infra.memory.in_memory.payment_in_memory_repository import (
    PaymentInMemoryRepository,
)


@dataclass
class PaymentService:
    repo: PaymentRepository = PaymentInMemoryRepository()
    converter: ICurrencyConverter = ErApiConverter()

    def calculate_payment(self, currency_id: str, amount: int) -> int:
        converted_total = self.converter.convert("GEL", currency_id, amount)
        return int(round(converted_total))

    def register_payment(
        self,
        payment_request: Payment,
    ) -> Payment:
        amount_in_currency = self.calculate_payment(
            payment_request.currency_id, payment_request.amount
        )
        payment = Payment(
            payment_request.receipt_id,
            payment_request.currency_id,
            amount_in_currency,
        )
        self.repo.register_payment(payment)
        return payment

    def get(self, receipt_id: str) -> Payment:
        payment = self.repo.get_payment(receipt_id)
        if payment is None:
            raise ValueError(f"Payment with receipt_id {receipt_id} does not exist.")
        return payment
