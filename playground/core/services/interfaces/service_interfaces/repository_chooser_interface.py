from typing import Protocol

from playground.core.services.interfaces.memory import ShiftRepository
from playground.core.services.interfaces.memory.product_repository import (
    ProductRepository,
)


class IRepositoryChooser(Protocol):
    def get_product_repo(self) -> ProductRepository:
        pass

    def get_shift_repository(self) -> ShiftRepository:
        pass
