from starlette.testclient import TestClient

from playground.core.enums.receipt_status import ReceiptStatus
from playground.core.enums.shift_state import ShiftState
from playground.core.models.product import Product
from playground.core.models.receipt import Receipt
from playground.core.models.shift import Shift
from playground.core.services.classes.repository_in_memory_chooser import (
    InMemoryChooser,
)
from playground.core.services.interfaces.memory.product_repository import (
    ProductRepository,
)
from playground.core.services.interfaces.memory.receipt_repository import (
    ReceiptRepository,
)
from playground.core.services.interfaces.memory.shift_repository import ShiftRepository
from playground.infra.memory.in_memory.products_in_memory_repository import (
    ProductInMemoryRepository,
)
from playground.infra.memory.in_memory.receipts_in_memory_repository import (
    ReceiptInMemoryRepository,
)
from playground.infra.memory.in_memory.shift_in_memory_repository import ShiftInMemoryRepository
from playground.runner.setup import SetupConfiguration, setup


def get_http(
    product_repo: ProductRepository = ProductInMemoryRepository(),
    receipt_repo: ReceiptRepository = ReceiptInMemoryRepository(),
    shift_repo: ShiftRepository = ShiftInMemoryRepository(),
) -> TestClient:
    return TestClient(
        setup(
            SetupConfiguration(
                repository_chooser=InMemoryChooser(
                    product_repo=product_repo, receipt_repo=receipt_repo, shift_repo=shift_repo
                )
            )
        )
    )


def test_should_not_create_receipt() -> None:
    try:
        get_http().post("/receipts", json={"status": "close"})
    except ValueError as e:
        assert "should be open" in str(e)


def test_should_create_receipt() -> None:
    receipts_list: list[Receipt] = []
    shifts_list = [Shift("11", ShiftState.OPEN, [])]
    response = get_http(
        receipt_repo=ReceiptInMemoryRepository(receipts_list),
        shift_repo=ShiftInMemoryRepository(shifts_list),
    ).post("/receipts", json={"status": "open"})
    assert response is not None
    assert response.status_code == 201
    assert len(receipts_list) == 1
    assert receipts_list[0] is not None
    assert receipts_list[0].status == "open"


def test_should_not_add_non_existing_product() -> None:
    receipts_list = [Receipt("1", "", ReceiptStatus.OPEN, [], 0, None)]
    response = get_http(receipt_repo=ReceiptInMemoryRepository(receipts_list)).post(
        "receipts/11/products", json={"id": "11", "quantity": 3}
    )
    assert "does not exist" in response.json()["detail"]
    assert response.status_code == 400


def test_should_not_add_product_to_non_existing_receipt() -> None:
    product_list = [Product("1", "vashli", "111", 4)]
    response = get_http(product_repo=ProductInMemoryRepository(product_list)).post(
        "/receipts/11/products", json={"id": "1", "quantity": 3}
    )
    assert "does not exist" in response.json()["detail"]
    assert response.status_code == 400


def test_should_not_add_product_to_closed_receipt() -> None:
    product_list = [Product("1", "vashli", "111", 4)]
    receipt_list = [Receipt("11", "", ReceiptStatus.CLOSED, [], 0, None)]
    response = get_http(
        product_repo=ProductInMemoryRepository(product_list),
        receipt_repo=ReceiptInMemoryRepository(receipt_list),
    ).post("receipts/11/products", json={"id": "1", "quantity": 3})
    assert "should be open" in response.json()["detail"]
    assert response.status_code == 400


def test_should_add_product_to_receipt() -> None:
    receipt_list = [Receipt("11", "", ReceiptStatus.OPEN, [], 0, None)]
    product_list = [Product("1", "vashli", "111", 4)]
    response = get_http(
        product_repo=ProductInMemoryRepository(product_list),
        receipt_repo=ReceiptInMemoryRepository(receipt_list),
    ).post("receipts/11/products", json={"id": "1", "quantity": 3})
    assert response.status_code == 200
    assert len(receipt_list[0].products) == 1
    assert receipt_list[0].products[0].product_id == "1"


def test_should_not_delete_non_existing_receipt() -> None:
    response = get_http().delete("/receipts/11")
    assert response.status_code == 400
    assert "does not exist" in response.json()["detail"]


def test_should_not_delete_closed_receipt() -> None:
    receipts_list = [Receipt("11", "", ReceiptStatus.CLOSED, [], 0, None)]
    response = get_http(receipt_repo=ReceiptInMemoryRepository(receipts_list)).delete(
        "/receipts/11"
    )
    assert response.status_code == 400
    assert "already Closed" in response.json()["detail"]
