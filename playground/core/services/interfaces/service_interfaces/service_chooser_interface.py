from mypy.semanal_shared import Protocol

from playground.core.services.interfaces.memory.product_repository import (
    ProductRepository,
)
from playground.core.services.interfaces.service_interfaces.product_service_interface import (
    IProductService,
)


class IServiceChooser(Protocol):
    def get_product_service(self, product_repo: ProductRepository) -> IProductService:
        pass
