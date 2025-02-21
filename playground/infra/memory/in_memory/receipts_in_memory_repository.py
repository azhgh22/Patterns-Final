from typing import List

from certifi import where

from playground.core.models.product import Product
from playground.core.models.receipt import Receipt, ReceiptResponse, ReceiptRequest, AddProductRequest, ReceiptItem
from playground.core.services.interfaces.memory.receipt_repository import ReceiptRepository


class ReceiptInMemoryRepository:
    def __init__(self, receipts: List[Receipt] | None = None) -> None:
        if receipts is None:
            receipts = []
        self.receipt_list = receipts

    def store_receipt(self , receipt: Receipt) -> None:
        self.receipt_list.append(receipt)

    def contains_receipt(self, receipt_id : str) -> bool:
        for receipt in self.receipt_list:
            if receipt.id == receipt_id:
                return True
        return False

    def delete_receipt(self, receipt_id : str) -> bool:
        for receipt in self.receipt_list:
            if receipt.id == receipt_id:
                self.receipt_list.remove(receipt)
                return True
        return False

    def get_receipt(self, receipt_id : str) -> Receipt | None:
        for receipt in self.receipt_list:
            if receipt.id == receipt_id:
                return receipt
        return None

    def add_product_to_receipt(self, receipt_id : str, product : Product , quantity : int) -> Receipt | None:
        receipt = self.get_receipt(receipt_id)
        if receipt is None or receipt.status is not "open":
            return None
        receipt.products.append(ReceiptItem(product.id , quantity , product.price , product.price * quantity))
        return receipt

