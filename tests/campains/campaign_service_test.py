from playground.core.enums.receipt_status import ReceiptStatus
from playground.core.models.campaign import Campaign
from playground.core.models.receipt import Receipt, ReceiptItem
from playground.core.services.classes.campaign_classes import CampaignRequestWithType
from playground.core.services.classes.campaign_service import CampaignService
from playground.infra.memory.in_memory.campaign_in_memory_repository import (
    CampaignInMemoryRepository,
)


def test_env_works() -> None:
    pass


def test_campaign_not_exists() -> None:
    try:
        CampaignService().get_by_id("1")
    except ValueError:
        assert True


def test_should_return_campaign() -> None:
    cl = [Campaign(id="1", description=CampaignRequestWithType(type="1", params={}))]
    service = CampaignService(CampaignInMemoryRepository(cl))
    assert service.get_by_id("1") is not None
    assert service.get_by_id("1").id == "1"
    assert service.get_by_id("1").description is not None


def test_should_add_campaign() -> None:
    service = CampaignService(CampaignInMemoryRepository())
    res = service.create(CampaignRequestWithType(type="1", params={}))
    assert res is not None
    assert res.id is not None
    assert res.description.type == "1"
    try:
        service.create(CampaignRequestWithType(type="1", params={}))
        assert False
    except ValueError:
        assert True


def test_get_all() -> None:
    cl = [Campaign(id="1", description=CampaignRequestWithType(type="1", params={}))]
    service = CampaignService(CampaignInMemoryRepository(cl))
    res = service.get_all()
    assert res is not None
    assert len(res) == 1


def test_delete_by_id() -> None:
    service = CampaignService(CampaignInMemoryRepository())
    try:
        service.delete("1")
        assert False
    except ValueError:
        assert True

    res = service.create(CampaignRequestWithType(type="1", params={}))
    assert res is not None
    assert res.id is not None
    try:
        service.delete(res.id)
        assert True
    except ValueError:
        assert False


def test_get_campaign_request_with_type_instance_discount_product() -> None:
    service = CampaignService(CampaignInMemoryRepository())
    res = service.get_campaign_request_with_type_instance(
        "discount_product", **{"applicable_product": "1", "discount_percentage": 50}
    )
    assert res is not None
    assert res.type == "discount_product"
    assert res.params == {"applicable_product": "1", "discount_percentage": 50}


def test_get_campaign_request_with_type_instance_discount_receipt() -> None:
    service = CampaignService(CampaignInMemoryRepository())
    res = service.get_campaign_request_with_type_instance(
        "discount_receipt",
        **{"applicable_receipt": "1", "discount_percentage": 50, "required_price": 100},
    )
    assert res is not None
    assert res.type == "discount_receipt"
    assert res.params == {
        "applicable_receipt": "1",
        "discount_percentage": 50,
        "required_price": 100,
    }


def test_get_campaign_request_with_type_instance_combo() -> None:
    service = CampaignService(CampaignInMemoryRepository())
    res = service.get_campaign_request_with_type_instance(
        "combo", **{"product_ids": [], "discount_percentage": 50}
    )
    assert res is not None
    assert res.type == "combo"
    assert res.params == {"product_ids": [], "discount_percentage": 50}


def test_get_campaign_request_with_type_instance_buy_n_get_n() -> None:
    service = CampaignService(CampaignInMemoryRepository())
    res = service.get_campaign_request_with_type_instance(
        "buy_n_get_n", **{"product_id": "1", "required_quantity": 1}
    )
    assert res is not None
    assert res.type == "buy_n_get_n"
    assert res.params == {"product_id": "1", "required_quantity": 1}


def test_apply_discount_product() -> None:
    service = CampaignService(
        CampaignInMemoryRepository(
            [
                Campaign(
                    id="1",
                    description=CampaignRequestWithType(
                        type="discount_product",
                        params={"applicable_product": "1", "discount_percentage": 50},
                    ),
                )
            ]
        )
    )
    res = service.apply(
        Receipt(
            id="1",
            shift_id="1",
            status=ReceiptStatus.OPEN,
            products=[
                ReceiptItem(
                    receipt_id="1",
                    product_id="1",
                    quantity=1,
                    price=100,
                    total=100,
                ),
                ReceiptItem(
                    receipt_id="1",
                    product_id="2",
                    quantity=1,
                    price=100,
                    total=100,
                ),
            ],
            total=200,
            discounted_total=None,
        )
    )
    assert res is not None
    assert res.id == "1"
    assert res.discounted_total == 150
    assert res.products[0].price == 100
    assert res.products[0].total == 50


def test_apply_discount_receipt() -> None:
    service = CampaignService(
        CampaignInMemoryRepository(
            [
                Campaign(
                    id="1",
                    description=CampaignRequestWithType(
                        type="discount_receipt",
                        params={
                            "applicable_receipt": "1",
                            "discount_percentage": 50,
                            "required_price": 100,
                        },
                    ),
                )
            ]
        )
    )
    res = service.apply(
        Receipt(
            id="1",
            shift_id="5",
            status=ReceiptStatus.OPEN,
            products=[
                ReceiptItem(
                    receipt_id="1",
                    product_id="1",
                    quantity=1,
                    price=100,
                    total=100,
                ),
                ReceiptItem(
                    receipt_id="1",
                    product_id="2",
                    quantity=1,
                    price=100,
                    total=100,
                ),
            ],
            total=200,
            discounted_total=None,
        )
    )
    assert res is not None
    assert res.id == "1"
    assert res.discounted_total == 100


def test_apply_buy_n_get_n() -> None:
    service = CampaignService(
        CampaignInMemoryRepository(
            [
                Campaign(
                    id="1",
                    description=CampaignRequestWithType(
                        type="buy_n_get_n",
                        params={"product_id": "1", "required_quantity": 1},
                    ),
                )
            ]
        )
    )
    res = service.apply(
        Receipt(
            id="1",
            shift_id="4",
            status=ReceiptStatus.OPEN,
            products=[
                ReceiptItem(
                    receipt_id="1",
                    product_id="1",
                    quantity=1,
                    price=100,
                    total=100,
                ),
                ReceiptItem(
                    receipt_id="1",
                    product_id="2",
                    quantity=1,
                    price=100,
                    total=100,
                ),
            ],
            total=200,
            discounted_total=None,
        )
    )
    assert res is not None
    assert res.id == "1"
    assert res.discounted_total == 200
    assert res.products[0].price == 100
    assert res.products[0].quantity == 2


def test_apply_combo() -> None:
    service = CampaignService(
        CampaignInMemoryRepository(
            [
                Campaign(
                    id="1",
                    description=CampaignRequestWithType(
                        type="combo",
                        params={"product_ids": ["1", "2"], "discount_percentage": 50},
                    ),
                )
            ]
        )
    )
    res = service.apply(
        Receipt(
            id="1",
            shift_id="1",
            status=ReceiptStatus.OPEN,
            products=[
                ReceiptItem(
                    receipt_id="1",
                    product_id="1",
                    quantity=1,
                    price=100,
                    total=100,
                ),
                ReceiptItem(
                    receipt_id="1",
                    product_id="2",
                    quantity=2,
                    price=10,
                    total=20,
                ),
                ReceiptItem(
                    receipt_id="1",
                    product_id="3",
                    quantity=3,
                    price=10,
                    total=30,
                ),
            ],
            total=150,
            discounted_total=None,
        )
    )
    assert res is not None
    assert res.id == "1"
    assert res.products[0].price == 100
    assert res.products[0].quantity == 1
    assert res.products[1].total == 10
    assert res.products[1].quantity == 2

    assert res.discounted_total == 90


def test_apply_mixed_campaigns() -> None:
    service = CampaignService(
        CampaignInMemoryRepository(
            [
                Campaign(
                    id="1",
                    description=CampaignRequestWithType(
                        type="combo",
                        params={"product_ids": ["1", "2"], "discount_percentage": 10},
                    ),
                ),
                Campaign(
                    id="2",
                    description=CampaignRequestWithType(
                        type="buy_n_get_n",
                        params={"product_id": "2", "required_quantity": 1},
                    ),
                ),
                Campaign(
                    id="3",
                    description=CampaignRequestWithType(
                        type="discount_receipt",
                        params={
                            "applicable_receipt": "1",
                            "discount_percentage": 50,
                            "required_price": 100,
                        },
                    ),
                ),
                Campaign(
                    id="4",
                    description=CampaignRequestWithType(
                        type="discount_product",
                        params={"applicable_product": "1", "discount_percentage": 10},
                    ),
                ),
            ]
        )
    )
    res = service.apply(
        Receipt(
            id="1",
            shift_id="2",
            status=ReceiptStatus.OPEN,
            products=[
                ReceiptItem(
                    receipt_id="1",
                    product_id="1",
                    quantity=1,
                    price=100,
                    total=100,
                ),
                ReceiptItem(
                    receipt_id="1",
                    product_id="2",
                    quantity=2,
                    price=10,
                    total=20,
                ),
                ReceiptItem(
                    receipt_id="1",
                    product_id="3",
                    quantity=3,
                    price=10,
                    total=30,
                ),
            ],
            total=150,
            discounted_total=None,
        )
    )
    assert res is not None
    assert res.id == "1"
    assert res.products[1].quantity == 3
    assert res.discounted_total == 75
