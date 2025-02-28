from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request

from playground.core.enums.receipt_status import ReceiptStatus
from playground.core.models.receipt import AddProductRequest, Receipt, ReceiptRequest
from playground.core.services.interfaces.service_interfaces.receipt_service_interface import (
    IReceiptService,
)
from playground.core.services.interfaces.service_interfaces.repository_chooser_interface import (
    IRepositoryChooser,
)
from playground.core.services.interfaces.service_interfaces.service_chooser_interface import (
    IServiceChooser,
)
from playground.core.services.interfaces.service_interfaces.shift_service_interface import (
    IShiftService,
)
from playground.infra.API.campaigns_api import get_campaign_service
from playground.infra.API.payments_api import get_payment_service
from playground.infra.API.products_api import get_product_service

receipts_api = APIRouter()


def get_receipt_service(request: Request) -> IReceiptService:
    service_chooser: IServiceChooser = request.app.state.core
    repository_chooser: IRepositoryChooser = request.app.state.repo
    return service_chooser.get_receipt_service(repository_chooser.get_receipt_repo())


def get_shift_service(request: Request) -> IShiftService:
    service_chooser: IServiceChooser = request.app.state.core
    repository_chooser: IRepositoryChooser = request.app.state.repo
    return service_chooser.get_shift_service(repository_chooser.get_shift_repo())


class ReceiptCreateRequest(BaseModel):
    status: ReceiptStatus


@receipts_api.post("/", status_code=status.HTTP_201_CREATED)
def create_receipt(request: Request, receipt_request: ReceiptCreateRequest) -> Receipt:
    receipt_req_model = ReceiptRequest(receipt_request.status)
    receipt_service = get_receipt_service(request)
    try:
        return receipt_service.create(receipt_req_model, get_shift_service(request))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@receipts_api.post("/{receipt_id}/products", status_code=status.HTTP_200_OK)
def add_product(
    request: Request, receipt_id: str, add_product_request: AddProductRequest
) -> Receipt:
    service = get_receipt_service(request)
    try:
        return service.add_product(receipt_id, add_product_request, get_product_service(request))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@receipts_api.delete("/{receipt_id}", status_code=status.HTTP_200_OK)
def delete_receipt(request: Request, receipt_id: str) -> None:
    service = get_receipt_service(request)
    try:
        service.delete(receipt_id, get_shift_service(request))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@receipts_api.post("/{receipt_id}/close", status_code=status.HTTP_200_OK)
def close_receipt(request: Request, receipt_id: str, currency_id: str) -> Receipt:
    service = get_receipt_service(request)
    try:
        res = service.close(
            receipt_id, currency_id, get_campaign_service(request), get_payment_service(request)
        )
        return res
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
