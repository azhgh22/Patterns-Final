from typing import Protocol

from playground.core.models.receipt import (
    ReceiptResponse,
    ReceiptRequest,
    AddProductRequest,
)
from playground.core.services.interfaces.campaign_service_interface import (
    ICampaignService,
)
from playground.core.services.interfaces.product_service_interface import (
    IProductService,
)


class IReceptService(Protocol):
    def create(self, prod_req: ReceiptRequest) -> ReceiptResponse:
        pass

    def close(self, campaign_service: ICampaignService) -> ReceiptResponse:
        pass

    def delete(self, receipt_id: str) -> None:
        pass

    def get(self, receipt_id: str) -> ReceiptResponse:
        pass

    def add_product(
        self,
        receipt_id: str,
        product: AddProductRequest,
        product_service: IProductService,
    ) -> ReceiptResponse:
        pass
