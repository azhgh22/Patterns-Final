from playground.core.services.interfaces.memory.product_repository import (
    ProductRepository,
)
from playground.infra.memory.in_memory.products_in_memory_repository import (
    ProductInMemoryRepository,
)


class InMemoryChooser:
    def __init__(
        self, product_repo: ProductRepository = ProductInMemoryRepository()
    ) -> None:
        self.product_repository = product_repo

    def get_product_repo(self) -> ProductRepository:
        return self.product_repository
