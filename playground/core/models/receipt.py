from dataclasses import dataclass
from typing import List


@dataclass
class ReceiptItem:
    product_id: str
    quantity: int
    price: int
    total: int


@dataclass
class Receipt:
    id: str
    shift_id: str
    status: str
    products: List[ReceiptItem]
    total: int
    discounted_total: int

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, type(self)):
            return False
        return self.id == other.id


@dataclass
class ReceiptRequest:
    status: str


@dataclass
class AddProductRequest:
    id: str
    quantity: int
