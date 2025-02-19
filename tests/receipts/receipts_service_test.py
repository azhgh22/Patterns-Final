from playground.core.models.receipt import ReceiptRequest
from playground.core.services.classes.receipt_service import ReceiptService


def test_env_works() -> None:
    pass

def test_should_not_create_receipt_wrong_status() -> None:
    assert ReceiptService().create(ReceiptRequest("close")) is None
