from typing import List

from playground.core.enums.shift_state import ShiftState
from playground.core.models.product import Product
from playground.core.models.receipt import AddProductRequest, Receipt, ReceiptRequest
from playground.core.models.shift import Shift
from playground.core.services.classes.product_service import ProductService
from playground.core.services.classes.receipt_service import ReceiptService
from playground.core.services.interfaces.service_interfaces.shift_service_interface import (
    IShiftService,
)
from playground.infra.memory.in_memory.products_in_memory_repository import (
    ProductInMemoryRepository,
)
from playground.infra.memory.in_memory.receipts_in_memory_repository import (
    ReceiptInMemoryRepository,
)


class ShiftServiceMock(IShiftService):
    def __init__(self, shift: Shift = Shift("11", ShiftState.OPEN, [])):
        self.open_shift = shift
        self.closed_shifts: List[Shift] = []

    def get_open_shift_id(self) -> str | None:
        return self.open_shift.id

    def add_receipt(self, shift_id: str, receipt: Receipt) -> bool:
        if shift_id != self.open_shift.id or receipt is None:
            return False
        return True


def test_env_works() -> None:
    pass


def test_should_not_create_receipt_wrong_status() -> None:
    try:
        ReceiptService().create(ReceiptRequest("close"), ShiftServiceMock())
    except ValueError as e:
        assert "should be open" in str(e)


def test_should_store_receipt() -> None:
    new_receipt = ReceiptService().create(ReceiptRequest("open"), ShiftServiceMock())
    assert isinstance(new_receipt, Receipt)
    assert new_receipt is not None


def test_should_not_delete_non_existing_receipt() -> None:
    service = ReceiptService(ReceiptInMemoryRepository())

    try:
        service.delete("11", ShiftServiceMock)
    except ValueError as e:
        assert "does not exist" in str(e)


def test_should_delete_existing_receipt() -> None:
    rec_list = [Receipt("11", "open", [], 0, 0)]
    service = ReceiptService(ReceiptInMemoryRepository(rec_list))
    assert not service.delete("11", ShiftServiceMock())  # if there is no assertions its good
    assert len(rec_list) == 0


def test_should_not_get_non_existing_receipt() -> None:
    service = ReceiptService(ReceiptInMemoryRepository([]))

    try:
        service.get("11")
    except ValueError as e:
        assert "does not exist" in str(e)


def test_should_get_existing_receipt() -> None:
    service = ReceiptService(ReceiptInMemoryRepository([Receipt("11", "open", [], 0, 0)]))

    response = service.get("11")
    assert isinstance(response, Receipt)
    assert response.id == "11"


def test_should_not_add_non_existing_product_to_receipt() -> None:
    product_service = ProductService()
    product_request = AddProductRequest("1", 1)
    receipt = Receipt("11", "open", [], 0, 0)
    receipt_service = ReceiptService(ReceiptInMemoryRepository([receipt]))

    try:
        receipt_service.add_product("11", product_request, product_service)
    except ValueError as e:
        assert "does not exist" in str(e)


def test_should_not_add_product_to_non_existing_receipt() -> None:
    product_service = ProductService(
        ProductInMemoryRepository([Product("1", "vashli", "111", 2)])
    )
    product_request = AddProductRequest("1", 1)
    receipt_service = ReceiptService(ReceiptInMemoryRepository())
    try:
        receipt_service.add_product("11", product_request, product_service)
    except ValueError as e:
        assert "does not exist" in str(e)


def test_should_add_product_to_receipt() -> None:
    product_service = ProductService(
        ProductInMemoryRepository([Product("1", "vashli", "111", 2)])
    )
    product_request = AddProductRequest("1", 1)
    receipt = Receipt("11", "open", [], 0, 0)
    receipt_service = ReceiptService(ReceiptInMemoryRepository([receipt]))
    response = receipt_service.add_product("11", product_request, product_service)
    assert isinstance(response, Receipt)
    assert response.id == "11"
    assert len(response.products) == 1
    assert len(receipt.products) == 1


def test_should_not_add_product_to_not_opened_receipt() -> None:
    product_service = ProductService(
        ProductInMemoryRepository([Product("1", "vashli", "111", 2)])
    )
    product_request = AddProductRequest("1", 1)
    receipt_service = ReceiptService(
        ReceiptInMemoryRepository([Receipt("11", "closed", [], 0, 0)])
    )
    try:
        receipt_service.add_product("11", product_request, product_service)
    except ValueError as e:
        assert "should be open" in str(e)
