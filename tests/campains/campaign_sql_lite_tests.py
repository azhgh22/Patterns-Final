import json
import sqlite3
from typing import Generator

import pytest

from playground.core.models.campaign import Campaign
from playground.core.services.classes.campaign_classes import CampaignRequestWithType
from playground.infra.memory.sql_lite.campaign_sql_lite_repository import (
    CampaignSQLRepository,
)


@pytest.fixture
def db_connection() -> Generator[sqlite3.Connection, None, None]:
    connection = sqlite3.connect("campaign_test_db", check_same_thread=False)
    yield connection
    connection.close()


@pytest.fixture
def repository(db_connection: sqlite3.Connection) -> CampaignSQLRepository:
    repo = CampaignSQLRepository(db_connection)
    repo.cursor.execute("DELETE FROM campaigns")
    repo.connection.commit()
    return repo


@pytest.fixture
def sample_campaign() -> Campaign:
    description = CampaignRequestWithType(
        type="discount", params={"discount_percentage": 20, "applicable_product": "123"}
    )
    return Campaign(id="1", description=description)


def test_add_campaign(
    repository: CampaignSQLRepository, sample_campaign: Campaign
) -> None:
    repository.add_campaign(sample_campaign)

    # Verify campaign was added
    repository.cursor.execute(
        "SELECT * FROM campaigns WHERE id = ?", (sample_campaign.id,)
    )
    row = repository.cursor.fetchone()
    assert row is not None
    assert row[0] == sample_campaign.id
    assert json.loads(row[1]) == {
        "type": sample_campaign.description.type,
        "params": sample_campaign.description.params,
    }


def test_add_campaign_two_times(
    repository: CampaignSQLRepository, sample_campaign: Campaign
) -> None:
    repository.add_campaign(sample_campaign)

    with pytest.raises(ValueError, match="Campaign already exists"):
        repository.add_campaign(sample_campaign)


def test_get_by_id(
    repository: CampaignSQLRepository, sample_campaign: Campaign
) -> None:
    repository.cursor.execute(
        "INSERT INTO campaigns (id, description) VALUES (?, ?)",
        (
            sample_campaign.id,
            json.dumps(
                {
                    "type": sample_campaign.description.type,
                    "params": sample_campaign.description.params,
                }
            ),
        ),
    )
    retrieved = repository.get_by_id("1")
    assert retrieved.id == sample_campaign.id
    assert retrieved.description.type == sample_campaign.description.type
    assert retrieved.description.params == sample_campaign.description.params


def test_get_by_id_not_found(repository: CampaignSQLRepository) -> None:
    with pytest.raises(ValueError, match="Campaign with id 2 not found"):
        repository.get_by_id("2")


def test_get_all(repository: CampaignSQLRepository, sample_campaign: Campaign) -> None:
    repository.cursor.execute(
        "INSERT INTO campaigns (id, description) VALUES (?, ?)",
        (
            sample_campaign.id,
            json.dumps(
                {
                    "type": sample_campaign.description.type,
                    "params": sample_campaign.description.params,
                }
            ),
        ),
    )
    campaigns = repository.get_all()
    assert len(campaigns) == 1
    assert campaigns[0].id == sample_campaign.id


def test_delete_campaign(
    repository: CampaignSQLRepository, sample_campaign: Campaign
) -> None:
    repository.cursor.execute(
        "INSERT INTO campaigns (id, description) VALUES (?, ?)",
        (
            sample_campaign.id,
            json.dumps(
                {
                    "type": sample_campaign.description.type,
                    "params": sample_campaign.description.params,
                }
            ),
        ),
    )
    repository.delete_campaign("1")

    # Verify campaign was deleted
    repository.cursor.execute("SELECT * FROM campaigns WHERE id = ?", ("1",))
    row = repository.cursor.fetchone()
    assert row is None


def test_delete_campaign_not_found(repository: CampaignSQLRepository) -> None:
    with pytest.raises(ValueError, match="Campaign with id 2 not found"):
        repository.delete_campaign("2")
