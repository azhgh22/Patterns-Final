from typing import List

from playground.core.models.campaign import Campaign


class CampaignInMemoryRepository:
    def __init__(self, campaign_list: List[Campaign] | None = None) -> None:
        self.campaigns: List[Campaign] = (
            campaign_list if campaign_list is not None else []
        )

    def add_campaign(self, campaign: Campaign) -> None:
        for camp in self.campaigns:
            if camp.equals(campaign):
                raise ValueError("Campaign already exists")
        self.campaigns.append(campaign)

    def get_by_id(self, campaign_id: str) -> Campaign:
        for campaign in self.campaigns:
            if campaign.id == campaign_id:
                return campaign
        raise ValueError(f"Campaign with id {campaign_id} not found")

    def get_all(self) -> List[Campaign]:
        return self.campaigns

    def delete_campaign(self, campaign_id: str) -> None:
        for campaign in self.campaigns:
            if campaign.id == campaign_id:
                self.campaigns.remove(campaign)
                return
        raise ValueError(f"Campaign with id {campaign_id} not found")
