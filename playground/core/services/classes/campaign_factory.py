import typing

from playground.core.services.classes.campaign_classes import (
    BuyNGetNCampaign,
    CampaignInterface,
    ComboCampaign,
    DiscountCampaign,
)


class CampaignFactory:
    CAMPAIGN_TYPES = {
        "buy_n_get_n": BuyNGetNCampaign,
        "discount": DiscountCampaign,
        "combo": ComboCampaign,
    }

    @staticmethod
    def create_campaign(campaign_type: str, **kwargs: typing.Any) -> CampaignInterface:
        campaign_class = CampaignFactory.CAMPAIGN_TYPES.get(campaign_type)
        if not campaign_class:
            raise ValueError(f"Invalid campaign type: {campaign_type}")
        obj = campaign_class(**kwargs)
        if not isinstance(obj, CampaignInterface):
            raise ValueError("Invalid campaign type")
        return obj
