from playground.core.models.campaign import Campaign, CampaignRequestWithType
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


def test_delete_by_id():
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


def test_get_campaign_request_with_type_instance_discount() -> None:
    service = CampaignService(CampaignInMemoryRepository())
    res = service.get_campaign_request_with_type_instance("discount")
    assert res is not None
    assert res.type == "discount"
    assert res.params == {"applicable_product": "1", "discount_percentage": 50}


def test_get_campaign_request_with_type_instance_combo() -> None:
    service = CampaignService(CampaignInMemoryRepository())
    res = service.get_campaign_request_with_type_instance("combo")
    assert res is not None
    assert res.type == "combo"
    assert res.params == {"product_ids": [], "discount_percentage": 50}


def test_get_campaign_request_with_type_instance_buy_n_get_n() -> None:
    service = CampaignService(CampaignInMemoryRepository())
    res = service.get_campaign_request_with_type_instance("buy_n_get_n")
    assert res is not None
    assert res.type == "buy_n_get_n"
    assert res.params == {"product_id": "1", "required_quantity": 1}


# todo: test apply ofter receipt is finished
