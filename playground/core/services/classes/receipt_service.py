from dataclasses import dataclass
from uuid import uuid4

from playground.core.enums.receipt_status import ReceiptStatus
from playground.core.models.payments import Payment
from playground.core.models.receipt import (
    AddProductRequest,
    Receipt,
    ReceiptItem,
    ReceiptRequest,
)
from playground.core.services.interfaces.memory.receipt_repository import (
    ReceiptRepository,
)
from playground.core.services.interfaces.service_interfaces.campaign_service_interface import (
    ICampaignService,
)
from playground.core.services.interfaces.service_interfaces.payments_service_interface import (
    IPaymentsService,
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
    receipt_repo: ReceiptRepository = ReceiptInMemoryRepository()

    def create(self, prod_req: ReceiptRequest, shift_service: IShiftService) -> Receipt:
        if prod_req.status != "open":
            raise ValueError("Receipt status should be open.")

        receipt_id = str(uuid4())
        new_receipt = shift_service.add_receipt(
            Receipt(receipt_id, "", ReceiptStatus.OPEN, [], 0, None)
        )
        self.receipt_repo.store_receipt(new_receipt)
        return new_receipt

    def close(
        self,
        receipt_id: str,
        currency_id: str,
        campaign_service: ICampaignService,
        payment_service: IPaymentsService,
    ) -> Receipt:
        receipt = self.receipt_repo.get_receipt(receipt_id)
        if receipt is None:
            raise ValueError(f"Receipt with id {receipt_id} not found.")
        if receipt.status == ReceiptStatus.CLOSED:
            raise ValueError("Receipt status should not be closed.")
        updated_receipt = campaign_service.apply(receipt)
        total = (
            updated_receipt.discounted_total
            if updated_receipt.discounted_total
            else updated_receipt.total
        )
        payment = Payment(receipt_id, currency_id, total)
        payment_service.register_payment(payment)
        updated_receipt.status = ReceiptStatus.CLOSED
        self.receipt_repo.delete_receipt(receipt_id)
        self.receipt_repo.store_receipt(updated_receipt)
        return updated_receipt

    def delete(self, receipt_id: str, shift_service: IShiftService) -> None:
        receipt = self.receipt_repo.get_receipt(receipt_id)
        if receipt is None:
            raise ValueError(f"Receipt with id {receipt_id} does not exist.")
        if receipt.status == ReceiptStatus.CLOSED:
            raise ValueError("Receipt is already Closed.")
        shift_service.remove_receipt(receipt_id, receipt.shift_id)
        self.receipt_repo.delete_receipt(receipt_id)

    def get(self, receipt_id: str) -> Receipt:
        receipt = self.receipt_repo.get_receipt(receipt_id)
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
        receipt = self.receipt_repo.get_receipt(receipt_id)
        if product is None:
            raise ValueError(f"Product with id {product_request.id} does not exist.")
        elif receipt is None:
            raise ValueError(f"Receipt with id {receipt_id} does not exist.")
        elif receipt.status != ReceiptStatus.OPEN:
            raise ValueError("Receipt status should be open.")

        total = product.price * product_request.quantity
        new_item = ReceiptItem(
            receipt.id, product.id, product_request.quantity, product.price, total
        )

        item = self.receipt_repo.get_item(product.id, receipt_id)
        if item is not None:
            new_item.quantity += item.quantity
            new_item.total += item.total
            self.receipt_repo.remove_item(item)

        self.receipt_repo.update_receipt_price(receipt_id, receipt.total + total)
        receipt = self.receipt_repo.add_product_to_receipt(new_item)
        if receipt is None:
            raise ValueError(f"Receipt with id {receipt_id} does not exist.")
        return receipt
