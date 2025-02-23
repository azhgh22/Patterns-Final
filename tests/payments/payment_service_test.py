from playground.core.models.receipt import Receipt
from playground.core.services.classes.payment_service import PaymentService
from playground.core.services.interfaces.service_interfaces.receipt_service_interface import (
    IReceiptService,
)

from forex_python.converter import CurrencyRates


class ReceiptServiceMock(IReceiptService):
    def get(self, receipt_id: str) -> Receipt:
        return Receipt("1", "open", [], 1000, 1000)


def test_env_works() -> None:
    assert True


def test_should_not_convert_total_into_unknown_currency() -> None:
    payment_service = PaymentService()
    result = payment_service.calculate_payment("1", "USD", ReceiptServiceMock())
    print(result)
