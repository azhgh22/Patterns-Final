import sqlite3
from dataclasses import dataclass

from playground.core.models.product import Product


@dataclass
class ProductSqlLiteRepository:
    connection: sqlite3.Connection

    def get_product_with_id(self, p_id: str) -> Product | None:
        pass

    def get_all_products(self) -> list[Product]:
        pass

    def update_price(self, p_id: str, price: int) -> bool:
        pass

    def store_product(self, prod: Product) -> None:
        pass

    def contains_product_with_barcode(self, barcode: str) -> bool:
        pass
