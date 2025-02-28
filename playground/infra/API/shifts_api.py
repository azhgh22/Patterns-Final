from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.requests import Request
from starlette.status import HTTP_400_BAD_REQUEST

from playground.core.models.shift import Shift
from playground.core.models.x_report import XReport
from playground.core.services.interfaces.service_interfaces.repository_chooser_interface import (
    IRepositoryChooser,
)
from playground.core.services.interfaces.service_interfaces.service_chooser_interface import (
    IServiceChooser,
)
from playground.core.services.interfaces.service_interfaces.shift_service_interface import (
    IShiftService,
)
from playground.infra.API.payments_api import get_payment_service

shifts_api = APIRouter()


def get_shifts_service(request: Request) -> IShiftService:
    service_chooser: IServiceChooser = request.app.state.core
    repository_chooser: IRepositoryChooser = request.app.state.repo
    return service_chooser.get_shift_service(repository_chooser.get_shift_repo())


class PaymentRequestModel(BaseModel):
    receipt_id: str
    currency_id: str


@shifts_api.post("/open", status_code=201)
def open_shift(request: Request) -> Shift:
    try:
        return get_shifts_service(request).open()
    except ValueError as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@shifts_api.post("/close/{shift_id}", status_code=200)
def close_shift(request: Request, shift_id: str) -> XReport:
    try:
        if get_shifts_service(request).close(shift_id):
            return get_shifts_service(request).get_x_report(
                shift_id, get_payment_service(request)
            )
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="closing shift failed",
        )
    except IndexError as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@shifts_api.get("/x-report/{shift_id}", status_code=200)
def get_x_report(request: Request, shift_id: str) -> XReport:
    try:
        return get_shifts_service(request).get_x_report(shift_id, get_payment_service(request))
    except IndexError as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
