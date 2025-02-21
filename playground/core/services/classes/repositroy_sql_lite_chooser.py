import sqlite3

from playground.core.services.interfaces.memory.product_repository import (
    ProductRepository,
)
from playground.infra.memory.sql_lite.product_sql_lite_repository import (
    ProductSqlLiteRepository,
)


class SqlLiteChooser:
    def __init__(self) -> None:
        connection = sqlite3.connect("shop.db", check_same_thread=False)
        self.product_repository = ProductSqlLiteRepository(connection)

    def get_product_repo(self) -> ProductRepository:
        return self.product_repository
