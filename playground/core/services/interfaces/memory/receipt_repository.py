from typing import Protocol

from playground.core.models.product import Product
from playground.core.models.receipt import Receipt


class ReceiptRepository(Protocol):
    def store_receipt(self, receipt: Receipt) -> None:
        pass

    def contains_receipt(self, receipt_id : str) -> bool:
        pass

    # Returns True if receipt is successfully deleted
    def delete_receipt(self, receipt_id : str) -> bool:
        pass

    def get_receipt(self, receipt_id : str) -> Receipt | None:
        pass

    def add_product_to_receipt(self, receipt_id : str, product : Product , quantity: int) -> Receipt | None:
        pass

