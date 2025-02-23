from typing import Protocol

from playground.core.models.receipt import AddProductRequest, Receipt, ReceiptRequest
from playground.core.services.interfaces.service_interfaces.campaign_service_interface import (
    ICampaignService,
)
from playground.core.services.interfaces.service_interfaces.product_service_interface import (
    IProductService,
)
from playground.core.services.interfaces.service_interfaces.shift_service_interface import (
    IShiftService,
)


class IReceiptService(Protocol):
    def create(self, prod_req: ReceiptRequest, shift_service: IShiftService) -> Receipt:
        pass

    def close(self, campaign_service: ICampaignService, shift_service: IShiftService) -> Receipt:
        pass

    def delete(self, receipt_id: str, shift_service: IShiftService) -> None:
        pass

    def get(self, receipt_id: str) -> Receipt:
        pass

    def add_product(
        self,
        receipt_id: str,
        product: AddProductRequest,
        product_service: IProductService,
    ) -> Receipt:
        pass

    def get_shift_receipts(self, shift_id: str) -> list[Receipt]:
        pass
