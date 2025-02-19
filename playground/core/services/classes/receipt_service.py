from uuid import uuid4

from pydantic.dataclasses import dataclass

from playground.core.models.receipt import ReceiptRequest, ReceiptResponse, AddProductRequest, Receipt
from playground.core.services.interfaces.memory.receipt_repository import ReceiptRepository
from playground.core.services.interfaces.service_interfaces.campaign_service_interface import ICampaignService
from playground.core.services.interfaces.service_interfaces.product_service_interface import IProductService
from playground.infra.memory.in_memory.receipts_in_memory_repository import ReceiptInMemoryRepository


@dataclass
class ReceiptService:
    receiptRepo: ReceiptRepository = ReceiptInMemoryRepository()

    def create(self, prod_req: ReceiptRequest) -> ReceiptResponse:
        if prod_req.status is not "open":
            raise ValueError
        receipt_id = str(uuid4())
        new_receipt = Receipt(receipt_id , "open" , [])
        self.receiptRepo.store_receipt(new_receipt)
        return ReceiptResponse(receipt_id , "open" , [] , 0)

    def close(self, campaign_service: ICampaignService) -> ReceiptResponse:
        pass

    def delete(self, receipt_id: str) -> None:
        if not self.receiptRepo.contains_receipt(receipt_id):
            raise ValueError
        self.receiptRepo.delete_receipt(receipt_id)

    def get(self, receipt_id: str) -> ReceiptResponse:
        receipt = self.receiptRepo.get_receipt(receipt_id)
        if receipt is None:
            raise ValueError
        return ReceiptResponse(receipt.id , receipt.status , receipt.products , receipt.calculate_total())

    def add_product(
            self,
            receipt_id: str,
            product_request: AddProductRequest,
            product_service: IProductService,
    ) -> ReceiptResponse:
        product = product_service.get_product(product_request.id)
        if product is None or not self.receiptRepo.contains_receipt(receipt_id):
            raise ValueError
        new_receipt = self.receiptRepo.add_product_to_receipt(receipt_id, product , product_request.quantity)
        return ReceiptResponse(new_receipt.id , "open" , new_receipt.l , 0)