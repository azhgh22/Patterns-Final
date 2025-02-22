from fastapi.testclient import TestClient

from playground.core.models.campaign import Campaign, CampaignRequestWithType
from playground.core.services.classes.repository_in_memory_chooser import (
    InMemoryChooser,
)
from playground.core.services.interfaces.memory.campaign_repository import (
    CampaignRepository,
)

from playground.infra.memory.in_memory.campaign_in_memory_repository import (
    CampaignInMemoryRepository,
)

from playground.runner.setup import setup, SetupConfiguration


def get_http(
    campaign_repo: CampaignRepository = CampaignInMemoryRepository(),
) -> TestClient:
    return TestClient(
        setup(
            SetupConfiguration(
                repository_chooser=InMemoryChooser(campaign_repo=campaign_repo)
            )
        )
    )


def test_should_return_empty_list() -> None:
    response = get_http().get("/campaigns")
    assert response.status_code == 200
    assert response.json() == []


def test_delete() -> None:
    cl = [Campaign(id="1", description=CampaignRequestWithType(type="none", params={}))]
    response = get_http(CampaignInMemoryRepository(cl)).delete(f"/campaigns/{1}")
    assert response.status_code == 200

    response = get_http().delete(f"/campaigns/{1}")
    assert response.status_code == 404


def test_should_return_not_empty_list() -> None:
    cl = [
        Campaign(id="1", description=CampaignRequestWithType(type="none", params={})),
        Campaign(id="2", description=CampaignRequestWithType(type="none", params={})),
        Campaign(id="3", description=CampaignRequestWithType(type="none", params={})),
    ]

    response = get_http(CampaignInMemoryRepository(cl)).get("/campaigns")

    assert response.status_code == 200
    assert list(response.json()).__len__() == 3


def test_should_add_campaign_buy_n_get_n() -> None:
    response = get_http().post(
        "/campaigns?campaign_type=buy_n_get_n",
        json={"required_quantity": 2, "product_id": 123},
    )
    assert response.status_code == 200
    assert response.json().get("description")["type"] == "buy_n_get_n"


def test_should_add_campaign_combo() -> None:
    response = get_http().post(
        "/campaigns?campaign_type=combo",
        json={"product_ids": [], "discount_percentage": 10},
    )
    assert response.status_code == 200
    assert response.json().get("description")["type"] == "combo"
    assert response.json().get("description")["params"]["discount_percentage"] == 10


def test_should_add_campaign_discount() -> None:
    response = get_http().post(
        "/campaigns?campaign_type=discount",
        json={"discount_percentage": 20, "applicable_product": 10},
    )

    assert response.status_code == 200
    assert response.json().get("description")["type"] == "discount"
    assert response.json().get("description")["params"]["discount_percentage"] == 20
