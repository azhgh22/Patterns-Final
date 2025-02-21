from playground.core.services.interfaces.memory.product_repository import (
    ProductRepository,
)
from playground.core.services.interfaces.memory.receipt_repository import ReceiptRepository
from playground.infra.memory.in_memory.products_in_memory_repository import (
    ProductInMemoryRepository,
)
from playground.infra.memory.in_memory.receipts_in_memory_repository import ReceiptInMemoryRepository


class InMemoryChooser:
    def __init__(
        self, product_repo: ProductRepository = ProductInMemoryRepository() , receipt_repo: ReceiptRepository = ReceiptInMemoryRepository()
    ) -> None:
        self.product_repository = product_repo
        self.receipt_repository = receipt_repo

    def get_product_repo(self) -> ProductRepository:
        return self.product_repository

    def get_receipt_repo(self) -> ReceiptRepository:
        return self.receipt_repository
