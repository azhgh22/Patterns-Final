from typing import List

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

    def add_product_to_receipt(self, item: ReceiptItem) -> Receipt | None:
        receipt = self.get_receipt(item.receipt_id)
        if receipt is not None:
            receipt.products.append(item)

        return self.get_receipt(item.receipt_id)

    def update_receipt_price(self, receipt_id: str, price: int) -> None:
        receipt = self.get_receipt(receipt_id)
        if receipt is not None:
            receipt.total = price

    def update_shift_id(self, shift_id: str, receipt_id: str) -> bool:
        for receipt in self.receipt_list:
            if receipt.id == receipt_id:
                receipt.shift_id = shift_id
                return True
        return False

    def get_all_receipts(self, shift_id: str) -> list[Receipt]:
        new_list: list[Receipt] = []
        for receipt in self.receipt_list:
            if receipt.shift_id == shift_id:
                new_list.append(receipt)
        return new_list

    def get_item(self, product_id: str, receipt_id: str) -> ReceiptItem | None:
        receipt = self.get_receipt(receipt_id)
        if receipt is None:
            return None

        for item in receipt.products:
            if product_id == item.product_id:
                return item

        return None

    def remove_item(self, item: ReceiptItem) -> None:
        receipt = self.get_receipt(item.receipt_id)
        if receipt is not None:
            receipt.products.remove(item)

    def close(self, updated_receipt: Receipt) -> None:
        receipt = self.get_receipt(updated_receipt.id)
        if receipt is None:
            return
        receipt.status = updated_receipt.status
        receipt.discounted_total = updated_receipt.discounted_total
        receipt.products = updated_receipt.products
