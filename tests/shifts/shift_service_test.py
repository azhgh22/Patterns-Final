from playground.core.enums.shift_state import ShiftState
from playground.core.models.receipt import Receipt, ReceiptItem
from playground.core.models.shift import Shift
from playground.core.services.classes.shift_service import ShiftService
from playground.infra.memory.in_memory.shift_in_memory_repository import ShiftInMemoryRepository


def test_env_works() -> None:
    assert True


def test_should_not_find_open_shift() -> None:
    assert ShiftService(ShiftInMemoryRepository()).get_open_shift_id() is None


def test_should_find_open_shift() -> None:
    service = ShiftService(ShiftInMemoryRepository())
    service.open()
    open_shift_id = service.get_open_shift_id()
    assert open_shift_id is not None


def test_two_open_should_fail() -> None:
    service = ShiftService(ShiftInMemoryRepository())
    service.open()
    try:
        service.open()
        assert False
    except ValueError:
        assert True


def test_should_get_stored_shift() -> None:
    receipt = Receipt(
        "1", "1", "open", [ReceiptItem("1", 2, 6, 12), ReceiptItem("2", 2, 4, 8)], 20, 10
    )
    shift_list = [Shift("1", ShiftState.OPEN, [receipt])]
    service = ShiftService(ShiftInMemoryRepository(shift_list))
    open_shift_id = service.get_open_shift_id()
    assert shift_list[0].id == open_shift_id


def test_add_receipt_to_closed_shift_should_fail() -> None:
    shift_list = [Shift("1", ShiftState.CLOSED, [])]
    service = ShiftService(ShiftInMemoryRepository(shift_list))
    receipt = Receipt("1", "", "open", [], 20, 10)
    try:
        service.add_receipt(receipt)
        assert False
    except ValueError:
        assert True


def test_add_incorrect_receipt_to_shift_should_fail() -> None:
    shift_list = [Shift("1", ShiftState.OPEN, [])]
    service = ShiftService(ShiftInMemoryRepository(shift_list))
    assert service.add_receipt(Receipt("1", "", "close", [], 20, 10)) is None


def test_add_receipt_to_shift() -> None:
    shift_list = [Shift("1", ShiftState.OPEN, [])]
    service = ShiftService(ShiftInMemoryRepository(shift_list))
    receipt = Receipt("1", "", "open", [], 20, 10)
    updated_receipt = service.add_receipt(receipt)
    assert updated_receipt is not None
    assert updated_receipt.shift_id == "1"


def test_remove_receipt_from_closed_shift_should_fail() -> None:
    receipt = Receipt(
        "1", "1", "closed", [ReceiptItem("1", 2, 6, 12), ReceiptItem("2", 2, 4, 8)], 20, 10
    )
    shift_list = [Shift("1", ShiftState.CLOSED, [receipt])]
    service = ShiftService(ShiftInMemoryRepository(shift_list))
    try:
        service.remove_receipt("1", "1")
        assert False
    except ValueError:
        assert True


def test_remove_receipt_from_shift() -> None:
    receipt = Receipt(
        "1", "1", "open", [ReceiptItem("1", 2, 6, 12), ReceiptItem("2", 2, 4, 8)], 20, 10
    )
    shift_list = [Shift("1", ShiftState.OPEN, [receipt])]
    service = ShiftService(ShiftInMemoryRepository(shift_list))
    assert service.remove_receipt("1", "1")
    # TODO: should I check x_report?


def test_close_incorrect_shift_should_fail() -> None:
    shift_list = [Shift("1", ShiftState.OPEN, [])]
    service = ShiftService(ShiftInMemoryRepository(shift_list))
    try:
        service.close("2")
        assert False
    except IndexError:
        assert True


def test_close_shift_with_open_receipt_should_fail() -> None:
    receipt = Receipt(
        "1", "1", "open", [ReceiptItem("1", 2, 6, 12), ReceiptItem("2", 2, 4, 8)], 20, 10
    )
    shift_list = [Shift("1", ShiftState.OPEN, [receipt])]
    service = ShiftService(ShiftInMemoryRepository(shift_list))
    assert service.close("1") is False


def test_close_shift() -> None:
    shift_list = [Shift("1", ShiftState.OPEN, [])]
    service = ShiftService(ShiftInMemoryRepository(shift_list))
    assert service.close("1")
