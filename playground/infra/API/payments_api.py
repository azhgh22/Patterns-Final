
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.requests import Request
from starlette.status import HTTP_400_BAD_REQUEST

from playground.core.services.interfaces.currency_converter_interface import ICurrencyConverter
from playground.core.services.interfaces.service_interfaces.payments_service_interface import (
    IPaymentsService,
)
from playground.core.services.interfaces.service_interfaces.repository_chooser_interface import (
    IRepositoryChooser,
)
from playground.core.services.interfaces.service_interfaces.service_chooser_interface import (
    IServiceChooser,
)

payments_api = APIRouter()


def get_payment_service(request: Request) -> IPaymentsService:
    service_chooser: IServiceChooser = request.app.state.core
    repository_chooser: IRepositoryChooser = request.app.state.repo
    converter: ICurrencyConverter = request.app.state.conv
    return service_chooser.get_payment_service(repository_chooser.get_payment_repo(), converter)


class PaymentRequestModel(BaseModel):
    currency_id: str
    price: int


@payments_api.post("/calculate", status_code=200)
def calculate_payment(request: Request, payment: PaymentRequestModel) -> int:
    try:
        amount = get_payment_service(request).calculate_payment(
            payment.currency_id, payment.price
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return amount
