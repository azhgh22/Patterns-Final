from typing import List

from fastapi import APIRouter

from playground.core.models.product import Product, ProductRequest

products_api = APIRouter()


@products_api.post("/")
async def create_product(product: ProductRequest) -> Product:
    pass


@products_api.get("/")
async def list_products() -> List[Product]:
    pass


@products_api.patch("/{product_id}")
async def update_product(product_id: str) -> Product:
    pass
