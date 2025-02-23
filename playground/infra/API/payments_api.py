from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.requests import Request
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from playground.core.models.payments import PaymentRequest, Payment
from playground.core.services.interfaces.service_interfaces.payments_service_interface import (
    IPaymentsService,
)
from playground.core.services.interfaces.service_interfaces.repository_chooser_interface import (
    IRepositoryChooser,
)
from playground.core.services.interfaces.service_interfaces.service_chooser_interface import (
    IServiceChooser,
)
from playground.infra.API.receipts_api import get_receipt_service

payments_api = APIRouter()


# TODO: gather all service getters in one place
def get_payment_service(request: Request) -> IPaymentsService:
    service_chooser: IServiceChooser = request.app.state.core
    repository_chooser: IRepositoryChooser = request.app.state.repo
    return service_chooser.get_payment_service(repository_chooser.get_payment_repository())


@payments_api.get("/", status_code=200)
def get_payment(request: Request, receipt_id: str) -> Payment:
    try:
        return get_payment_service(request).get(receipt_id)
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=str(e),
        )


class PaymentRequestModel(BaseModel):
    receipt_id: str
    currency_id: str


@payments_api.get("/calculate", status_code=200)
def calculate_payment(request: Request, payment: PaymentRequestModel) -> int:
    try:
        amount = get_payment_service(request).calculate_payment(
            payment.receipt_id, payment.currency_id, get_receipt_service(request)
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return amount


@payments_api.post("/register", status_code=201)
def add_payment(request: Request, payment: PaymentRequestModel) -> Payment:
    p_request = PaymentRequest(payment.receipt_id, payment.currency_id)
    try:
        new_payment = get_payment_service(request).add_payment(
            p_request, get_receipt_service(request)
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return new_payment
