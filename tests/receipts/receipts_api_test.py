from starlette.testclient import TestClient

from playground.core.models.product import Product
from playground.core.models.receipt import Receipt
from playground.core.services.classes.repository_in_memory_chooser import InMemoryChooser
from playground.core.services.interfaces.memory.product_repository import ProductRepository
from playground.core.services.interfaces.memory.receipt_repository import ReceiptRepository
from playground.infra.memory.in_memory.products_in_memory_repository import ProductInMemoryRepository
from playground.infra.memory.in_memory.receipts_in_memory_repository import ReceiptInMemoryRepository
from playground.runner.setup import setup, SetupConfiguration


def get_http(
    product_repo: ProductRepository = ProductInMemoryRepository(),
    receipt_repo: ReceiptRepository = ReceiptInMemoryRepository(),
) -> TestClient:
    return TestClient(
        setup(
            SetupConfiguration(
                repository_chooser=InMemoryChooser(product_repo=product_repo , receipt_repo=receipt_repo)
            )
        )
    )

def test_should_not_create_receipt():
    try:
        get_http().post("/receipts" , json = {"status" : "close"})
    except ValueError as e:
        raise "should be open" in str(e)

def test_should_create_receipt():
    receipts_list = []
    response = get_http(receipt_repo=ReceiptInMemoryRepository(receipts_list)).post("/receipts" , json = {"status" : "open"})
    assert response is not None
    assert response.status_code == 201
    assert len(receipts_list) == 1
    assert receipts_list[0] is not None
    assert receipts_list[0].status == "open"

def test_should_not_add_non_existing_product():
    receipts_list = [Receipt("1" , "open" , [])]
    try:
        get_http(receipt_repo=ReceiptInMemoryRepository(receipts_list)).post("receipts/11/products" , json = {"id" : "11" , "quantity" : 3})
    except ValueError as e:
        assert "does not exist" in str(e)

def test_should_not_add_product_to_non_existing_receipt():
    product_list = [Product("1" , "vashli" , "111" , 4)]
    try:
        get_http(product_repo=ProductInMemoryRepository(product_list)).post("/receipts/11/products" , json = {"id" : "1" , "quantity" : 3})
    except ValueError as e:
        assert "does not exist" in str(e)

def test_should_not_add_product_to_closed_receipt():
    product_list = [Product("1" , "vashli" , "111" , 4)]
    receipt_list = [Receipt("11" , "closed" , [])]
    try:
        get_http(product_repo=ProductInMemoryRepository(product_list) , receipt_repo=ReceiptInMemoryRepository(receipt_list)).post("receipts/11/products" , json = {"id" : "1" , "quantity" : 3})
    except ValueError as e:
        assert "should be open" in str(e)

def test_should_add_product_to_receipt():
    receipt_list = [Receipt("11" , "open" , [])]
    product_list = [Product("1" , "vashli" , "111" , 4)]
    response = get_http(product_repo=ProductInMemoryRepository(product_list) , receipt_repo=ReceiptInMemoryRepository(receipt_list)).post("receipts/11/products" , json = {"id" : "1" , "quantity" : 3})
    assert response.status_code == 200
    assert len(receipt_list[0].products) == 1
    assert receipt_list[0].products[0].product_id == "1"