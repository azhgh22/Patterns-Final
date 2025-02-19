from fastapi import HTTPException
from typing import List

from starlette.requests import Request
from pydantic import BaseModel

from fastapi import APIRouter

from playground.core.models.product import Product, ProductRequest
from playground.core.services.interfaces.service_interfaces.product_service_interface import (
    IProductService,
)
from playground.core.services.interfaces.service_interfaces.repository_chooser_interface import (
    IRepositoryChooser,
)
from playground.core.services.interfaces.service_interfaces.service_chooser_interface import (
    IServiceChooser,
)

products_api = APIRouter()


def get_product_service(request: Request) -> IProductService:
    service_chooser: IServiceChooser = request.app.state.core
    repository_chooser: IRepositoryChooser = request.app.state.repo
    return service_chooser.get_product_service(repository_chooser.get_product_repo())


class ProductRequestModel(BaseModel):
    name: str
    barcode: str
    price: int


@products_api.post("/", status_code=201)
def create_product(request: Request, product: ProductRequestModel) -> Product:
    p_request = ProductRequest(product.name, product.barcode, product.price)
    new_product = get_product_service(request).create(p_request)
    if new_product is None:
        raise HTTPException(status_code=300)
    return new_product


@products_api.get("/", status_code=200)
def list_products(request: Request) -> List[Product]:
    service = get_product_service(request)
    return service.get_all()


class UpdateModel(BaseModel):
    price: int


@products_api.patch("/{product_id}")
def update_product(request: Request, product_id: str, data: UpdateModel) -> Product:
    service = get_product_service(request)
    try:
        service.update(product_id, data.price)
        return service.get_product(product_id)
    except ValueError:
        raise HTTPException(status_code=409)
    except IndexError:
        raise HTTPException(status_code=404)
