from playground.core.services.classes.product_service import ProductService
from playground.core.services.interfaces.memory.product_repository import (
    ProductRepository,
)
from playground.core.services.interfaces.service_interfaces.product_service_interface import (
    IProductService,
)


class ServiceChooser:
    def get_product_service(self, product_repo: ProductRepository) -> IProductService:
        return ProductService(product_repo)
