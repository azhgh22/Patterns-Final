from typing import Protocol

from playground.core.models.receipt import (
    AddProductRequest,
    ReceiptRequest,
    ReceiptResponse,
)
from playground.core.services.interfaces.service_interfaces.campaign_service_interface import (
    ICampaignService,
)
from playground.core.services.interfaces.service_interfaces.product_service_interface import (
    IProductService,
)


class IReceiptService(Protocol):
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
