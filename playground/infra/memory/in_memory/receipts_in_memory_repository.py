from typing import List

from playground.core.models.product import Product
from playground.core.models.receipt import (
    Receipt,
    ReceiptItem,
)


class ReceiptInMemoryRepository:
    def __init__(self, receipts: List[Receipt] | None = None) -> None:
        if receipts is None:
            receipts = []
        self.receipt_list = receipts

    def store_receipt(self, receipt: Receipt) -> None:
        self.receipt_list.append(receipt)

    def contains_receipt(self, receipt_id: str) -> bool:
        for receipt in self.receipt_list:
            if receipt.id == receipt_id:
                return True
        return False

    def delete_receipt(self, receipt_id: str) -> bool:
        for receipt in self.receipt_list:
            if receipt.id == receipt_id:
                self.receipt_list.remove(receipt)
                return True
        return False

    def get_receipt(self, receipt_id: str) -> Receipt | None:
        for receipt in self.receipt_list:
            if receipt.id == receipt_id:
                return receipt
        return None

    def add_product_to_receipt(
        self, receipt: Receipt, product: Product, quantity: int
    ) -> Receipt:
        receipt_item = receipt.get_receipt_item(product)
        if receipt_item is None:
            receipt.products.append(
                ReceiptItem(product.id, quantity, product.price, product.price * quantity)
            )
        else:
            receipt_item.add_item(quantity)

        receipt.total += product.price * quantity
        return receipt

    def close_receipt(self, updated_receipt: Receipt) -> None:
        for r in self.receipt_list:
            if r.id == updated_receipt.id:
                r = updated_receipt

    def update_shift_id(self, shift_id: str, receipt_id: str) -> None:
        for receipt in self.receipt_list:
            if receipt.id == receipt_id:
                receipt.shift_id = shift_id

    def get_all_receipts(self, shift_id: str) -> list[Receipt]:
        new_list: list[Receipt] = []
        for receipt in self.receipt_list:
            if receipt.shift_id == shift_id:
                new_list.append(receipt)
        return new_list

    def clear_receipt_shift_id(self, receipt_id: str) -> bool:
        receipt = self.get_receipt(receipt_id)
        if receipt is None:
            return False
        receipt.shift_id = ""
        return True
