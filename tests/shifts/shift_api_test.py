from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from playground.core.enums.shift_state import ShiftState
from playground.core.models.shift import Shift
from playground.core.models.x_report import XReport
from playground.core.services.classes.repository_in_memory_chooser import InMemoryChooser
from playground.core.services.interfaces.memory.shift_repository import ShiftRepository
from playground.infra.memory.in_memory.shift_in_memory_repository import ShiftInMemoryRepository
from playground.runner.setup import SetupConfiguration, setup


def get_http(
    shift_repo: ShiftRepository = ShiftInMemoryRepository(),
) -> TestClient:
    return TestClient(
        setup(SetupConfiguration(repository_chooser=InMemoryChooser(shift_repo=shift_repo)))
    )


def test_open_shift() -> None:
    response = get_http().post("/shifts/open")
    assert response.status_code == HTTP_201_CREATED
    shift = Shift(**(response.json()))
    assert shift.receipts == []
    assert shift.state == ShiftState.OPEN


def test_close_shift() -> None:
    response = get_http(ShiftInMemoryRepository([Shift("1", ShiftState.OPEN, [])])).post(
        "/shifts/close/1"
    )
    assert response.status_code == HTTP_200_OK
    assert bool(response.json())


def test_close_non_existent_shift() -> None:
    response = get_http().post("/shifts/close/999")
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert "open shift doesn't exist" == response.json()["detail"]


def test_get_x_report_for_existing_shift() -> None:
    shift_repo = ShiftInMemoryRepository([Shift("1", ShiftState.OPEN, [])])
    response = get_http(shift_repo).get("/shifts/x-report/1")
    assert response.status_code == HTTP_200_OK
    assert isinstance(XReport(**response.json()), XReport)
    x_report = XReport(**response.json())
    assert x_report.shift_id == "1"
    assert x_report.num_receipts == 0


def test_get_x_report_for_non_existent_shift() -> None:
    response = get_http().get("/shifts/x-report/999")
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert "shift doesn't exist" == response.json()["detail"]


def test_open_shift_when_one_is_already_open() -> None:
    shift_repo = ShiftInMemoryRepository([Shift("1", ShiftState.OPEN, [])])
    response = get_http(shift_repo).post("/shifts/open")
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert "shift is already open" == response.json()["detail"]


def test_close_shift_that_is_not_open() -> None:
    shift_repo = ShiftInMemoryRepository([Shift("1", ShiftState.CLOSED, [])])
    response = get_http(shift_repo).post("/shifts/close/1")
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert "open shift doesn't exist" == response.json()["detail"]
