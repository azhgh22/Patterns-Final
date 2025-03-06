from dataclasses import dataclass

from playground.core.enums.receipt_status import ReceiptStatus
from playground.core.enums.shift_state import ShiftState
from playground.core.models.payments import Payment
from playground.core.models.product import ProductReport
from playground.core.models.receipt import Receipt, ReceiptItem
from playground.core.models.revenue import Revenue
from playground.core.models.shift import Shift
from playground.core.models.x_report import XReport
from playground.core.services.classes.payment_service import PaymentService
from playground.core.services.classes.shift_service import ShiftService
from playground.infra.memory.in_memory.shift_in_memory_repository import ShiftInMemoryRepository


@dataclass
class PaymentsServiceMock(PaymentService):
    def __init__(self, payment: Payment = Payment("1", "GEL", 10)):
        self.payment = payment

    def get(self, receipt_id: str) -> Payment:
        return self.payment


def get_receipt() -> Receipt:
    return Receipt(
        "1",
        "1",
        ReceiptStatus.OPEN,
        [ReceiptItem("1", "1", 2, 6, 12), ReceiptItem("1", "2", 2, 4, 8)],
        20,
        10,
    )


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
    shift_list = [Shift("1", ShiftState.OPEN, [get_receipt()])]
    service = ShiftService(ShiftInMemoryRepository(shift_list))
    open_shift_id = service.get_open_shift_id()
    assert shift_list[0].id == open_shift_id


def test_add_receipt_to_closed_shift_should_fail() -> None:
    shift_list = [Shift("1", ShiftState.CLOSED, [])]
    service = ShiftService(ShiftInMemoryRepository(shift_list))
    receipt = Receipt("1", "", ReceiptStatus.OPEN, [], 20, 10)
    try:
        service.add_receipt(receipt)
        assert False
    except ValueError:
        assert True


def test_add_incorrect_receipt_to_shift_should_fail() -> None:
    shift_list = [Shift("1", ShiftState.OPEN, [])]
    service = ShiftService(ShiftInMemoryRepository(shift_list))
    try:
        service.add_receipt(Receipt("1", "", ReceiptStatus.CLOSED, [], 20, 10))
        assert False
    except ValueError:
        assert True


def test_add_receipt_to_shift() -> None:
    shift_list = [Shift("1", ShiftState.OPEN, [])]
    service = ShiftService(ShiftInMemoryRepository(shift_list))
    receipt = Receipt("1", "", ReceiptStatus.OPEN, [], 20, 10)
    updated_receipt = service.add_receipt(receipt)
    assert updated_receipt is not None
    assert updated_receipt.shift_id == "1"


def test_remove_receipt_from_closed_shift_should_fail() -> None:
    shift_list = [Shift("1", ShiftState.CLOSED, [get_receipt()])]
    service = ShiftService(ShiftInMemoryRepository(shift_list))
    try:
        service.remove_receipt("1", "1")
        assert False
    except ValueError:
        assert True


def test_remove_receipt_from_shift() -> None:
    shift_list = [Shift("1", ShiftState.OPEN, [get_receipt()])]
    service = ShiftService(ShiftInMemoryRepository(shift_list))
    assert service.remove_receipt("1", "1")


def test_close_incorrect_shift_should_fail() -> None:
    shift_list = [Shift("1", ShiftState.OPEN, [])]
    service = ShiftService(ShiftInMemoryRepository(shift_list))
    try:
        service.close("2")
        assert False
    except IndexError:
        assert True


def test_close_shift_with_open_receipt_should_fail() -> None:
    shift_list = [Shift("1", ShiftState.OPEN, [get_receipt()])]
    service = ShiftService(ShiftInMemoryRepository(shift_list))
    try:
        service.close("1")
        assert False
    except IndexError:
        assert True


def test_close_shift() -> None:
    shift_list = [Shift("1", ShiftState.OPEN, [])]
    service = ShiftService(ShiftInMemoryRepository(shift_list))
    assert service.close("1")
    assert shift_list[0].state == ShiftState.CLOSED


def test_x_report() -> None:
    x_report = XReport("1", 1, [ProductReport("1", 2)], [Revenue("GEL", 10)])
    receipt = Receipt("1", "1", ReceiptStatus.CLOSED, [ReceiptItem("1", "1", 2, 5, 10)], 10, 10)
    shift_list = [Shift("1", ShiftState.OPEN, [receipt])]
    service = ShiftService(ShiftInMemoryRepository(shift_list))

    assert service.get_x_report("1", PaymentsServiceMock()) == x_report


def test_x_report_on_non_existing_shift() -> None:
    service = ShiftService(ShiftInMemoryRepository())
    try:
        service.get_x_report("1", PaymentsServiceMock())
        assert False
    except IndexError:
        assert True


def test_should_return_z_report() -> None:
    x_report = XReport("2", 1, [ProductReport("1", 2)], [Revenue("GEL", 10)])
    receipt = Receipt("1", "1", ReceiptStatus.CLOSED, [ReceiptItem("1", "1", 2, 5, 10)], 10, 10)
    shift_list = [Shift("2", ShiftState.OPEN, [receipt])]
    service = ShiftService(ShiftInMemoryRepository(shift_list))

    assert service.get_z_report("2", PaymentsServiceMock()) == x_report
    assert shift_list[0].state == ShiftState.CLOSED
