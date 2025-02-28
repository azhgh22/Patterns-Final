import json
import sqlite3
from typing import List

from playground.core.models.campaign import Campaign
from playground.core.services.classes.campaign_classes import CampaignRequestWithType


class CampaignSQLRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection
        self.cursor = connection.cursor()
        self._create_table()

    def _create_table(self) -> None:
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS campaigns (
                id TEXT PRIMARY KEY,
                description TEXT NOT NULL
            )
            """
        )
        self.connection.commit()

    def add_campaign(self, campaign: Campaign) -> None:
        try:
            self.cursor.execute(
                "INSERT INTO campaigns (id, description) VALUES (?, ?)",
                (
                    campaign.id,
                    json.dumps(
                        {
                            "type": campaign.description.type,
                            "params": campaign.description.params,
                        }
                    ),
                ),
            )
            self.connection.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Campaign already exists")

    def get_by_id(self, campaign_id: str) -> Campaign:
        self.cursor.execute(
            "SELECT id, description FROM campaigns WHERE id = ?", (campaign_id,)
        )
        row = self.cursor.fetchone()
        if row is None:
            raise ValueError(f"Campaign with id {campaign_id} not found")
        description_data = json.loads(row[1])
        campaign_request = CampaignRequestWithType(
            type=description_data["type"], params=description_data["params"]
        )
        return Campaign(id=row[0], description=campaign_request)

    def get_all(self) -> List[Campaign]:
        self.cursor.execute("SELECT id, description FROM campaigns")
        rows = self.cursor.fetchall()
        campaigns = []
        for row in rows:
            description_data = json.loads(row[1])
            campaign_request = CampaignRequestWithType(
                type=description_data["type"], params=description_data["params"]
            )
            campaigns.append(Campaign(id=row[0], description=campaign_request))
        return campaigns

    def delete_campaign(self, campaign_id: str) -> None:
        self.cursor.execute("DELETE FROM campaigns WHERE id = ?", (campaign_id,))
        if self.cursor.rowcount == 0:
            raise ValueError(f"Campaign with id {campaign_id} not found")
        self.connection.commit()
