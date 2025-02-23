from dataclasses import dataclass
import requests

from playground.core.models.payments import PaymentRequest, Payment
from playground.core.services.interfaces.memory.payment_repository import PaymentRepository
from playground.core.services.interfaces.service_interfaces.receipt_service_interface import (
    IReceiptService,
)
from playground.infra.memory.in_memory.payment_in_memory_repository import (
    PaymentInMemoryRepository,
)


@dataclass
class PaymentService:
    repo: PaymentRepository = PaymentInMemoryRepository()

    def calculate_payment(
        self, receipt_id: str, currency_id: str, receipt_service: IReceiptService
    ) -> int:
        receipt = receipt_service.get(receipt_id)
        total = (
            receipt.discounted_total if receipt.discounted_total is not None else receipt.total
        )
        url = "https://open.er-api.com/v6/latest/GEL"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Failed to fetch currency rates.")

        data = response.json()
        rates = data.get("rates", {})

        if currency_id not in rates:
            raise IndexError(f"Currency {currency_id} is not supported.")

        conversion_rate = rates[currency_id]
        converted_total = total * conversion_rate

        return int(round(converted_total))

    # TODO: receipt should get closed after registering payment
    def register_payment(
        self, payment_request: PaymentRequest, receipt_service: IReceiptService
    ) -> Payment:
        amount_in_currency = self.calculate_payment(
            payment_request.receipt_id, payment_request.currency_id, receipt_service
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
