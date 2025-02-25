from dataclasses import dataclass
from uuid import uuid4

from playground.core.enums.receipt_status import ReceiptStatus
from playground.core.models.receipt import (
    AddProductRequest,
    Receipt,
    ReceiptRequest,
)
from playground.core.services.interfaces.memory.receipt_repository import (
    ReceiptRepository,
)
from playground.core.services.interfaces.service_interfaces.campaign_service_interface import (
    ICampaignService,
)
from playground.core.services.interfaces.service_interfaces.product_service_interface import (
    IProductService,
)
from playground.core.services.interfaces.service_interfaces.shift_service_interface import (
    IShiftService,
)
from playground.infra.memory.in_memory.receipts_in_memory_repository import (
    ReceiptInMemoryRepository,
)


@dataclass
class ReceiptService:
    receiptRepo: ReceiptRepository = ReceiptInMemoryRepository()

    def create(self, prod_req: ReceiptRequest, shift_service: IShiftService) -> Receipt:
        if prod_req.status != "open":
            raise ValueError("Receipt status should be open.")

        receipt_id = str(uuid4())
        new_receipt = shift_service.add_receipt(
            Receipt(receipt_id, "", ReceiptStatus.OPEN, [], 0, None)
        )
        self.receiptRepo.store_receipt(new_receipt)
        return new_receipt

    def close(self, campaign_service: ICampaignService, shift_service: IShiftService) -> Receipt:
        pass

    def delete(self, receipt_id: str, shift_service: IShiftService) -> None:
        receipt = self.receiptRepo.get_receipt(receipt_id)
        if receipt is None:
            raise ValueError(f"Receipt with id {receipt_id} does not exist.")
        if receipt.status == ReceiptStatus.CLOSED:
            raise ValueError("Receipt is already Closed.")
        shift_service.remove_receipt(receipt_id, receipt.shift_id)
        self.receiptRepo.delete_receipt(receipt_id)

    def get(self, receipt_id: str) -> Receipt:
        receipt = self.receiptRepo.get_receipt(receipt_id)
        if receipt is None:
            raise ValueError(f"Receipt with id {receipt_id} does not exist.")
        return receipt

    def add_product(
        self,
        receipt_id: str,
        product_request: AddProductRequest,
        product_service: IProductService,
    ) -> Receipt:
        product = product_service.get_product(product_request.id)
        receipt = self.receiptRepo.get_receipt(receipt_id)
        if product is None:
            raise ValueError(f"Product with id {product_request.id} does not exist.")
        elif receipt is None:
            raise ValueError(f"Receipt with id {receipt_id} does not exist.")
        elif receipt.status != ReceiptStatus.OPEN:
            raise ValueError("Receipt status should be open.")
        return self.receiptRepo.add_product_to_receipt(
            receipt, product, product_request.quantity
        )
