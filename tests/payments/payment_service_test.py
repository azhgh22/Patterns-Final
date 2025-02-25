from playground.core.models.payments import Payment
from playground.core.models.receipt import Receipt
from playground.core.services.classes.payment_service import PaymentService
from playground.infra.memory.in_memory.payment_in_memory_repository import (
    PaymentInMemoryRepository,
)


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
        payment_service.calculate_payment("BLA", 10)
    except IndexError:
        assert True


def test_should_convert_total_into_currency_closed_receipt() -> None:
    payment_service = PaymentService(converter=ConverterMock())
    result = payment_service.calculate_payment("USD", 10)
    assert result == 20


def test_should_convert_open_receipt() -> None:
    payment_service = PaymentService(converter=ConverterMock())
    result = payment_service.calculate_payment("USD", 20)
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
    assert payment_service.register_payment(Payment("1", "USD", 10))
    assert len(payment_list) == 1
    assert payment_list[0] == Payment("1", "USD", 20)
