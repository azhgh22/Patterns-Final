from typing import Protocol

from playground.core.models.product import ProductRequest, ProductResponse
from playground.core.models.receipt import ReceiptResponse, ReceiptRequest, AddProductRequest
from playground.core.services.interfaces.campaign_service_interface import ICampaignService
from playground.core.services.interfaces.product_service_interface import IProductService


class IReceptService(Protocol):

    def create(self, prod_req: ReceiptRequest) -> ReceiptResponse:
        pass

    def close(self, i_campaign: ICampaignService) -> ReceiptResponse :
        pass

    def delete(self, receipt_id: str) -> None:
        pass

    def get(self, receipt_id: str) -> ReceiptResponse:
        pass

    def add_product(self, receipt_id: str, product: AddProductRequest, i_product: IProductService) -> ReceiptResponse:
        pass
