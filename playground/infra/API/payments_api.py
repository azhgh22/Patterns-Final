from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.requests import Request
from starlette.status import HTTP_400_BAD_REQUEST

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
