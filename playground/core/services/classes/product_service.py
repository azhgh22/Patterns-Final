from dataclasses import dataclass
from uuid import uuid4

from playground.core.models.product import ProductRequest, Product
from playground.core.services.interfaces.memory.product_repository import (
    ProductRepository,
)
from playground.infra.memory.in_memory.products_in_memory_repository import (
    ProductInMemoryRepository,
)


@dataclass
class ProductService:
    repo: ProductRepository = ProductInMemoryRepository()

    def create(self, prod_req: ProductRequest) -> Product | None:
        if prod_req.price < 0 or self.repo.contains_product_with_barcode(
            prod_req.barcode
        ):
            return None
        new_product = Product(
            str(uuid4()), prod_req.name, prod_req.barcode, prod_req.price
        )
        self.repo.store_product(new_product)
        return new_product

    def get_all(self) -> list[Product]:
        return self.repo.get_all_products()

    def update(self, p_id: str, price: int) -> bool:
        if price < 0:
            return False
        return self.repo.update_price(p_id, price)

    def get_product(self, p_id: str) -> Product | None:
        return self.repo.get_product_with_id(p_id)
