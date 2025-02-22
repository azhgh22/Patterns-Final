from dataclasses import dataclass
from uuid import uuid4

from playground.core.models.receipt import (
    AddProductRequest,
    Receipt,
    ReceiptRequest,
    ReceiptResponse,
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

    def create(self, prod_req: ReceiptRequest, shift_service: IShiftService) -> ReceiptResponse:
        if prod_req.status != "open":
            raise ValueError("Receipt status should be open.")
        shift_id = shift_service.get_open_shift_id()
        if shift_id is None:
            raise ValueError("There Are No Open Shifts To Create Receipt.")
        receipt_id = str(uuid4())
        new_receipt = Receipt(receipt_id, "open", [], 0, None)
        self.receiptRepo.store_receipt(new_receipt)
        shift_service.add_receipt(shift_id, new_receipt)
        return ReceiptResponse(receipt_id, "open", [], 0, None)

    def close(self, campaign_service: ICampaignService) -> ReceiptResponse:
        pass

    def delete(self, receipt_id: str) -> None:
        if not self.receiptRepo.contains_receipt(receipt_id):
            raise ValueError(f"Receipt with id {receipt_id} does not exist.")
        self.receiptRepo.delete_receipt(receipt_id)

    def get(self, receipt_id: str) -> ReceiptResponse:
        receipt = self.receiptRepo.get_receipt(receipt_id)
        if receipt is None:
            raise ValueError(f"Receipt with id {receipt_id} does not exist.")
        return ReceiptResponse(
            receipt.id, receipt.status, receipt.products, receipt.total, receipt.discounted_total
        )

    def add_product(
        self,
        receipt_id: str,
        product_request: AddProductRequest,
        product_service: IProductService,
    ) -> ReceiptResponse:
        product = product_service.get_product(product_request.id)
        if product is None:
            raise ValueError(f"Product with id {product_request.id} does not exist.")
        elif not self.receiptRepo.contains_receipt(receipt_id):
            raise ValueError(f"Receipt with id {receipt_id} does not exist.")
        elif self.receiptRepo.get_receipt(receipt_id).status != "open":
            raise ValueError("Receipt status should be open.")
        new_receipt = self.receiptRepo.add_product_to_receipt(
            receipt_id, product, product_request.quantity
        )
        return ReceiptResponse(
            new_receipt.id,
            "open",
            new_receipt.products,
            new_receipt.total,
            new_receipt.discounted_total,
        )
