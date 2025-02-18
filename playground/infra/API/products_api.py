from fastapi import APIRouter

from playground.core.models.product import Product, ProductRequest

products_api = APIRouter()


@products_api.post("")
async def create_product(product: ProductRequest) -> Product:
    pass
