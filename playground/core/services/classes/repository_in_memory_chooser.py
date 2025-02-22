from playground.core.services.interfaces.memory.product_repository import (
    ProductRepository,
)
from playground.core.services.interfaces.memory.shift_repository import ShiftRepository
from playground.infra.memory.in_memory.products_in_memory_repository import (
    ProductInMemoryRepository,
)
from playground.infra.memory.in_memory.shift_in_memory_repository import (
    ShiftInMemoryRepository,
)


class InMemoryChooser:
    def __init__(
        self,
        product_repo: ProductRepository = ProductInMemoryRepository(),
        shift_repo: ShiftRepository = ShiftInMemoryRepository(),
    ) -> None:
        self.product_repository = product_repo
        self.shift_repository = shift_repo

    def get_product_repo(self) -> ProductRepository:
        return self.product_repository

    def get_shift_repo(self) -> ShiftRepository:
        return self.shift_repository
