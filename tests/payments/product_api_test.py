from fastapi.testclient import TestClient

from playground.core.services.interfaces.currency_converter_interface import ICurrencyConverter
from playground.runner.setup import SetupConfiguration, setup
from tests.payments.payment_service_test import ConverterMock


def get_http(converter: ICurrencyConverter) -> TestClient:
    return TestClient(setup(SetupConfiguration.for_testing(converter=converter)))


def test_should_convert_price() -> None:
    response = get_http(ConverterMock()).post(
        "/payments/calculate", json={"currency_id": "USD", "price": 20}
    )
    assert response.status_code == 200
    assert response.json() == 40
