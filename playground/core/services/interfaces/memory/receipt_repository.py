from typing import Protocol

from playground.core.models.receipt import Receipt, ReceiptItem


class ReceiptRepository(Protocol):
    def store_receipt(self, receipt: Receipt) -> None:
        pass

    def contains_receipt(self, receipt_id: str) -> bool:
        pass

    # Returns True if receipt is successfully deleted
    def delete_receipt(self, receipt_id: str) -> bool:
        pass

    def get_receipt(self, receipt_id: str) -> Receipt | None:
        pass

    def add_product_to_receipt(self, item: ReceiptItem) -> Receipt | None:
        pass

    def remove_item(self, item: ReceiptItem) -> None:
        pass

    def update_shift_id(self, shift_id: str, receipt_id: str) -> bool:
        pass

    def get_all_receipts(self, shift_id: str) -> list[Receipt]:
        pass

    def get_item(self, product_id: str, receipt_id: str) -> ReceiptItem | None:
        pass

    def update_receipt_price(self, receipt_id: str, price: int) -> None:
        pass
