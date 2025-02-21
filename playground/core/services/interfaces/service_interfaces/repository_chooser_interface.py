from typing import Protocol

from playground.core.services.interfaces.memory.product_repository import (
    ProductRepository,
)
from playground.core.services.interfaces.memory.receipt_repository import (
    ReceiptRepository,
)


class IRepositoryChooser(Protocol):
    def get_product_repo(self) -> ProductRepository:
        pass

    def get_receipt_repo(self) -> ReceiptRepository:
        pass
