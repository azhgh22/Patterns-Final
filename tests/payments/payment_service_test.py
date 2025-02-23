from playground.core.models.payments import Payment, PaymentRequest
from playground.core.models.receipt import Receipt
from playground.core.services.classes.payment_service import PaymentService
from playground.core.services.interfaces.service_interfaces.receipt_service_interface import (
    IReceiptService,
)
from playground.infra.memory.in_memory.payment_in_memory_repository import (
    PaymentInMemoryRepository,
)


class ReceiptServiceMock(IReceiptService):
    def __init__(self, receipt: Receipt = Receipt("1", "open", [], 20, 10)) -> None:
        self.receipt = receipt

    def get(self, receipt_id: str) -> Receipt:
        return self.receipt


class ConverterMock:
    def convert(self, from_currency: str, to_currency: str, amount: float) -> float:
        if to_currency == "BLA":
            raise IndexError
        return amount * 2


def test_env_works() -> None:
    assert True


def test_should_not_convert_total_into_unknown_currency() -> None:
    payment_service = PaymentService(converter=ConverterMock())
    try:
        payment_service.calculate_payment("1", "BLA", ReceiptServiceMock())
    except IndexError:
        assert True


def test_should_convert_total_into_currency_closed_receipt() -> None:
    payment_service = PaymentService(converter=ConverterMock())
    result = payment_service.calculate_payment("1", "USD", ReceiptServiceMock())
    assert result == 20


def test_should_convert_open_receipt() -> None:
    payment_service = PaymentService(converter=ConverterMock())
    result = payment_service.calculate_payment(
        "1", "USD", ReceiptServiceMock(Receipt("1", "open", [], 20, None))
    )
    assert result == 40


def test_should_get_payment() -> None:
    payment = Payment("1", "USD", 32)
    payment_service = PaymentService(repo=PaymentInMemoryRepository([payment]))
    assert payment_service.get("1") == payment


def test_should_not_return_unknown_payment() -> None:
    try:
        PaymentService().get("1")
    except ValueError:
        assert True


def test_should_add_new_payment() -> None:
    payment_list: list[Payment] = []
    payment_service = PaymentService(PaymentInMemoryRepository(payment_list), ConverterMock())
    assert payment_service.register_payment(PaymentRequest("1", "USD"), ReceiptServiceMock())
    assert len(payment_list) == 1
    assert payment_list[0] == Payment("1", "USD", 20)
