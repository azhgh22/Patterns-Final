from fastapi import APIRouter
from starlette import status

from playground.core.models.receipt import Receipt

receipts_api = APIRouter()

@receipts_api.post("" , status_code=status.HTTP_201_CREATED)
def create_receipt():
    pass

@receipts_api.post("/{receipt_id}/products" , status_code=status.HTTP_200_OK)
def add_product_to_receipt():
    pass

@receipts_api.post("/{receipt_id}/quotes" ,status_code=status.HTTP_200_OK)
def calculate_product_quote():
    pass

@receipts_api.post("/{receipt_id}/payments" , status_code=status.HTTP_200_OK)
def add_payment_to_receipt():
    pass

