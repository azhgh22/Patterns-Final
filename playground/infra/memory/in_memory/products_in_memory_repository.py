from copy import deepcopy
from typing import List

from playground.core.models.product import Product


class ProductInMemoryRepository:
    def __init__(self, product_list: List[Product] = None) -> None:
        if product_list is None:
            product_list = []
        self.product_list = product_list

    def get_product_with_id(self, p_id: str) -> Product | None:
        for p in self.product_list:
            if p.id == p_id:
                return p
        return None

    def get_all_products(self) -> list[Product]:
        return deepcopy(self.product_list)

    def update_price(self, p_id: str, price: int) -> bool:
        for p in self.product_list:
            if p.id == p_id:
                p.price = price
                return True
        return False

    def store_product(self, prod: Product) -> None:
        self.product_list.append(deepcopy(prod))

    def contains_product_with_barcode(self, barcode: str) -> bool:
        for p in self.product_list:
            if p.barcode == barcode:
                return True
        return False
