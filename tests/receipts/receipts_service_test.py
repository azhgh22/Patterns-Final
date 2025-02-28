
from playground.core.enums.receipt_status import ReceiptStatus
from playground.core.enums.shift_state import ShiftState
from playground.core.models.product import Product
from playground.core.models.receipt import AddProductRequest, Receipt, ReceiptRequest
from playground.core.models.shift import Shift
from playground.core.services.classes.campaign_service import CampaignService
from playground.core.services.classes.payment_service import PaymentService
from playground.core.services.classes.product_service import ProductService
from playground.core.services.classes.receipt_service import ReceiptService
from playground.core.services.classes.shift_service import ShiftService
from playground.infra.memory.in_memory.products_in_memory_repository import (
    ProductInMemoryRepository,
)
from playground.infra.memory.in_memory.receipts_in_memory_repository import (
    ReceiptInMemoryRepository,
)
from playground.infra.memory.in_memory.shift_in_memory_repository import ShiftInMemoryRepository


def test_env_works() -> None:
    pass


def test_should_not_create_receipt_wrong_status() -> None:
    try:
        ReceiptService().create(ReceiptRequest(ReceiptStatus.CLOSED), ShiftService())
    except ValueError as e:
        assert "should be open" in str(e)


def test_should_store_receipt() -> None:
    shifts = [Shift("11", ShiftState.OPEN, [])]
    new_receipt = ReceiptService().create(
        ReceiptRequest(ReceiptStatus.OPEN), ShiftService(ShiftInMemoryRepository(shifts))
    )
    assert isinstance(new_receipt, Receipt)
    assert new_receipt is not None


def test_should_not_delete_non_existing_receipt() -> None:
    service = ReceiptService(ReceiptInMemoryRepository())

    try:
        service.delete("11", ShiftService())
    except ValueError as e:
        assert "does not exist" in str(e)


def test_should_delete_existing_receipt() -> None:
    rec_list = [Receipt("11", "", ReceiptStatus.OPEN, [], 0, None)]
    shift_list = [Shift("11", ShiftState.OPEN, [])]
    service = ReceiptService(ReceiptInMemoryRepository(rec_list))
    service.delete(
        "11", ShiftService(ShiftInMemoryRepository(shift_list))
    )  # if there is no assertions its good
    assert len(rec_list) == 0


def test_should_not_get_non_existing_receipt() -> None:
    service = ReceiptService(ReceiptInMemoryRepository([]))

    try:
        service.get("11")
    except ValueError as e:
        assert "does not exist" in str(e)


def test_should_get_existing_receipt() -> None:
    service = ReceiptService(
        ReceiptInMemoryRepository([Receipt("11", "", ReceiptStatus.OPEN, [], 0, None)])
    )

    response = service.get("11")
    assert isinstance(response, Receipt)
    assert response.id == "11"


def test_should_not_add_non_existing_product_to_receipt() -> None:
    product_service = ProductService()
    product_request = AddProductRequest("1", 1)
    receipt = Receipt("11", "", ReceiptStatus.OPEN, [], 0, None)
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
    receipt = Receipt("11", "", ReceiptStatus.OPEN, [], 0, None)
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
        ReceiptInMemoryRepository([Receipt("11", "", ReceiptStatus.CLOSED, [], 0, None)])
    )
    try:
        receipt_service.add_product("11", product_request, product_service)
    except ValueError as e:
        assert "should be open" in str(e)


def test_should_not_delete_open_receipt() -> None:
    receipt = Receipt("11", "", ReceiptStatus.CLOSED, [], 0, None)
    service = ReceiptService(ReceiptInMemoryRepository([receipt]))
    try:
        service.delete("11", ShiftService())
    except ValueError as e:
        assert "already Closed" in str(e)


def test_should_not_close_non_existing_receipt() -> None:
    try:
        service = ReceiptService(ReceiptInMemoryRepository([]))
        service.close("1", "1", CampaignService(), PaymentService())
        assert False
    except ValueError as e:
        assert "not found" in str(e)


def test_should_not_close_already_closed_receipt() -> None:
    receipt = Receipt("11", "", ReceiptStatus.CLOSED, [], 0, None)
    service = ReceiptService(ReceiptInMemoryRepository([receipt]))
    try:
        service.close("11", "1", CampaignService(), PaymentService())
        assert False
    except ValueError as e:
        assert "should not be closed" in str(e)


def test_should_close_receipt() -> None:
    receipt = Receipt("11", "", ReceiptStatus.OPEN, [], 0, None)
    service = ReceiptService(ReceiptInMemoryRepository([receipt]))
    updated_receipt = service.close("11", "GEL", CampaignService(), PaymentService())
    assert isinstance(updated_receipt, Receipt)
    assert updated_receipt.id == "11"
    assert updated_receipt.status == ReceiptStatus.CLOSED
