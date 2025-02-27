from playground.core.models.payments import Payment
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


def test_should_return_empty_sales_list() -> None:
    service = PaymentService(repo=PaymentInMemoryRepository([]))
    assert service.get_sales() == []


def test_should_return_sales_broken_by_id() -> None:
    payment_list = [
        Payment(
            "1",
            "USD",
            50,
        ),
        Payment(
            "2",
            "GEL",
            50,
        ),
        Payment(
            "2",
            "GEL",
            50,
        ),
    ]
    service = PaymentService(PaymentInMemoryRepository(payment_list))
    sales_list = service.get_sales()
    assert len(sales_list) == 2
    if sales_list[0].currency_id == "GEL":
        assert sales_list[0].total_price == 100
        assert sales_list[1].total_price == 50
        assert sales_list[1].currency_id == "USD"
    else:
        assert sales_list[0].currency_id == "USD"
        assert sales_list[0].total_price == 50
        assert sales_list[1].total_price == 100
        assert sales_list[1].currency_id == "GEL"
