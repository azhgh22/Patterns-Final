from dataclasses import dataclass
from typing import List

from playground.core.enums.receipt_status import ReceiptStatus
from playground.core.models.product import Product


@dataclass
class ReceiptItem:
    product_id: str
    quantity: int
    price: int
    total: int

    def add_item(self, num_items: int) -> None:
        self.quantity += num_items
        self.total += self.price * num_items


@dataclass
class Receipt:
    id: str
    shift_id: str
    status: ReceiptStatus
    products: List[ReceiptItem]
    total: int
    discounted_total: int | None

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, type(self)):
            return False
        return self.id == other.id

    def get_receipt_item(self, product: Product) -> ReceiptItem | None:
        for p in self.products:
            if p.product_id == product.id:
                return p
        return None


@dataclass
class ReceiptRequest:
    status: ReceiptStatus


@dataclass
class AddProductRequest:
    id: str
    quantity: int
