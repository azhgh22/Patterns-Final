from dataclasses import dataclass
from typing import List

from playground.core.models.product import ProductReport
from playground.core.models.revenue import Revenue


@dataclass
class XReport:
    id: str
    num_receipts: int
    products: List[ProductReport]
    revenue: List[Revenue]

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, type(self)):
            return False
        return (
            self.id == other.id
            and self.num_receipts == other.num_receipts
            and self.products == other.products
            and self.revenue == other.revenue
        )
