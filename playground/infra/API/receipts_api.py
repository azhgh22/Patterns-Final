from fastapi import HTTPException
from typing import List

from starlette import status
from starlette.requests import Request
from pydantic import BaseModel

from fastapi import APIRouter

from playground.core.models.product import Product, ProductRequest
from playground.core.models.receipt import Receipt, ReceiptRequest, AddProductRequest
from playground.core.services.interfaces.service_interfaces.product_service_interface import IProductService
from playground.core.services.interfaces.service_interfaces.receipt_service_interface import IReceiptService
from playground.core.services.interfaces.service_interfaces.repository_chooser_interface import (
    IRepositoryChooser,
)
from playground.core.services.interfaces.service_interfaces.service_chooser_interface import (
    IServiceChooser,
)

receipts_api = APIRouter()

def get_product_service(request: Request) -> IProductService:
    service_chooser: IServiceChooser = request.app.state.core
    repository_chooser: IRepositoryChooser = request.app.state.repo
    return service_chooser.get_product_service(repository_chooser.get_product_repo())


def get_receipt_service(request: Request) -> IReceiptService:
    service_chooser: IServiceChooser = request.app.state.core
    repository_chooser: IRepositoryChooser = request.app.state.repo
    return service_chooser.get_receipt_service(repository_chooser.get_receipt_repo())

class ReceiptCreateRequest(BaseModel):
    status:str

@receipts_api.post("/" , status_code=status.HTTP_201_CREATED)
def create_receipt(request: Request , receipt_request: ReceiptCreateRequest) -> Receipt:
    receipt_req_model = ReceiptRequest(receipt_request.status)
    service = get_receipt_service(request)
    try:
        new_receipt = service.create(receipt_req_model)
        return Receipt(new_receipt.id , new_receipt.status , new_receipt.products)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@receipts_api.post("/{receipt_id}/products" , status_code=status.HTTP_200_OK)
def add_product(request: Request, receipt_id: str , add_product_request: AddProductRequest) -> Receipt:
    service = get_receipt_service(request)
    try:
        updated_receipt = service.add_product(receipt_id , add_product_request , get_product_service(request))
        return Receipt(updated_receipt.id , updated_receipt.status , updated_receipt.products)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))