from sqlite3 import Connection

from playground.core.models.product import Product
from playground.core.models.receipt import Receipt


class ReceiptSqlLiteRepository:
    def __init__(self, connection: Connection):
        self.connection = connection

    def store_receipt(self, receipt: Receipt) -> None:
        pass

    def contains_receipt(self, receipt_id: str) -> bool:
        pass

    # Returns True if receipt is successfully deleted
    def delete_receipt(self, receipt_id: str) -> bool:
        pass

    def get_receipt(self, receipt_id: str) -> Receipt | None:
        pass

    def add_product_to_receipt(
        self, receipt: Receipt, product: Product, quantity: int
    ) -> Receipt:
        pass

    def close_receipt(self, updated_receipt: Receipt) -> None:
        pass
