from dataclasses import dataclass
from typing import List


class ReceiptItem:
    product_id: str
    quantity: int
    price: int
    total: int


class Receipt:
    id: str
    status: str
    products: List[ReceiptItem]

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, type(self)):
            return False
        return self.id == other.id

    def calculate_total(self) -> int:
        return sum(product.total for product in self.products)


@dataclass
class ReceiptRequest:
    status: str


@dataclass
class ReceiptResponse:
    id: str
    status: str
    products: List[ReceiptItem]
    total: int


@dataclass
class AddProductRequest:
    id: str
    quantity: int
