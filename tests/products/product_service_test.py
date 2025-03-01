from playground.core.models.product import Product, ProductRequest
from playground.core.services.classes.product_service import ProductService
from playground.infra.memory.in_memory.products_in_memory_repository import (
    ProductInMemoryRepository,
)


def test_env_works() -> None:
    pass


def test_should_not_find_product() -> None:
    assert ProductService().get_product("1") is None


def test_should_get_stored_product() -> None:
    product_list = [Product("1", "1", "1", 1)]
    service = ProductService(ProductInMemoryRepository(product_list))
    prod = service.get_product("1")
    assert product_list[0] == prod


def test_should_get_empty_list() -> None:
    assert ProductService().get_all() == []


def test_should_get_all_products() -> None:
    product_list = [Product("1", "1", "1", 1)]
    service = ProductService(ProductInMemoryRepository(product_list))
    assert service.get_all() == product_list


def test_should_not_update_non_existing_product() -> None:
    try:
        ProductService().update("1", 1)
        assert False
    except IndexError:
        assert True


def test_should_return_updated_product() -> None:
    prod_list = [Product("1", "1", "1", 1)]
    service = ProductService(ProductInMemoryRepository(prod_list))
    assert service.update("1", 2)
    assert 2 == prod_list[0].price


def test_should_not_update_with_negative_price() -> None:
    prod_list = [Product("1", "1", "1", 1)]
    service = ProductService(ProductInMemoryRepository(prod_list))
    try:
        service.update("1", -4)
        assert False
    except ValueError:
        assert True
    assert 1 == prod_list[0].price


def test_should_not_create_product_with_negative_price() -> None:
    try:
        ProductService().create(ProductRequest("1", "1", -3))
        assert False
    except ValueError:
        assert True


def test_should_store_product() -> None:
    product_list: list[Product] = []
    service = ProductService(ProductInMemoryRepository(product_list))
    product = service.create(ProductRequest("1", "1", 3))
    assert product is not None
    assert 1 == len(product_list)
    assert product_list[0] == product


def test_should_not_store_product_with_existing_barcode() -> None:
    prod_list = [Product("1", "1", "1", 1)]
    service = ProductService(ProductInMemoryRepository(prod_list))
    try:
        service.create(ProductRequest("1", "1", 1))
        assert False
    except IndexError:
        assert True
