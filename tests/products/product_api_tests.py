from fastapi.testclient import TestClient

from playground.core.models.product import Product
from playground.core.services.classes.repository_in_memory_chooser import (
    InMemoryChooser,
)
from playground.core.services.interfaces.memory.product_repository import (
    ProductRepository,
)
from playground.infra.memory.in_memory.products_in_memory_repository import (
    ProductInMemoryRepository,
)
from playground.runner.setup import SetupConfiguration, setup


def get_http(
    product_repo: ProductRepository = ProductInMemoryRepository(),
) -> TestClient:
    return TestClient(setup(SetupConfiguration.for_testing(product_repo=product_repo)))


def test_should_return_empty_list() -> None:
    response = get_http().get("/products")
    assert response.status_code == 200
    assert 0 == len(response.json())


def test_should_list_all_products() -> None:
    product_list = [Product("1", "1", "1", 1)]
    http = get_http(ProductInMemoryRepository(product_list=product_list))
    response = http.get("/products")
    assert response.status_code == 200
    assert product_list == [Product(**(response.json()[0]))]


def test_should_update_product_price() -> None:
    product_list = [Product("1", "1", "1", 1)]
    http = get_http(ProductInMemoryRepository(product_list=product_list))
    response = http.patch("/products/1", json={"price": 10})
    assert response.status_code == 200
    assert product_list[0].price == 10


def test_should_not_update_price_of_non_existing_product() -> None:
    response = get_http().patch("/products/1", json={"price": 100})
    assert response.status_code == 404


def test_should_not_update_product_with_negative_price() -> None:
    product_list = [Product("1", "1", "1", 1)]
    http = get_http(ProductInMemoryRepository(product_list=product_list))
    response = http.patch("/products/1", json={"price": -10})
    assert response.status_code == 409
    assert product_list[0].price == 1


def test_should_add_new_product() -> None:
    product_list: list[Product] = []
    http = get_http(ProductInMemoryRepository(product_list=product_list))
    response = http.post("/products", json={"name": "1", "barcode": "1", "price": 10})
    assert response.status_code == 201
    assert len(product_list) == 1
    assert product_list[0] == Product(**response.json())
    assert product_list[0] == Product(product_list[0].id, "1", "1", 10)


def test_should_not_create_product_with_existing_barcode() -> None:
    product_list = [Product("1", "1", "1", 1)]
    http = get_http(ProductInMemoryRepository(product_list=product_list))
    response = http.post("/products", json={"name": "1", "barcode": "1", "price": 10})
    assert response.status_code == 409
    assert 1 == len(product_list)


def test_should_not_create_product_with_negative_price() -> None:
    product_list: list[Product] = []
    http = get_http(ProductInMemoryRepository(product_list=product_list))
    response = http.post("/products", json={"name": "1", "barcode": "1", "price": -10})
    assert response.status_code == 422
    assert 0 == len(product_list)
