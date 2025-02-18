from typing import Protocol

from playground.core.models.product import ProductRequest, ProductResponse, Product


class IProductService(Protocol):
    def create(self, prod_req: ProductRequest) -> ProductResponse:
        pass

    def get_all(self) -> list[ProductResponse]:
        pass

    def update(self) -> ProductResponse:
        pass

    def get_product(self, p_id: str) -> Product:
        pass
