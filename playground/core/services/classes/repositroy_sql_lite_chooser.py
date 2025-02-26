import sqlite3

from playground.core.services.interfaces.memory.payment_repository import PaymentRepository
from playground.core.services.interfaces.memory.product_repository import (
    ProductRepository,
)
from playground.core.services.interfaces.memory.receipt_repository import ReceiptRepository
from playground.core.services.interfaces.memory.shift_repository import ShiftRepository
from playground.infra.memory.sql_lite.payment_sql_lite_repository import PaymentSqlLiteRepository
from playground.infra.memory.sql_lite.product_sql_lite_repository import (
    ProductSqlLiteRepository,
)
from playground.infra.memory.sql_lite.receipt_sql_lite_repository import ReceiptSqlLiteRepository
from playground.infra.memory.sql_lite.shift_sql_lite_repository import ShiftSqlLiteRepository


class SqlLiteChooser:
    def __init__(self) -> None:
        connection = sqlite3.connect("shop.db", check_same_thread=False)
        self.product_repository = ProductSqlLiteRepository(connection)
        self.payment_repository = PaymentSqlLiteRepository(connection)
        self.receipt_repository = ReceiptSqlLiteRepository(connection)
        self.shift_repository = ShiftSqlLiteRepository(connection, self.receipt_repository)

    def get_product_repo(self) -> ProductRepository:
        return self.product_repository

    def get_receipt_repo(self) -> ReceiptRepository:
        return self.receipt_repository

    def get_shift_repo(self) -> ShiftRepository:
        return self.shift_repository

    def get_payment_repo(self) -> PaymentRepository:
        return self.payment_repository
