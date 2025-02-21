from typing import Protocol

from playground.core.models.product import Product, ProductRequest


class IProductService(Protocol):
    def create(self, prod_req: ProductRequest) -> Product:
        pass

    def get_all(self) -> list[Product]:
        pass

    def update(self, p_id: str, price: int) -> bool:
        pass

    def get_product(self, p_id: str) -> Product | None:
        pass
