import sqlite3

from playground.core.services.interfaces.memory.payment_repository import PaymentRepository
from playground.core.services.interfaces.memory.product_repository import (
    ProductRepository,
)
from playground.core.services.interfaces.memory.receipt_repository import ReceiptRepository
from playground.core.services.interfaces.memory.shift_repository import ShiftRepository
from playground.infra.memory.sql_lite.product_sql_lite_repository import (
    ProductSqlLiteRepository,
)


class SqlLiteChooser:
    def __init__(self) -> None:
        connection = sqlite3.connect("shop.db", check_same_thread=False)
        self.product_repository = ProductSqlLiteRepository(connection)

    def get_product_repo(self) -> ProductRepository:
        return self.product_repository

    def get_receipt_repo(self) -> ReceiptRepository:
        pass

    def get_shift_repository(self) -> ShiftRepository:
        pass

    def get_payment_repository(self) -> PaymentRepository:
        pass
